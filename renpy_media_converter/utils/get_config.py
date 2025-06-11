import os
import configparser
import pathlib
from dataclasses import dataclass,field
import multiprocessing


if __name__ == '__main__':
    # from ..utils import main_path_fixer
    import main_path_fixer
    # from utils import main_path_fixer
    main_path_fixer.path_main_fixer()


import renpy_media_converter.utils.paths

config_filename = 'config.ini'

@dataclass
class Config():
    game_folder: os.PathLike = field(init=False)
    image_folder: os.PathLike = field(init=False)
    output_folder: os.PathLike = field(init=False)
    img_seqs_json: os.PathLike = field(init=False)
    at_json: os.PathLike = field(init=False)
    audio_folder: os.PathLike = field(init=False)

    def __post_init__(self):
        settings_dict = Get_config()._config_dict
        for k,v in settings_dict.items():
            setattr(self,k,v)
            
    def __str__(self) -> str:
        normal_fields = [f for f in self.__dir__() if not f.startswith('_')]
        return '\n'.join([f'{k} : {getattr(self,k)}' for k in normal_fields])

class Get_config():
    def __init__(self) -> None:
        self._config_dict = self.load_settings()
        
    def load_settings(self) -> dict:
        config = self.read_config_file()
        parsed_config = self.parse_config_file(config)
        fixed_config = self.fix_game_paths(parsed_config)
        return fixed_config
    
    def get_config_path(self) -> os.PathLike:
        dir_path = renpy_media_converter.utils.paths.get_main_folder()
        return dir_path.joinpath(config_filename)
    
    def read_config_file(self):
        full_path = self.get_config_path()
        config = configparser.ConfigParser()
        config.read(full_path)
        return config  

    def parse_config_file(self,config) -> dict[str,os.PathLike]:
        settings = {}
        for section in config.sections():
            for option in config.options(section):
                value = config.get(section, option).replace('\'','')
                value = pathlib.Path(value)
                if not value.is_dir():
                    if not value.parent.__str__() == 'game':
                        main_folder = renpy_media_converter.utils.paths.get_main_folder()
                        value = main_folder.joinpath(value)
                settings[option] = value
        return settings


    def fix_game_paths(self,config) -> dict[str,os.PathLike]:
        out_dict = {}
        game_folder = config['game_folder']
        for k,v in config.items():
            if v.parent.__str__() == 'game':
                path = game_folder.joinpath(v.relative_to('game'))
                out_dict[k] = path
            else:
                out_dict[k] = v
        return out_dict

if __name__ == '__main__':
    settings = Config()
    print(settings)



