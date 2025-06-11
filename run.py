import renpy_media_converter.utils.paths
import renpy_media_converter.utils.get_config
import renpy_media_converter.main_logic


config = renpy_media_converter.utils.get_config.Config()
folders = ['game_folder','image_folder','output_folder']

args = [config.__getattribute__(f) for f in folders]
img_seqs = renpy_media_converter.main_logic.Media_converter(*args)
# img_seqs.read_rpys()


# img_seqs.process_items()






# read_image_sequences(game_folder)
# print(dir(img_seqs))