from typing import Tuple
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
        # self.sprites[self.state+str(self.direct)][self.animation_frame].composite_draw(0, 'c' , x, Screen_size[1] - y + 1, w, h)
        self.sprites[self.state+str(self.direct)][self.animation_frame].draw_to_origin( x, y,w*s_size,h*s_size)
        # if self.state == 'ATTACK':
            # print('player : '+str(x)+' '+str(y))
        pass

    def set_direct(self, _direct):
        self.direct = directs[_direct]

        
        


class player(object):

    flag_move = False
    Roll_count = 0
    Atk_count = 0
    AtK_stack = 0
    equiped_weapon = 0
    previous_state = []
    shild_count = 0
    previous_state_count = 0
    Holding_direct = directs['down']
    Holded_flag = False
    move_trigger = [False, False, False, False]
    correction_place = list()
    correction_place.append(
                    [(-2, 9),(-5, -7),(-12, -2),(-12, 9),(24, 26),(-11, -3),(-11, -5),(-11, 8),(-2, 21),(-4, -7),(-11, -2),(-11, 9),(23, 24),(23, 23),(22, 23),(23, 23),(23, 23),
                    ])
    correction_place.append(
                    [(22, 5),(8, 4),(-3, 6),(-7, 9),(-7, 17),(5, 5),(23, 2),(22, 0),(24, 8),(-1, 5),(-8, 6),(-13, 6),(-15, 9),(-10, 10),(-9, 10),(-9, 10),(-9, 10),
                    ])
    correction_place.append(
                    [(21, 14),(-12, 18),(-13, 1),(-13, -2),(0,0),(-9,8),(-12, 11),(-12, 8),(28, 5),(-12, 12),(-14, -2),(-16, -6),(-17, -8),(-16, -6),(-11, -2),(-11, -2),(-12, -2),
                    ])
    correction_place.append(
                    [(0, 5),(-19, 5),(-15, 6),(-9, 0),(20, 17),(-11, 5),(-11, 2),(-8, 0),(0, 8),(-15, 5),(-11, 5),(-7, 6),(27, 8),(25, 10),(25, 10),(25, 10),(25, 10),
                    ])

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

        for i in range(0, 6):
            self.sprites[states['SSHIELD']+str(directs['down'])].append(load_image('sprite\will_shield deffense down_0'+str(i)+'.png'))
            self.sprites[states['SSHIELD']+str(directs['up'])].append(load_image('sprite\will_shield deffense up_0'+str(i)+'.png'))
            self.sprites[states['SSHIELD']+str(directs['left'])].append(load_image('sprite\will_shield deffense left_0'+str(i)+'.png'))
            self.sprites[states['SSHIELD']+str(directs['right'])].append(load_image('sprite\will_shield deffense right_0'+str(i)+'.png'))

        for i in range(0,8):
            self.sprites[states['SHEILDWALK']+str(directs['down'])].append(load_image('sprite\will_shield deffense walk down_0'+str(i)+'.png'))
            self.sprites[states['SHEILDWALK']+str(directs['up'])].append(load_image('sprite\will_shield deffense walk up_0'+str(i)+'.png'))
            self.sprites[states['SHEILDWALK']+str(directs['left'])].append(load_image('sprite\will_shield deffense walk left_0'+str(i)+'.png'))
            self.sprites[states['SHEILDWALK']+str(directs['right'])].append(load_image('sprite\will_shield deffense walk right_0'+str(i)+'.png'))

        self.previous_state.append('IDLE')
        self.switch_state('IDLE')
        self.speed = 10
        self.locate = 300, 400

        

    def switch_state(self, _state):
        if len(self.previous_state) > 1:
            self.previous_state.pop(0)
        self.previous_state.append(_state)
        super().switch_state(_state)

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

    def S_attack(self):
        if self.state != 'SATTACK':
            if self.equiped_weapon == 0:
                self.Holding_direct = self.direct
                self.switch_state('SSHIELD')
                self.shild_count = 6*5
                self.update_sprite_speed = self.update_sprite_speed//2

    def shield_cycle(self):
        if self.state == 'SSHIELD':
            if self.equiped_weapon == 0:
                if self.shild_count > 0:
                    self.now_time = time()
                    if  self.now_time - self.Late_time > 1/6:
                        self.Late_time = self.now_time
                        self.animation_frame = (self.animation_frame+1) % self.Maximum_frame 
                else:
                    self.Holded_flag = True
                self.shild_count -= 1     

    def set_move_flag(self, _flag, _direct = None):
        # self.flag_move = _flag
        if _flag:
            self.switch_state('MOVE')
        else:
            flag_count = 0
            for i in self.move_trigger:
                if i == True: flag_count += 1
            if flag_count < 2:
                self.switch_state('IDLE')
            if _direct != None:
                self.set_moveTrigger(False, directs[_direct])
        print(self.state)

    def set_move_shield(self, _flag, _direct = None):
        if _flag:
            self.switch_state('SHEILDWALK')
        else:
            flag_count = 0
            for i in self.move_trigger:
                if i == True: flag_count += 1
            if flag_count < 2:
                self.switch_state('SSHIELD')
            if _direct != None:
                self.set_moveTrigger(False, directs[_direct])

    def attack(self):
        if self.AtK_stack == 3:
            self.move(0.15)
        else:
            self.move(0.3)
        if self.state != states['ATTACK']:
            print(self.previous_state)
            if self.previous_state[0] == 'ATTACK':
                self.AtK_stack += 1
            else:
                self.AtK_stack = 1
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

    def shield_move_cycle(self):
        self.now_time = time()
        if  self.now_time - self.Late_time > 1/6:
            self.Late_time = self.now_time
            self.animation_frame = (self.animation_frame+1) % self.Maximum_frame

    def sp_attack(self):
        pass

    def guard(self):
        pass

    def set_moveTrigger(self, _flag, _direct = None):
        if _direct != None:
            self.move_trigger[_direct] = _flag
        else:
            self.move_trigger[self.direct] = _flag
        
    def move_up(self):
        self.direct = self.direct if self.direct == directs['up'] else directs['up']
        self.set_moveTrigger(True)
        pass
    
    def move_down(self):
        self.direct = self.direct if self.direct == directs['down'] else directs['down']
        self.set_moveTrigger(True)
        pass

    def move_right(self):
        self.direct = self.direct if self.direct == directs['right'] else directs['right']
        self.set_moveTrigger(True)
        pass

    def move_left(self):
        self.direct = self.direct if self.direct == directs['left'] else directs['left']
        self.set_moveTrigger(True)
        pass

    def move(self, mag = 1):
        if mag == 0:
            mag = 1
        if self.state == 'SHEILDWALK':
            mag == 5
        x, y = self.locate
        dx, dy = 0, 0
        k_flag = False
        if self.move_trigger[0]:
            dy = 1  
            k_flag = True
        if self.move_trigger[1]:
            dx = 1
            k_flag = True
        if self.move_trigger[2]:
            dy = -1
            k_flag = True
        if self.move_trigger[3]:
            dx = -1
            k_flag = True
        if k_flag == False:
            if self.direct % 2 == 0:
                dy = 1-self.direct
            else:
                dx = 2-self.direct
        d_len = math.sqrt(dx**2+dy**2)
        dx, dy = dx/d_len*self.speed/mag, dy/d_len*self.speed/mag
        self.locate = x+dx, y+dy

    def update(self):
        if self.state == states['MOVE']:
            self.move()
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
        elif self.state == 'SSHIELD':
            if self.equiped_weapon == 0:
                self.shield_cycle()
        elif self.state == 'SHEILDWALK' and self.Holded_flag:
            self.shield_move_cycle()
            self.move(5)
        # super().update()


    def rendering(self):
        if self.state == 'SSHIELD' or self.state == 'SHEILDWALK':
            x, y = self.locate
            w, h = self.sprites[self.state+str(self.Holding_direct)][self.animation_frame].w, self.sprites[self.state+str(self.Holding_direct)][self.animation_frame].h
            self.sprites[self.state+str(self.Holding_direct)][self.animation_frame].draw_to_origin( x, y,w*s_size,h*s_size)
        else:
            super().rendering()
        if self.state == 'ATTACK':
            x, y = self.locate
            # y = Screen_size[1] - y + 1
            w, h = self.sprites[self.state+str(self.direct)][self.animation_frame].w, self.sprites[self.state+str(self.direct)][self.animation_frame].h
            # print('playersize'+str(w)+' '+str(h))
            # if self.direct == 0:
            #     x, y = x + w/2, y + h/2  
            # elif self.direct == 1:
            #     x, y = x + w/2, y - h 
            # elif self.direct == 2:
            #     x, y = x , y  
            # elif self.direct == 3:
            #     x, y = x - w, y - h  
            # self.sprites[self.state+str(self.direct)][self.animation_frame].
            if self.equiped_weapon == 0:
                temp = 0
                if self.animation_frame < 17:
                    if self.animation_frame >= 14:
                        x, y = x + self.correction_place[self.direct][self.animation_frame-1][0]*s_size, y - self.correction_place[self.direct][self.animation_frame-1][1]*s_size
                        temp = -1
                    else:
                        x, y = x + self.correction_place[self.direct][self.animation_frame][0]*s_size, y - self.correction_place[self.direct][self.animation_frame][1]*s_size
                        temp = 0
                    
                    w_w, w_h = self.sprites['SSWORD'+str(self.direct)][self.animation_frame+temp].w, self.sprites['SSWORD'+str(self.direct)][self.animation_frame+temp].h
                    x, y = x, y + h*s_size - w_h*s_size
                    # print('sword : '+str(x)+' '+str(y))
                    # self.sprites['SSWORD'+str(self.direct)][self.animation_frame+temp].composite_draw(0, 'c' , x, Screen_size[1] - y + 1, w, h)
                    self.sprites['SSWORD'+str(self.direct)][self.animation_frame+temp].draw_to_origin(x, y,w_w*s_size,w_h*s_size)
            
