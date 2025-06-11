
if __name__ == '__main__':
    ''' fix for running a module as a script, '''
    import sys
    from os.path import dirname as up
    p_dir = up(up(up(__file__)))
    print(p_dir)
    sys.path.append(p_dir) 



class Categorizer():
    def __init__(self,anim):
        #  self.img_seqs = read_write.read_img_seqs_file()
        self.anim = anim

        # def 
    def build_tags(self):
                self.anim['tags'] = []
                minimum_image_count = 3

                if isinstance(self.anim['frame_rate'],list):
                    #multi frame rate
                    # logging.info(f'{target} has differing pause amounts')
                    self.anim['tags'].append('bad frame rate')
                if not self.anim['frame_rate']:
                    # logging.info(f'{target} is missing framerate')
                    self.anim['tags'].append('no frame rate')
                if self.anim['img count'] < minimum_image_count:
                    # logging.info(f'{target} only has {self.anim["img count"]} images')
                    self.anim['tags'].append('too few images')
                if not self.anim['imgs ordered']:
                    # logging.info(f'{target} has unordered images files')
                    self.anim['tags'].append('images not ordered')
                if self.anim['sound overrun'] > 0:
                    # logging.info(f'{target} has sound overrun')
                    self.anim['tags'].append('sound overrun')
                if not self.anim['img type'] == 'jpg':
                    # logging.info(f'{target} has img type {self.anim["img type"]}')
                    self.anim['tags'].append(f'wrong img format :{self.anim["img type"]}')
                if self.anim['repeat'] == False:
                    # logging.info(f'{target} does not repeat')
                    self.anim['tags'].append(f'doesn\'t repeat')
                # check for alphas

    
if __name__ == '__main__':
    from renpy_media_converter.utils import read_write
    img_seq = read_write.read_img_seqs_file()
    first_anim = img_seq[list(img_seq.keys())[0]]
    categorizer = Categorizer(first_anim)
    categorizer.build_tags()
    print(categorizer.anim)



