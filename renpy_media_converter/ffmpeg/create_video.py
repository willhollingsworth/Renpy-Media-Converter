'''
You can use ffmpeg to convert the images into a video. 
The command is something like this: ffmpeg -framerate 30 -i <frame_name>%d.jpg -c:v libx264 -pix_fmt yuv420p output.webm

From <https://discord.com/channels/286633898581164032/286633898581164032/1027405222030610473> 

    links
official docs https://ffmpeg.org/ffmpeg.html
framerate https://trac.ffmpeg.org/wiki/ChangingFrameRate
simple command explanations http://wiki.webmproject.org/ffmpeg
ffmpeg image sequence docs https://en.wikibooks.org/wiki/FFMPEG_An_Intermediate_Guide/image_sequence#Numbered_with_leading_zeroes
collection of guides for ffmpeg https://trac.ffmpeg.org/ 


encoding types
h264 https://trac.ffmpeg.org/wiki/Encode/H.264
vp9 https://trac.ffmpeg.org/wiki/Encode/VP9


instead of the input method being a path with simple schema like path\%04d.jpg 
you can specify a text file with each image's path
see https://stackoverflow.com/questions/31201164/ffmpeg-error-pattern-type-glob-was-selected-but-globbing-is-not-support-ed-by

'''

import os
import subprocess
import time
import json

if __name__ == '__main__':
    ''' fix for running a module as a script, '''
    import sys
    from os.path import dirname as up
    p_dir = up(up(__file__))
    sys.path.append(p_dir) 

from renpy_media_converter.utils import get_config

base = 'cmd /c'


class Create_video():
    def __init__(self):
        self.ffmpeg_path = r'C:\Apps\ffmpeg-20200831-4a11a6f-win64-static\bin\ffmpeg.exe'
        self.image_folder = get_config.Config().image_folder
        self.output_folder = get_config.Config().output_folder
        self.img_seqs = self.read_img_seq_file()

    def img_seq_args(self):
        args = []
        #hide banner
        args.append('-hide_banner')
        # sets the codecs
        args.append('-c:v libx264')
        # sets profile to very high
        args.append('-profile:v high')
        #quality
        args.append('-crf 18')
        # pixel format
        args.append('-pix_fmt yuv420p')
        # # output report
        # args.append('-report')
        args_final = " ".join(args)
        return args_final
    
    def convert_image_sequence(self,target):
        global ffmpeg_path
        global base
        start = time.time()
        target_folder = self.image_folder + self.img_seqs[target]['path'][6:]
        input_start_frame = os.listdir(target_folder)[0].split('.')[0]
        input_framerate = self.img_seqs[target]['frame_rate']
        output_framerate = 30
        args_final = self.img_seq_args()
        output_full = f'{self.output_folder}\{target}.webm'
        inputs = f'-start_number {input_start_frame} -r {input_framerate} -i "{target_folder}\%04d.jpg"'
        input_sound_path = f'{self.output_folder}\{target}.mp3'
        sound_exists = os.path.exists(input_sound_path)
        if sound_exists:
            inputs = f'{inputs} -i "{input_sound_path}"'
        in_out_paths =  f'{inputs} -r {output_framerate} "{output_full}"'
        commands = ['cmd /c',self.ffmpeg_path,in_out_paths,args_final]
        final_command = " ".join(commands)
        if os.path.exists(output_full):
            os.remove(output_full)
        result = subprocess.run(final_command, capture_output=True).stderr.decode('utf-8')
        if sound_exists:
            os.remove(input_sound_path)
        print(target, 'processed in',round(time.time() - start,1),'seconds \t',result.split('\n')[-2])

    def read_img_seq_file(self):
        file_path  = get_config.Config().img_seqs_json
        img_seqs = {}
        with open(file_path,'r') as f:
            img_seqs = json.load(f)
        return img_seqs

    def render_last_frame(self,target_file_name):
        global ffmpeg_path
        global base
        start = time.time()
        args = []
        # # output report
        # args.append('-report')
        args_final = " ".join(args)
        target_command = f'-sseof -1 -i "{target_file_name}"'
        output_image = 'lastfr.png'
        output_command = f'-update 1 "{output_image}"'
        commands = ['cmd /c',self.ffmpeg_path,target_command,args_final,output_command]
        final_command = " ".join(commands)
        print(final_command)
        try: 
            os.remove(output_image)
        except:
            pass
        result = subprocess.run(final_command, capture_output=True).stderr.decode('utf-8')
        print(target_file_name, 'last frame output in',round(time.time() - start,1),'seconds \t',result.split('\n')[-2])

def test_create_img_seq_video():
    target = 'looping1'
    create_video = Create_video()
    create_video.convert_image_sequence(target)

def test_render_last_frame():
    target_file_name = r'D:\Games\dev\video_outputs\example1.webm'
    create_video = Create_video()
    create_video.render_last_frame(target_file_name)    

if __name__ == '__main__':
    test_create_img_seq_video()
    # test_render_last_frame()
    # input_path = r'D:\Games\Test_Renpy_game\images\example1'
    # output_path = r'D:\Gamese\dev\video_outputs'

    # convert_image_sequence(input_path,output_path)
    # render_last_frame(output_path+r'\example1.webm')


    