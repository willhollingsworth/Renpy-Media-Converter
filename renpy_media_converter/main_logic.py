import os
import time
import logging

if __name__ == '__main__':
    ''' fix for running a module as a script, '''
    import sys
    from os.path import dirname as up
    p_dir = up(up(__file__))
    sys.path.append(p_dir) 


from renpy_media_converter.rpy_reader import rpy_reader
from renpy_media_converter.rpy_reader.img_seq_report import Animation_report

from renpy_media_converter.sound.sound_creator import Sound_creator
from renpy_media_converter.ffmpeg.create_video import Create_video


# import renpy_media_converter.rpy_reader# from renpy_media_converter.sound.sound_creator import Sound_creator
# import renpy_media_converter.utils
from renpy_media_converter.utils import get_config
from renpy_media_converter.utils import read_write
from renpy_media_converter.utils import paths

config = get_config.Config()



class Media_converter():
    def __init__(self,
                 game_folder = config.game_folder,
                 image_folder= config.image_folder,
                 output_folder= config.output_folder
                 ):
        logging.basicConfig(filename='media_converter.log', filemode='w', format='%(levelname)s - %(message)s',level=logging.WARNING)
        self.img_seqs = {}
        self.targets = []
        self.bad_targets = {}
        self.game_folder = game_folder
        self.image_folder = image_folder
        self.output_folder = output_folder


    def read_rpys(self):
        sequences = rpy_reader.read_image_sequences()
        sequences.process_all_rpy()
        self.img_seqs = sequences.img_seqs
        print(f'found {len(self.img_seqs)} image sequences')

    def read_audio_files(self):
        ... 

    def process_items(self,limit=None,sound_only=False):
        '''process all ren'py image sequences into webm files'''
        start = time.time()
        report = Animation_report()
        self.targets = report.return_zero_tag_items()
        print(f'after filtering {len(self.targets)} animations meet the requirements for processing')
        print(report.print_tag_per_anim_summary())

        sound_creator = Sound_creator()
        video_creator = Create_video(self.image_folder, self.output_folder)


        if limit:
            targets = self.targets[:limit]
        else:
            targets = self.targets

        # print(f'processing {len(targets)} items')
        # last_time = time.time()
        # log_interval_seconds = .5
        # for i,target in enumerate(targets):
        #     if time.time() - last_time > log_interval_seconds:
        #         percent_done = round(i/len(targets)*100,2)
        #         print(f'processed {i} items, {percent_done}% done')
        #         last_time = time.time()
        #     sound_creator.create_audio_from_seq_data(target)
        #     if not sound_only:
        #         video_creator.convert_image_sequence(target)
        # elapsed_seconds = int(time.time()-start)
        # print(f'finish processing, took {elapsed_seconds} seconds' )
    
    def export_targets(self):
        exports = []
        for target in self.targets:
            exports.append(target)
        filename = 'targets.json'
        folder = 'data'
        full_path = paths.get_main_folder().joinpath(folder).joinpath(filename)
        read_write.write_json_file(full_path,exports)

if __name__ == '__main__':
    img_seqs = Media_converter()
    img_seqs.read_rpys()
    img_seqs.process_items()

    # report = Animation_report()
    # report.run_reports()


    # img_seqs.export_targets()






    # img_seqs = rpy_reader.read_image_sequences()
    # img_seqs.process_all_rpy()
    # print('sequences :',len(img_seqs.img_seqs.keys()))

    # media_converter = Media_converter()
    # media_converter.process_items(game_folder,image_folder,output_folder,limit=1)


    # process_items(game_folder,image_folder,output_folder,limit=5)
    # media_converter.process_items(game_folder,image_folder,output_folder,limit=200,sound_only=True)
    # media_converter.process_items(game_folder,image_folder,output_folder)



    # input_path = r'D:\Games\Test_Renpy_game\images\example1'
    # output_path = r'D:\Games\Test_Renpy_game\dev\video_outputs'
    # ffmpeg_utils.convert_image_sequence(input_path,output_path)


