import pathlib
import sys
import os

def path_main_fixer(depth=3) -> bool:
    ''' fix for running a module as a script, '''
    main_folder = get_main_folder(depth)
    if not main_folder in sys.path:
            sys.path.append(main_folder)      
            return True
    else:
            return False
    

def get_main_folder(depth=3) -> str:
        script_path = pathlib.Path(__file__)
        main_folder = script_path
        for i in range(depth):
                main_folder = main_folder.parent
        return main_folder.__str__()

def try_import():
        try:
                import renpy_media_converter.utils.paths
                print('import success')
        except:
                print('failed import')

if __name__ == '__main__':
        try_import()
        path_main_fixer()
        try_import()
