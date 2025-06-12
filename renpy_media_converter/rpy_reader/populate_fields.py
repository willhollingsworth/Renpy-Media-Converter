import os

import pydub

from renpy_media_converter.utils import read_write

class populate_img_seqs:
    def __init__(self,rpy_file,curr_line:int,curr_contents:list):
        self.rpy_file = rpy_file
        self.curr_line = curr_line
        self.curr_contents = curr_contents
        self.audio_translations = read_write.read_audio_trans_file()
        
    def get_img_seq_fields(self) -> dict:
        cur_images = self.get_cur_images()
        img_sequence = {}
        img_sequence['path'] = self.get_image_path()
        img_sequence['rpy'] = {}
        img_sequence['rpy']['rpy_file'] = self.rpy_file.name
        img_sequence['rpy']['line_start'] = self.curr_line+1
        img_sequence['rpy']['line_end'] = self.curr_line+1+len(self.curr_contents)
        img_sequence['rpy']['line_total'] = img_sequence['rpy']['line_end'] - img_sequence['rpy']['line_start']
        img_sequence['frame_rate'] = self.get_frame_rate()
        img_sequence['sounds'] = self.get_image_sounds()
        img_sequence['duration'] = self.get_seq_duration(img_sequence['sounds'])
        img_sequence['sound overrun'] = self.get_sound_overrun(img_sequence['sounds'],img_sequence['duration'])
        img_sequence['img count'] = len(cur_images)
        img_sequence['imgs ordered'] = self.check_images_ordered(cur_images)
        img_sequence['img type'] = cur_images[0].split('.')[-1]
        img_sequence['repeat'] = self.get_repeat()
        return img_sequence
        
    def get_image_path(self) -> str:
        '''parse the image sequence and grab the first image's folder location'''
        for line in self.curr_contents:
            if line.startswith('"images/'):
                separator = '\\'
                output = separator.join(line.replace('"','').split('/')[:-1])
                return output

    def get_frame_rate(self):
        ''' parse the image sequence and read all the sleep values
            either return a consistent frame rate or list of the differing sleep values
        '''
        pause_amount = None
        for line in self.curr_contents:
            if 'pause' in line:
                current_pause_amount = line.split('pause ')[1]
                if pause_amount and current_pause_amount != pause_amount:
                    if current_pause_amount not in pause_amount:
                        if isinstance(pause_amount,list):
                            pause_amount = [*pause_amount,current_pause_amount]
                        else:
                            pause_amount = [pause_amount,current_pause_amount]
                else:
                    pause_amount = current_pause_amount
        if not isinstance(pause_amount,list) and pause_amount:
            frame_rate = round(1/float(pause_amount),2)
        elif pause_amount:
            frame_rate = pause_amount
        if not pause_amount:
            return None
        return frame_rate

    def get_seq_duration(self,sounds:list) -> float:
        '''given a sounds list determine the total image sequence length'''
        total = 0
        for i in sounds:
            if isinstance(i,float):
                total += i
        return total
    
    def get_cur_images(self) -> list[str]:
        ''' get all images associated with a img seq'''
        images = []
        for line in self.curr_contents:
            if line.startswith('"images/'):
                images.append(line.split('/')[-1].replace('"',''))
        return images

    def check_images_ordered(self,images) -> bool:
        ''' check that all the image files are ordered otherwise ffmpeg will have issues
            slight complexity due to mixed letter and numbers names'''
        previous = None
        for x in images:
            formatted = x.split('.')[0]
            if not formatted.isdigit():
                formatted = self.find_tailing_numbers(formatted)
                if not formatted:
                    return False
            num = int(formatted)
            if previous:
                if previous - num > 1:
                    return False
            else:
                num = previous
        return True
    
    def find_tailing_numbers(self,str:str):
        '''convert a mixed letter and number string to the tailing numbers only'''
        index = self.get_last_letter_index(str)
        if index:
            return str[index:]
        else:
            return False
        
    def get_last_letter_index(self,str:str) -> int:
        '''given a string find the index of the last letter'''
        numbers = '0123456789'
        for i,c in enumerate(str[::-1]):
            if c not in numbers:
                return -i
        return False

    def get_sound_overrun(self,sounds:list,duration:float) -> float:
        offset,overrun = 0,0
        for i in sounds:
            if isinstance(i,float):
                offset += float(i)
            elif isinstance(i,str):
                i_length = self.audio_translations[i][1]
                i_end = offset + i_length
                if i_end > duration:
                    new_overrun = i_end - duration
                    if new_overrun > overrun:
                        overrun = new_overrun
        return round(overrun,2)

    def get_repeat(self) -> bool:
        for line in self.curr_contents:
            if line.strip() == 'repeat':
                return True
        return False
    
    def get_image_sounds(self) -> list[str]:
        '''parse image sequence and find both sounds and their timings (count sleep amounts)'''
        sounds = []
        pause_amount = 0
        for line in self.curr_contents:
            if line.startswith('pause'):
                sleep_length = line.replace('pause ','')
                pause_amount += round((float(sleep_length)),2)
            elif line.startswith('function'):
                if pause_amount > 0:
                    sounds.append(round(pause_amount,2))
                    pause_amount = 0
                sound_name = line.replace('function ','')
                sounds.append(sound_name)
        if pause_amount > 0:
            sounds.append(round(pause_amount,2))
        types = [str(type(x)) for x in sounds]
        if '<class \'str\'>' not in types:
            sounds = []
        return sounds

    def convert_audio_name(self,func_name: str) -> str:
        ''' convert audio name from function name to audio file
            need better way to do this as not all names are consistent
        '''
        folder_path = r'D:\Games\Test_Renpy_game\game\audio'
        all_audio = os.listdir(folder_path)
        for audio in all_audio:
            if func_name in audio:
                return func_name
        return func_name

if __name__ == '__main__':
    pass


