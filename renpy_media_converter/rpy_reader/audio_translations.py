import os
import json
import pathlib

import pydub

if __name__ == '__main__':
    ''' fix for running a module as a script, '''
    import sys
    from os.path import dirname as up
    p_dir = up(up(up(__file__)))
    print(p_dir)
    sys.path.append(p_dir) 

import renpy_media_converter.utils.paths
import renpy_media_converter.utils.read_write
import renpy_media_converter.utils.get_config


def build_ats(rpy_files='',overwrite=False) -> dict:
    '''find all audio files in a rpy file, get their filepath and duration '''
    if not rpy_files:
            rpy_files = renpy_media_converter.utils.paths.get_rpy_files()

    out_dict = {}
    game_folder = renpy_media_converter.utils.get_config.Config().game_folder
    game_folder = pathlib.Path(game_folder)
    audio_folder = game_folder.joinpath('audio')
    if not renpy_media_converter.utils.read_write.check_audio_trans_exists() or overwrite:       
        for file in rpy_files:
            with open(file,mode='r') as f:
                lines = f.readlines()
            for i,line in enumerate(lines):
                if '(trans, st, at):' in line:
                    func_name = line.split('def ')[1].split('(')[0]
                    file_name = lines[i+1].split('"')[1:2][0].split('/')[1]
                    full_path = audio_folder.joinpath(file_name)
                    try :
                        duration = round(len(pydub.AudioSegment.from_file(full_path))/1000,2)
                        out_dict[func_name] = [file_name,duration]
                    except FileNotFoundError:
                        print('cant find',file_name,'for',func_name)
                        duration = 0
        renpy_media_converter.utils.read_write.write_audio_trans_file(out_dict)
    else:
        out_dict = renpy_media_converter.utils.read_write.read_audio_trans_file()
    return out_dict

if __name__ == '__main__':
    audio = build_ats(overwrite=True)
    print(len(audio),'audio files processed')
