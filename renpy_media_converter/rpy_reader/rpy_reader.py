import os
import json
import logging
import pathlib
from pprint import pprint

import pydub

if __name__ == '__main__':
    ''' fix for running a module as a script, '''
    import sys
    from os.path import dirname as up
    p_dir = up(up(up(__file__)))
    sys.path.append(p_dir) 

from renpy_media_converter.rpy_reader.populate_fields import populate_img_seqs
from renpy_media_converter.rpy_reader.audio_translations import build_ats
from renpy_media_converter.rpy_reader.categorizer import Categorizer
from renpy_media_converter.rpy_reader.img_seq_report import Animation_report

from renpy_media_converter.utils import get_config
from renpy_media_converter.utils import paths
from renpy_media_converter.utils import read_write
# import renpy_media_converter.utils as utils

class read_image_sequences():
    '''collect information about image sequences stores in ren'py .rpy files'''

    def __init__(self, game_folder='') -> None:
        self.config = get_config.Config()
        if not game_folder:
            self.game_folder = self.config.game_folder
        else:
            self.game_folder = pathlib.Path(game_folder)

        logging.basicConfig(filename='rpy_reader.log', filemode='w', format='%(levelname)s - %(message)s',level=logging.INFO)
        self.rpy_files = paths.get_rpy_files()
        build_ats(rpy_files=self.rpy_files)
    
    def process_all_rpy(self) -> None:
        '''process all rpy files, write results to json file'''
        image_sequences = {}
        for file in self.rpy_files:
            new_sequences = self.get_image_sequences(self.game_folder.joinpath(file))
            image_sequences.update(new_sequences)
        log_msg = f'{len(image_sequences)} img sequences found'
        logging.info(log_msg)
        logging.info(f'files checked {", ".join(self.rpy_files)}')
        self.img_seqs = image_sequences
        read_write.write_img_seqs_file(self.img_seqs)

    def name_filter(self,string: str) -> str:
        ''' simple cleaning function'''
        string = string.replace('\n','').replace(':','').replace('image','').strip()
        return string

    def get_image_contents(self,lines: list,line_start: int) -> list[str]:
        ''' grab the contents of the image sequence as a list of lines'''
        output_lines = []
        for line in lines[line_start+1:]:
            if not line.startswith('    '):
                break
            output_lines.append(line.replace('\n','')[4:])
        return output_lines

    def read_txt_file(self,file_path:str) -> list[str]:
        with open(file_path,mode='r') as f:
            lines = f.readlines()
        return lines
    
    def get_image_sequences(self,file_path,start:int=0,stop:int=0):
        ''' read rpy file and extract image sequence details'''
        all_sequences = {}
        lines = self.read_txt_file(file_path)
        for i,line in enumerate(lines):
            if start:
                if i < start: continue
            if line.startswith('image'):
                if '/' in line:
                    continue
                cur_contents = self.get_image_contents(lines,i)
                cur_name = self.name_filter(line)
                get_fields = populate_img_seqs(
                    rpy_file=file_path,
                    curr_line=i,
                    curr_contents =cur_contents,
                    )
                img_sequence_fields = get_fields.get_img_seq_fields()
                categorizer = Categorizer(img_sequence_fields)
                categorizer.build_tags()
                img_sequence_fields = categorizer.anim
                all_sequences[cur_name] = img_sequence_fields
            if stop:
                if i> stop: break
        return all_sequences
    
    def return_first_anim(self):
        first_anim_key = list(self.img_seqs.keys())[0]
        anim = self.img_seqs[first_anim_key]
        anim['name'] = first_anim_key
        return anim
    
if __name__ == '__main__':
    sequence = read_image_sequences()
    sequence.process_all_rpy()
    print('total sequences :',len(sequence.img_seqs.keys()))
    print('first animation : ',sequence.return_first_anim()['name'])
    print()
    report = Animation_report()
    report.run_reports()
