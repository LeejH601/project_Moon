from math import dist, sqrt
from Object import *
import Player

type_of_monster = {'baby_slime' : 0, 'gollem_knight': 1}

class Monster(Object):
    type = None

    def __init__(self, _health, _speed, _type):
        self.name = _type
        self.type = type_of_monster[_type]
        super().__init__(self.name, _health, _speed)
        if self.type == 0:
            
            for i in range(0+1,10):
                self.sprites[str(self.name)+states['ATTACK']+str(directs['down'])].append(load_image('sprite\monster\BabySlime_Attack_Down_'+str(i)+'.png'))
                self.sprites[str(self.name)+states['ATTACK']+str(directs['up'])].append(load_image('sprite\monster\BabySlime_Attack_Up_'+str(i)+'.png'))
                self.sprites[str(self.name)+states['ATTACK']+str(directs['left'])].append(load_image('sprite\monster\BabySlime_Attack_Left_'+str(i)+'.png'))
                self.sprites[str(self.name)+states['ATTACK']+str(directs['right'])].append(load_image('sprite\monster\BabySlime_Attack_Right_'+str(i)+'.png'))
            self.sprites[str(self.name)+states['IDLE']+str(directs['down'])].append(load_image('sprite\monster\Babyslime_idle.png'))
            self.sprites[str(self.name)+states['IDLE']+str(directs['up'])].append(load_image('sprite\monster\Babyslime_idle.png'))
            self.sprites[str(self.name)+states['IDLE']+str(directs['left'])].append(load_image('sprite\monster\Babyslime_idle.png'))
            self.sprites[str(self.name)+states['IDLE']+str(directs['right'])].append(load_image('sprite\monster\Babyslime_idle.png'))
            for i in range(0+1,6):
                self.sprites[str(self.name)+states['MOVE']+str(directs['down'])].append(load_image('sprite\monster\Babyslime_walk_'+str(i)+'.png'))
                self.sprites[str(self.name)+states['MOVE']+str(directs['up'])].append(load_image('sprite\monster\Babyslime_walk_'+str(i)+'.png'))
                self.sprites[str(self.name)+states['MOVE']+str(directs['left'])].append(load_image('sprite\monster\Babyslime_walk_'+str(i)+'.png'))
                self.sprites[str(self.name)+states['MOVE']+str(directs['right'])].append(load_image('sprite\monster\Babyslime_walk_'+str(i)+'.png'))
            pass
        elif self.type == 1:
            pass

        self.switch_state('IDLE')
        self.speed = 5
        self.locate = 300, 400
        self.direct = directs['down']

    def chase_state(self):
        _player = Player.player._instance
        px, py = _player.Get_Locate()
        x, y = self.locate
        dx, dy = px - x, py - y
        distance = dx**2 + dy**2
        if sqrt(distance) < 30:
            self.switch_state('ATTACK')
        else :
            self.switch_state('MOVE')
        pass

    def rendering(self):
        print(self.animation_frame)
        return super().rendering()

    def update(self):
        self.chase_state()
        if self.state == 'MOVE':
            self.move()
        return super().update()

    def move(self):
        x, y = self.locate
        _player = Player.player._instance
        px,py = _player.Get_Locate()
        dx,dy = px - x, py - y
        d_size = math.sqrt(px ** 2 + py**2)
        dx, dy = dx/d_size, dy/d_size
        if abs(dx) > abs(dy):
            if dx > 0: self.direct = 1
            else : self.direct = 3
        else :
            if dy > 0: self.direct = 0
            else : self.direct = 2
            pass
        x, y = x + dx*self.speed, y + dy*self.speed

        if self.check_place(x, y):
            self.locate = x, y
        pass