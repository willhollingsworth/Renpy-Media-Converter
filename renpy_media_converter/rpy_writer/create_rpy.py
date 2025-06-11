
import pathlib


if __name__ == '__main__':
    ''' fix for running a module as a script, '''
    import sys
    from os.path import dirname as up
    p_dir = up(up(up(__file__)))
    sys.path.append(p_dir) 

from renpy_media_converter.utils import read_write
from renpy_media_converter.utils import get_config
from renpy_media_converter.utils import paths
config = get_config.Config()
main_folder = paths.get_main_folder()

webm_folder = 'webm'


class Create_rpy():
    def __init__(self):
        self.output_path = ''
        self.animations = self.load_animation_targets()
        
    def create_new(self):
        target_path = main_folder.joinpath('exports','webms').with_suffix('.rpy')
        write_data = self.build_new_rpy_data()
        with open(target_path,mode='w') as f:
             f.writelines(write_data)

    def build_new_rpy_data(self):
        output_text = []
        for anim in self.animations:
            anim_str = f'image {anim} = Movie(play="{webm_folder}/{anim}.webm")\r'
            output_text.append(anim_str)
        return output_text
        
    def load_animation_targets(self):
        target_path = main_folder.joinpath('data','targets').with_suffix('.json')
        targets = read_write.read_json_file(target_path)
        return targets



if __name__ == '__main__':
    create_rpy = Create_rpy()
    create_rpy.create_new()