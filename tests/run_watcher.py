import pathlib
import subprocess
import os


repos_folder = pathlib.Path(__file__).parents[3]
runner_path = ['Misc-Scripts','detect_file_change','detect_file_change.py']
runner_path_full = repos_folder.joinpath(*runner_path)

target_folder = pathlib.Path(__file__).parents[1]

# target_file = 'test_get_config.py'
# target_command_full = pathlib.Path(__file__).parents[0].joinpath(target_file)

target_command_full = '-m unittest -v'

print(os.getcwd())
print(runner_path_full)
print(target_folder)
print(target_command_full)

commands = ['python',runner_path_full,target_folder,target_command_full]
subprocess.run(commands)
