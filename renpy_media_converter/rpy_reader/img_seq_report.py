

import pydub

if __name__ == '__main__':
    ''' fix for running a module as a script, '''
    import sys
    from os.path import dirname as up
    p_dir = up(up(up(__file__)))
    sys.path.append(p_dir) 

from renpy_media_converter.utils import get_config
from renpy_media_converter.utils import paths
from renpy_media_converter.utils import read_write


class Animation_report():
    def __init__(self):
        self.img_seqs = read_write.read_img_seqs_file()
        self.tag_count = self.parse_all_tags()
        self.tags_per_animation = self.parse_tags_per_animation()

    def run_reports(self,full=False):
        print('total animations',len(self.img_seqs))
        print()
        print(self.print_tag_per_anim_summary())
        print()
        print(self.print_tags_occurrence_summary())
        print()
        print( self.print_longest_anim_line_count())
        print()
        print(self.print_longest_anim_duration())
        if not full: return
        print()
        print(self.print_anims_without_issues())

    def parse_tags_per_animation(self):
        tags_per_animation_count   = {}
        for name,details in self.img_seqs.items():
            tag_count = len(details['tags'])
            if tag_count not in tags_per_animation_count:
                tags_per_animation_count[tag_count] = {'count':0,'seqs':[]}
            tags_per_animation_count[tag_count]['count'] += 1
            tags_per_animation_count[tag_count]['seqs'].append(name)
        return tags_per_animation_count
    
    def print_tag_per_anim_summary(self):
        str_list = [f'{k}:{v["count"]}' for (k,v) in self.tag_count.items()]
        output = ', '.join(str_list)
        return 'tag amount on animations\n'+output

    def parse_all_tags(self): 
        tag_count = {}
        tag_count['no tags'] = {'count':0,'seqs':[]}
        for name,details in self.img_seqs.items():
            tags = details['tags']
            for tag in tags:
                if tag not in tag_count:
                    tag_count[tag] = {'count':0,'seqs':[]}
                tag_count[tag]['count'] += 1
                tag_count[tag]['seqs'].append(name)
            if tags == []:
                tag_count['no tags']['count'] += 1
                tag_count['no tags']['seqs'].append(name)
        return tag_count
    
    def print_tags_occurrence_summary(self):
        str_list = [f'{k} tags:{v["count"]}' for (k,v) in self.tags_per_animation.items()]
        output = ', '.join(str_list)
        return 'total count of tags\n'+output
    
    def return_zero_tag_items(self):
        return self.tags_per_animation[0]['seqs']
    
    def print_longest_anim_line_count(self):
        dict_list = list(self.img_seqs.items())
        dict_list = sorted(dict_list,key=lambda x:x[1]['rpy']['line_total'],reverse=True)
        line_count = dict_list[0][1]['rpy']['line_total']
        name =  dict_list[0][0]
        return f'longest animation by line count : {name}:{line_count}'
    
    def print_longest_anim_duration(self):
        dict_list = list(self.img_seqs.items())
        dict_list = sorted(dict_list,key=lambda x:x[1]['duration'],reverse=True)
        duration = dict_list[0][1]['duration']
        name =  dict_list[0][0]
        return f'longest animation by duration : {name}:{duration:.1f} seconds'

    def print_anims_without_issues(self):
        no_issues_str = ', '.join(self.return_zero_tag_items())
        return 'Animations without issues\r' + no_issues_str  
    
    
if __name__ == '__main__':
    anim_report = Animation_report()
    anim_report.run_reports()

    # print(animation_report.img_seqs)