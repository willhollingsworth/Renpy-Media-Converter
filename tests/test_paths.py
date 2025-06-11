import unittest
import os

from common import Path_fixing
Path_fixing().fix_path()

from renpy_media_converter.utils import paths

class Paths_test(unittest.TestCase):
    
    def test_rpy_files_length(self):
        rpy_files = paths.get_rpy_files()
        length = len(rpy_files)
        self.assertGreater(length,0)

    def test_rpy_files_valid(self):
        rpy_files = paths.get_rpy_files()
        first_file = rpy_files[0]
        self.assertTrue(os.path.isfile(first_file))

    def test_get_main_folder(self):
        main_folder = paths.get_main_folder()
        self.assertTrue(os.path.isdir(main_folder))

if __name__ == '__main__':
    unittest.main()