import pathlib
import json
import os

if __name__ == '__main__':
        import main_path_fixer
        main_path_fixer.path_main_fixer()

def get_main_folder(depth=3) -> os.PathLike:
        script_path = pathlib.Path(__file__)
        main_folder = script_path
        for i in range(depth):
                main_folder = main_folder.parent
        return main_folder

def collect_file_list(path) -> list[os.PathLike]:
        file_list = []
        for root, subdirs, files in os.walk(path):
                for file in files:
                        filepath = root+'\\'+file
                        filepath = pathlib.Path(root).joinpath(file).as_posix()
                        file_list.append(filepath)
        # print(len(file_list),'files collected')
        # with open('file_paths.json','w') as f:
        #         json.dump(file_list,f)
        return file_list

def get_rpy_files() -> list:
        '''parse game folder for all .rpy files'''
        import renpy_media_converter.utils.get_config
        config = renpy_media_converter.utils.get_config.Config()
        game_folder = config.game_folder
        rpy_files = [file for file in os.listdir(game_folder) if file.endswith('.rpy')]
        rpy_full_paths = [pathlib.Path(game_folder).joinpath(file).as_posix() for file in rpy_files]
        return rpy_full_paths
        
if __name__ == '__main__':
        print(get_main_folder())
        rpy_files = get_rpy_files()
        file_list = collect_file_list(get_main_folder().joinpath('renpy_media_converter').joinpath('utils'))

