from typing import Tuple
from modules import *

class Object:
    name = None
    sprites = defaultdict(list)
    locate = x, y = 0, 0
    Health = 0
    Speed = 0
    state = states['NONE']
    animation_frame = 0
    Maximum_frame = 0
    frame_update_count = 0
    direct = directs['down']
    sprite_size = (0, 0)
    flag_invincibility = False
    state_buffer = str()
    update_sprite_speed = 10
    Late_time = 0
    now_time = time()
    def __init__(self, name, _health, _speed):
        self.name = name
        self.Health = _health
        self.Speed = _speed
    
    def switch_state(self, _state):
        if self.state != states[_state]:
            self.state_buffer = self.state
            self.state = states[_state]
            self.set_sprite()

    def set_sprite(self):
        # if self.name == 'baby_slime' and self.state == 'ATTACK' :
        #     print(0)
        self.animation_frame = 0
        self.Maximum_frame = len(self.sprites[str(self.name)+self.state+str(self.direct)])

    def update(self):
        if self.Maximum_frame != 0:
            self.now_time = time()
            if self.now_time - self.Late_time > 1/6:
                self.animation_frame = (self.animation_frame+1) % self.Maximum_frame
                self.Late_time = self.now_time
            # self.frame_update_count = (self.frame_update_count+1) % self.update_sprite_speed
            # if self.frame_update_count == 0:
            #     self.animation_frame = (self.animation_frame+1) % self.Maximum_frame
        pass

    def rendering(self):
        x, y = self.locate
        # self.sprites[self.state+str(self.direct)][self.animation_frame].
        w, h = self.sprites[str(self.name)+self.state+str(self.direct)][self.animation_frame].w, self.sprites[str(self.name)+self.state+str(self.direct)][self.animation_frame].h
        # self.sprites[self.state+str(self.direct)][self.animation_frame].composite_draw(0, 'c' , x, Screen_size[1] - y + 1, w, h)
        self.sprites[str(self.name)+self.state+str(self.direct)][self.animation_frame].draw_to_origin( x, y,w*s_size,h*s_size)
        # if self.state == 'ATTACK':
            # print('player : '+str(x)+' '+str(y))
        pass

    def set_direct(self, _direct):
        self.direct = directs[_direct]

    def Get_Locate(self):
        return self.locate
        
    def check_place(self,_x,_y):
        if _x > 0 and _x < Screen_size[0]:
            if _y > 0 and _y < Screen_size[1]:
                return True
        return False


