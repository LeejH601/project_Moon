from modules import *

class Object:
    name = None
    locate = [0, 0]
    Atk = 0
    health = 0
    speed = 0
    direct = [0, -1]
    previous_direct = [0, -1]
    rect_size = [0, 0]
    
    image = None
    frame = 0
    

    def __init__(self, _x, _y, _health, _speed, _direct = [0, -1]):
        self.locate = [_x, _y]
        self.health = _health
        self.speed = _speed
        self.direct = _direct
        self.frame = 0
        self.previous_direct = _direct
        

    def update(self, deltatime):
        pass

    def rendering(self):
        pass

    def handle_event(self, event):
        pass

    def set_name(self, _name):
        self.name = _name

    def get_name(self):
        return self.name

    def set_direct(self, _direct):
        self.direct = _direct

    def get_direct(self):
        return self.direct

    def get_locate(self):
        return self.locate

    def get_rect(self):
        return self.locate[0], self.locate[1], self.locate[0] + self.rect_size[0], self.locate[1] + self.rect_size[1]

    def set_atk(self, _atk):
        self.Atk = _atk

    def hit(self, demage):
        self.health -= demage

    def myclamp(self):
        self.locate[0] = clamp(0, self.locate[0], Screen_size[0] - 40)
        self.locate[1] = clamp(0, self.locate[1], Screen_size[1] - 40)
        return self.locate

    def Set_rectSize(self, w, h):
        self.rect_size = [w, h]

    def collision(self):
        pass
