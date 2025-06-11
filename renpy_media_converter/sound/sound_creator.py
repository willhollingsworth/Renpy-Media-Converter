import pydub
import os
import json
import subprocess
import logging

from pydub import AudioSegment
from pydub.playback import play

if __name__ == '__main__':
    ''' fix for running a module as a script, '''
    import sys
    from os.path import dirname as up
    p_dir = up(up(up(__file__)))
    sys.path.append(p_dir) 

from renpy_media_converter.utils import get_config
from renpy_media_converter.utils import read_write
from renpy_media_converter.utils import paths

config = get_config.Config()

'''
https://github.com/jiaaro/pydub
combining multiple audio streams https://github.com/jiaaro/pydub/blob/master/API.markdown#audiosegmentoverlay

'''
class Sound_creator():
    '''
    used to create audio files from ren'py image sequence data
    loads multiple audio files and combines them to a single track with the correct order and timing
    '''
    def __init__(self,
                  audio_folder = config.audio_folder,
                    output_folder = config.output_folder,
                    ):
        logging.basicConfig(filename='read_image_sequences.log', filemode='w', format='%(levelname)s - %(message)s',level=logging.WARNING)
        self.audio_folder = audio_folder
        self.output_folder = output_folder
        self.img_seqs = read_write.read_img_seqs_file()
        # at_exists = read_write.check_audio_trans_exists()
        # if not at_exists:   
            #build at
        self.audio_trans = read_write.read_audio_trans_file()

    def return_img_seqs(self):
        return self.img_seqs
    
    def create_audio_from_seq_data(self, target):
        ''' given a list of audio file and silences combine them into a single audio track
        cant get the audio files to combine in a loop without erroring out'''
        offset = 0
        total_length = self.img_seqs[target]['duration']*1000
        sounds = [AudioSegment.silent(total_length)]
        for i in self.img_seqs[target]['sounds']:
            if isinstance(i,(int,float)) :
                #found pause
                offset += i*1000
            elif isinstance(i,str):
                #found audio
                audio_name = self.audio_trans[i][0]
                audio_full_path = self.audio_folder.joinpath(audio_name)
                new_audio = AudioSegment.from_file(audio_full_path)

                sounds.append(sounds[-1].overlay(new_audio,position=offset))
                overrun = round((len(new_audio) + offset - total_length)/1000,2)
                if overrun > 0:
                    msg = f'{target}\'s sound runs longer than the total animation by {overrun} seconds'
                    logging.warning(msg)
        output_file_path = self.output_folder.joinpath(target+'.mp3')
        sounds[-1].export(output_file_path,format='mp3')
        logging.info(f'output {target} to {output_file_path}')
    
    def create_audio_sequential(self,input_list,output_filename):
        '''
        given a list of files and silence amounts create an mp3
        '''
        audio = AudioSegment.empty()
        for i in input_list:
            if isinstance(i,(int,float)) :
                audio += AudioSegment.silent(duration=i*100)
            elif isinstance(i,str):
                audio += AudioSegment.from_file(self.audio_folder.joinpath(i))
            else:
                raise Exception
        output_fullpath = self.output_folder.joinpath(output_filename)
        audio.export(output_fullpath,format='mp3')

def test_audio_sequential(input_list, output_filename):
    audio_sequential = Sound_creator()
    audio_sequential.create_audio_sequential(input_list, output_filename)
    # open_with_vlc(filename)

def test_audio_standard(target_sequence):
    audio_overlapping = Sound_creator()
    audio_overlapping.create_audio_from_seq_data(target_sequence)

def open_with_vlc(file_name):
    vlc_path = r'C:\Program Files (x86)\VideoLAN\VLC\vlc.exe'
    subprocess.call(f'{vlc_path} {os.getcwd()}\\{file_name}')

if __name__ == '__main__':

    target_sequence = 'example1'
    test_audio_standard(target_sequence)

    output_filename = 'sequential_test.mp3'
    input_list = [1,'sound1.mp3',.5,'sound2.mp3',.5,'sound3.wav',.5,'sound4.ogg']
    test_audio_sequential(input_list, output_filename)

