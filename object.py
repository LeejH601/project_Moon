from modules import *

class object:
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
        self.state_buffer = self.state
        self.state = states[_state]
        self.set_sprite()

    def set_sprite(self):
        self.animation_frame = 0
        self.Maximum_frame = len(self.sprites[self.state+str(self.direct)])

    def update(self):
        if self.Maximum_frame != 0:
            self.frame_update_count = (self.frame_update_count+1) % self.update_sprite_speed
            if self.frame_update_count == 0:
                self.animation_frame = (self.animation_frame+1) % self.Maximum_frame
        pass

    def rendering(self):
        x, y = self.locate
        # self.sprites[self.state+str(self.direct)][self.animation_frame].
        w, h = self.sprites[self.state+str(self.direct)][self.animation_frame].w, self.sprites[self.state+str(self.direct)][self.animation_frame].h
        self.sprites[self.state+str(self.direct)][self.animation_frame].composite_draw(0, 'c' , x, y, w*4, h*4)
        pass

    def set_direct(self, _direct):
        self.direct = directs[_direct]

        
        


class player(object):

    flag_move = False
    Roll_count = 0
    Atk_count = 0
    AtK_stack = 0
    equiped_weapon = 0

    def __init__(self, name, _health, _speed):
        super().__init__(name, _health, _speed)
        for i in range(0+1,10):
            self.sprites[states['IDLE']+str(directs['down'])].append(load_image('sprite\Will_Idle_Down_'+str(i)+'.png'))
            self.sprites[states['IDLE']+str(directs['up'])].append(load_image('sprite\Will_Idle_Up_'+str(i)+'.png'))
            self.sprites[states['IDLE']+str(directs['left'])].append(load_image('sprite\Will_Idle_Left_'+str(i)+'.png'))
            self.sprites[states['IDLE']+str(directs['right'])].append(load_image('sprite\Will_Idle_Right_'+str(i)+'.png'))
        for i in range(0+1,9):
            self.sprites[states['MOVE']+str(directs['down'])].append(load_image('sprite\will animation cycle front dungeon_0'+str(i)+'.png'))
            self.sprites[states['MOVE']+str(directs['up'])].append(load_image('sprite\will walking cycle back_0'+str(i)+'.png'))
            self.sprites[states['MOVE']+str(directs['left'])].append(load_image('sprite\will_walking cycle_left side0'+str(i)+'.png'))
            self.sprites[states['MOVE']+str(directs['right'])].append(load_image('sprite\will_walking cycle_right side0'+str(i)+'.png'))

            self.sprites[states['ROLL']+str(directs['down'])].append(load_image('sprite\Will_Roll_Down_'+str(i)+'.png'))
            self.sprites[states['ROLL']+str(directs['up'])].append(load_image('sprite\Will_Roll_Up_'+str(i)+'.png'))
            self.sprites[states['ROLL']+str(directs['left'])].append(load_image('sprite\Will_Roll_Left_'+str(i)+'.png'))
            self.sprites[states['ROLL']+str(directs['right'])].append(load_image('sprite\Will_Roll_Right_'+str(i)+'.png'))

        for i in range(0+1,19):
            self.sprites[states['ATTACK']+str(directs['down'])].append(load_image('sprite\Will_ShortSwordCombo_Animation_Down_'+str(i)+'.png'))
            self.sprites[states['ATTACK']+str(directs['up'])].append(load_image('sprite\Will_ShortSwordCombo_Animation_Up_'+str(i)+'.png'))
            self.sprites[states['ATTACK']+str(directs['left'])].append(load_image('sprite\Will_ShortSwordCombo_Animation_Left_'+str(i)+'.png'))
            self.sprites[states['ATTACK']+str(directs['right'])].append(load_image('sprite\Will_ShortSwordCombo_Animation_Right_'+str(i)+'.png'))

        for i in range(0+1,18):
            if i != 15:
                self.sprites[states['SSWORD']+str(directs['down'])].append(load_image('sprite\SoldierShortSwordCombo_Main_Down_'+str(i)+'.png'))
                self.sprites[states['SSWORD']+str(directs['up'])].append(load_image('sprite\SoldierShortSwordCombo_Main_Up_'+str(i)+'.png'))
                self.sprites[states['SSWORD']+str(directs['left'])].append(load_image('sprite\SoldierShortSwordCombo_Main_Left_'+str(i)+'.png'))
                self.sprites[states['SSWORD']+str(directs['right'])].append(load_image('sprite\SoldierShortSwordCombo_Main_Right_'+str(i)+'.png'))

        self.switch_state('IDLE')
        self.speed = 10
        self.locate = 300, 400

    def get_state(self):
        return self.state

    def set_Roll(self):
        if self.state != 'ROLL':
            self.switch_state('ROLL')
            self.Roll_count = 5*7
            self.update_sprite_speed = self.update_sprite_speed//2

    def Roll_cycle(self):
        if self.state == 'ROLL':
            # print(self.Roll_count)
            x, y = self.locate
            if self.direct == 0:
                y += self.speed*1.2  
            elif self.direct == 1:
                x += self.speed*1.2 
            elif self.direct == 2:
                y -= self.speed*1.2 
            elif self.direct == 3:
                x -= self.speed*1.2
            self.locate = x, y
            self.now_time = time()
            if  self.now_time - self.Late_time > 1/12:
                self.Late_time = self.now_time
                self.animation_frame = (self.animation_frame+1) % self.Maximum_frame
            self.flag_invincibility = True if self.Roll_count > 20 else False
            self.Roll_count -= 1
            pass

    def set_move_flag(self, _flag):
        # self.flag_move = _flag
        if _flag:
            self.switch_state('MOVE')
        else:
            self.switch_state('IDLE')
        print(self.state)

    def attack(self):
        if self.state != states['ATTACK']:
            self.switch_state('ATTACK')
            if self.AtK_stack == 1 or self.AtK_stack > 3:
                self.AtK_stack = 1
                self.Atk_count = 5*10-8
            elif self.AtK_stack == 2:
                self.Atk_count = 4*10
                self.animation_frame += 5
                pass
            elif self.AtK_stack == 3:
                self.Atk_count = 9*10
                self.animation_frame += 9
                pass
            self.AtK_stack += 1

        pass

    def attack_cycle(self):
        if self.state == states['ATTACK']:
            self.now_time = time()
            if  self.now_time - self.Late_time > 1/6:
                self.Late_time = self.now_time
                self.animation_frame = (self.animation_frame+1) % self.Maximum_frame
            self.Atk_count -= 1
            pass

    def normal_cycle(self):
        self.now_time = time()
        if  self.now_time - self.Late_time > 1/6:
            self.Late_time = self.now_time
            self.animation_frame = (self.animation_frame+1) % self.Maximum_frame


    def sp_attack(self):
        pass

    def guard(self):
        pass
        
    def move_up(self):
        self.direct = self.direct if self.direct == directs['up'] else directs['up']
        pass
    
    def move_down(self):
        self.direct = self.direct if self.direct == directs['down'] else directs['down']
        pass

    def move_right(self):
        self.direct = self.direct if self.direct == directs['right'] else directs['right']
        pass

    def move_left(self):
        self.direct = self.direct if self.direct == directs['left'] else directs['left']
        pass

    def update(self):
        if self.state == states['MOVE']:
            x, y = self.locate
            if self.direct == 0:
                y += self.speed    
            elif self.direct == 1:
                x += self.speed
            elif self.direct == 2:
                y -= self.speed
            elif self.direct == 3:
                x -= self.speed
            self.locate = x, y
            self.normal_cycle()
        elif self.state == 'IDLE':
            self.normal_cycle()
        elif self.state == 'ROLL':
            if self.Roll_count <= 0:
                self.switch_state('IDLE')
                self.update_sprite_speed = 10
            else:
                self.Roll_cycle()
        elif self.state == 'ATTACK':
            if self.Atk_count <= 0:
                self.switch_state('IDLE')
                self.update_sprite_speed = 10
                pass
            else:
                self.attack_cycle()
        # super().update()


    def rendering(self):
        super().rendering()
        if self.state == 'ATTACK':
            x, y = self.locate
            w, h = self.sprites[self.state+str(self.direct)][self.animation_frame].w, self.sprites[self.state+str(self.direct)][self.animation_frame].h
            if self.direct == 0:
                x, y = x + w/2, y + h/2  
            elif self.direct == 1:
                x, y = x + w/2, y - h 
            elif self.direct == 2:
                x, y = x , y  
            elif self.direct == 3:
                x, y = x - w, y - h  
            # self.sprites[self.state+str(self.direct)][self.animation_frame].
            if self.equiped_weapon == 0:
                temp = 0
                if self.AtK_stack == 4:
                    if self.animation_frame >=17:
                        temp = -2
                    elif self.animation_frame >= 16:
                        temp = -1
                else:
                    temp = 0
                w, h = self.sprites['SSWORD'+str(self.direct)][self.animation_frame+temp].w, self.sprites['SSWORD'+str(self.direct)][self.animation_frame+temp].h
                self.sprites['SSWORD'+str(self.direct)][self.animation_frame+temp].composite_draw(0, 'c' , x, y, w*4, h*4)
            