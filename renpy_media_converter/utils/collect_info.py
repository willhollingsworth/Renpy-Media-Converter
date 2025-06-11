import os
import pathlib

from PIL import Image

if __name__ == '__main__':
    ''' fix for running a module as a script, '''
    import sys
    from os.path import dirname as up
    p_dir = up(up(up(__file__)))
    sys.path.append(p_dir) 

from renpy_media_converter.utils.get_config import load_settings

def add_to_dict(dict,val) -> None:
        if val in dict.keys():
                dict[val] += 1
        else:
              dict[val] = 1

def get_image_resolutions() -> None:
        resolutions = {}
        with open('file_paths.json','r') as f:
                file_list = json.load(f) 
        length = len(file_list)
        for i,image in enumerate(file_list):
                if i %100 == 0:
                        print(int(i/length*100),'% - files ', i)
                        print(resolutions)
                res = Image.open(image).size
                add_to_dict(resolutions,res)
        print(resolutions)
        