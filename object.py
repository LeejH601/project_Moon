from modules import *

class Object:
    locate = [0, 0]
    health = 0
    speed = 0
    direct = [0, 0]
    rect_size = [0, 0]
    
    

    

    def __init__(self, _x, _y, _health, _speed):
        self.locate = [_x, _y]
        self.health = _health
        self.speed = _speed
        self.direct = [0,0]

    def update(self):
        pass

    def rendering(self):
        pass

    def handle_event(self, event):
        pass

    def set_direct(self, _direct):
        pass

    def get_direct(self):
        pass

    def myclamp(self):
        self.locate[0] = clamp(0, self.locate[0], Screen_size[0] - 40)
        self.locate[1] = clamp(0, self.locate[1], Screen_size[1] - 40)
        return self.locate

    def collision(self):
        pass