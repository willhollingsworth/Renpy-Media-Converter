from dataclasses import dataclass,field

@dataclass
class img_seqs:
    path:str = field(init=False)
    rpy_source:str = field(init=False)
    start_line:int = field(init=False)
    end_line:int = field(init=False)
    frame_rate:float = field(init=False)
    duration:float = field(init=False)
    sound_overrun:bool = field(init=False)
    img_count:int = field(init=False)
    imgs_ordered:bool = field(init=False)
    img_type:str = field(init=False)
    repeats:bool = field(init=False)