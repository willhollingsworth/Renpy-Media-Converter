
import pathlib
from pprint import pprint
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


class Edit_rpy():
    def __init__(self):
        self.animations = self.load_animation_targets()
        self.img_seqs = read_write.read_img_seqs_file()
        self.skip_list = self.build_skip_list()
        self.skip_named = self.build_skip_named()
        self.rpy_paths = paths.get_rpy_files()

    def build_skip_named(self):
        skip_named = {}
        for anim in self.animations:
            rpy_file = self.img_seqs[anim]['rpy']['rpy_file']
            if not rpy_file in skip_named.keys():
                skip_named[rpy_file] = []
            skip_named[rpy_file].append(anim)
        return skip_named

    def build_skip_list(self):
        skip_list = {}
        for anim in self.animations:
            details = self.img_seqs[anim]['rpy']
            rpy_file = details['rpy_file']
            rpy_start = details['line_start']
            rpy_end = details['line_end']
            if not rpy_file in skip_list.keys():
                skip_list[rpy_file] = []
            skip_list[rpy_file].append([rpy_start,rpy_end])
        return skip_list

    def modify_single_rpy(self,rpy_file):
        rpy_contents = self.read_rpy_file(rpy_file)
        if not rpy_file in self.skip_list.keys():
            print('skipping',rpy_file)
            return
        skip_list = self.skip_list[rpy_file]
        edited,skipped = [],[]
        for i,line in enumerate(rpy_contents):
            # if line.strip() == '':
            #     continue
            if self.between_multi(i+1,skip_list):
                skipped.append(line)
            else:
                edited.append(line)
        edited_full_path = main_folder.joinpath('exports','edited',rpy_file).with_suffix('.rpy')
        self.write_rpy_file(edited,edited_full_path)
        skipped_full_path = main_folder.joinpath('exports','skipped',rpy_file).with_suffix('.rpy')
        self.write_rpy_file(skipped,skipped_full_path)

    def modify_all_rpys(self):
        rpys = self.skip_list.keys()
        for rpy in rpys:
            self.modify_single_rpy(rpy)

    def read_rpy_file(self,rpy_file):
        full_path = [i for i in self.rpy_paths if rpy_file in i][0]
        with open(full_path,mode='r') as f:
            lines = f.readlines()
        return lines

    def write_rpy_file(self,data,full_path):
        parent = full_path.parent
        if not parent.is_dir():
            parent.mkdir()
        with open(full_path,mode='w') as f:
             f.writelines(data)

    def between_single(self,num,range):
        return num>=range[0] and num <= range[1] 
    def between_multi(self,num,range_2d):
        return any([self.between_single(num,i) for i in range_2d])
    
    def load_animation_targets(self):
        target_path = main_folder.joinpath('data','targets').with_suffix('.json')
        targets = read_write.read_json_file(target_path)
        return targets

if __name__ == '__main__':
    edit_rpy = Edit_rpy()

    # rpy= 'example1.rpy'
    # edit_rpy.modify_single_rpy(rpy)
    # print(edit_rpy.skip_named[rpy])

    # rpy= 'script.rpy'
    # edit_rpy.modify_single_rpy(rpy)
    # print(edit_rpy.skip_named)
    print(edit_rpy.img_seqs['example1'])
    # edit_rpy.modify_all_rpys()



