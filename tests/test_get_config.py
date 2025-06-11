import sys
import os
import unittest

from common import Path_fixing
Path_fixing().fix_path()


from renpy_media_converter.utils import get_config


class Config_test(unittest.TestCase):
    def test_get_config(self):
        config = get_config.Config()
        self.assertIsNotNone(config)

    def test_config_length(self):
        config = get_config.Config()
        config_fields = [f for f in config.__dir__() if not f.startswith('_')]
        self.assertGreater(len(config_fields),1)

# def suite():
#     """This testsuite's main function."""
#     return unittest.TestLoader().loadTestsFromName(__name__)


if __name__ == '__main__':
    # Config_test().test_config_length()
    unittest.main()