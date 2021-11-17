from modules import *

class Object:
    locate = [0, 0]
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

    def update(self, deltatime):
        pass

    def rendering(self):
        pass

    def handle_event(self, event):
        pass

    def set_direct(self, _direct):
        self.direct = _direct

    def get_direct(self):
        return self.direct

    def get_locate(self):
        return self.locate

    def get_rect(self):
        return self.locate[0], self.locate[1], self.locate[0] + self.rect_size[0], self.locate[1] + self.rect_size[1]

    def myclamp(self):
        self.locate[0] = clamp(0, self.locate[0], Screen_size[0] - 40)
        self.locate[1] = clamp(0, self.locate[1], Screen_size[1] - 40)
        return self.locate

    def collision(self):
        pass