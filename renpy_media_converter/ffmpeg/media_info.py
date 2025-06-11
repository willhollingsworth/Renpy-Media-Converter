import subprocess
import json

ffprobe_path = r'C:\Apps\ffmpeg-20200831-4a11a6f-win64-static\bin\ffprobe.exe'
base_command = 'cmd /c'


def count_frames(input):
    ''' given an input video return the total frame count
    '''
    global ffprobe_path
    global base_command
    target_full = f'-i "{input}"'
    args = []

    args.append('-v quiet -show_entries stream=nb_read_packets -count_packets -select_streams v:0')
    args.append('-print_format json')

    args_final = " ".join(args)
    commands = [base_command,ffprobe_path,target_full,args_final]
    final_command = " ".join(commands)
    # print(final_command)
    result = subprocess.run(final_command, stdout=subprocess.PIPE).stdout.decode('utf-8')
    result = json.loads(result)['streams'][0]['nb_read_packets']
    return result


def show_frame_types(input):
    ''' given an input video return the total frame count
    '''
    global ffprobe_path
    global base_command
    target_full = f'-i "{input}"'

    args = []
    args.append('-v quiet -show_frames -show_entries frame=pict_type')
    args.append('-print_format json')

    args_final = " ".join(args)
    commands = [base_command,ffprobe_path,target_full,args_final]
    final_command = " ".join(commands)
    # print(final_command)
    result = subprocess.run(final_command, stdout=subprocess.PIPE).stdout.decode('utf-8')
    result = json.loads(result)['frames']
    result = [x['pict_type'] for x in result]
    return result

if __name__ == '__main__':
    target = r'D:\Games\dev\video_outputs\output.webm'
    print(count_frames(target))
    print(show_frame_types(target))