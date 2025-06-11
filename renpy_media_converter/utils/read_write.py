import json
import os

if __name__ == '__main__':
    ''' fix for running a module as a script, '''
    import sys
    from os.path import dirname as up
    p_dir = up(up(up(__file__)))
    sys.path.append(p_dir) 

from renpy_media_converter.utils import get_config
from renpy_media_converter.utils import paths
config = get_config.Config()
main_folder = paths.get_main_folder()

def write_json_file(filename,data) -> None:
    parent_folder = os.path.dirname(filename)
    if not os.path.exists(parent_folder):
        os.mkdir(parent_folder)
    with open(filename,mode='w') as f:
        json.dump(data, f,indent=4)

def read_json_file(filename) -> dict:
    with open(filename,'r') as f:
        out_dict = json.load(f)
    return out_dict

def read_audio_trans_file() -> dict:
    return read_json_file(config.at_json)

def write_audio_trans_file(at:dict) -> None:
    write_json_file(config.at_json,at)

def check_audio_trans_exists() -> bool:
    return os.path.exists(config.at_json)

def read_img_seqs_file() -> dict:
    return read_json_file(config.img_seqs_json)

def write_img_seqs_file(img_seq) -> None:
    write_json_file(config.img_seqs_json,img_seq)

def check_img_seqs_exists() -> bool:
    return os.path.exists(config.img_seqs_json)

def delete_audio_trans_file():
    if check_audio_trans_exists():
        os.remove(config.at_json)

if __name__ == '__main__':
    delete_audio_trans_file()
    test_dict = {1:2,3:4}
    write_audio_trans_file(test_dict)
    at = read_audio_trans_file()
    print(at)
    delete_audio_trans_file()
