import unittest
import pathlib

from common import Path_fixing
Path_fixing().fix_path()

from renpy_media_converter.rpy_reader import audio_translations
from renpy_media_converter.utils import get_config

class Config_test(unittest.TestCase):

    def test_at_length(self):
        ats = audio_translations.build_ats()
        length = len(ats)
        self.assertGreater(length,0)

    def test_no_zero_duration(self):
        ats = audio_translations.build_ats()
        for _,detail in ats.items():
            duration = detail[1]
            self.assertGreater(duration,0)

    def test_valid_path(self):
        ats = audio_translations.build_ats()
        audio_folder = get_config.Config().audio_folder
        for _,detail in ats.items():
            filename = detail[0]
            full_path = pathlib.Path(audio_folder).joinpath(filename)
            self.assertTrue(full_path.is_file())

if __name__ == '__main__':
    unittest.main()
    Config_test()
