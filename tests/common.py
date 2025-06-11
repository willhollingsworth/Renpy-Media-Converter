import os
import sys

print(os.getcwd())
# from ..renpy_media_converter.utils import main_path_fixer
# import ..renpy_media_converter

class Path_fixing():
    def __init__(self):
        self.parent_folder = self.get_parent_folder()

    def go_up(self,path,loops=2):
        for x in range(loops):
            path = os.path.dirname(path)
        return  path

    def get_parent_folder(self):
        return self.go_up(__file__)
    
    def fix_path(self):
        if self.parent_folder in sys.path:
            return
        sys.path.append(self.parent_folder)



if __name__ == '__main__':
    Path_fixing().fix_path()
