from math import dist, sqrt
from object import *


monster_status_table = {'slime': [50, 5], 'gollem': [100, 10]}

class Monster(Object):

    RUN_SPEED_KMPH = 1.0
    RUN_SPEED_MPM = 0
    RUN_SPEED_MPS = 0
    RUN_SPEED_PPS = 0

    cur_state = None

    vector = None

    my_event_list = {'faraway': 0, 'near': 1, 'detect': 2, 'hit': 3, 'hitTimer': 4}
    my_state_table = None
    my_next_state_table = None

    def Set_Speed(self, _speed = 1):
        self.RUN_SPEED_KMPH = _speed
        self.RUN_SPEED_MPM = (self.RUN_SPEED_KMPH * 1000.0 / 60.0)
        self.RUN_SPEED_MPS = (self.RUN_SPEED_MPM / 60.0)
        self.RUN_SPEED_PPS = (self.RUN_SPEED_MPS * PIXEL_PER_METER)

    def __init__(self, _x, _y, _health, _speed, _direct=[0, -1]):
        super().__init__(_x, _y, _health, _speed, _direct)
        self.Set_Speed(_speed)
        self.set_name('monster')
        self.event_que = []

    def rendering(self):
        self.cur_state.draw(self)
        draw_rectangle(*self.get_rect())

    def update(self, deltatime):
        if self.health <= 0.0:
            game_world.remove_object(self)
        self.cur_state.do(self, deltatime)
        if len(self.event_que) > 0:
            event = self.event_que.pop()
            if event == 3:
                print('여기')
            if event in self.my_next_state_table[self.cur_state]:
                self.cur_state.exit(self, event)
                self.cur_state = self.my_next_state_table[self.cur_state][event]
                self.cur_state.enter(self, event)
    
    def handle_event(self, event):
        if event in self.my_state_table:
            self.add_event(event)

    def add_event(self, event):
        self.event_que.insert(0, event)

    def Set_my_event_list(self, _list):
        self.my_event_list = _list

    def Set_state_table(self, _table):
        self.my_state_table = _table

    def Set_next_state_table(self, _table):
        self.my_next_state_table = _table

    def Get_event_list(self):
        pass

    def Set_cur_state(self, state):
        self.cur_state = state

    def collider(self, my_rect, b):
        left_a, bottom_a, right_a, top_a = my_rect
        left_b, bottom_b, right_b, top_b = b.get_rect()

        if left_a > right_b: return False
        if right_a < left_b: return False
        if top_a < bottom_b: return False
        if bottom_a > top_b: return False
    
        return True

    def hit(self, demage):
        return super().hit(demage)

    pass

class SmallSlime(Monster):

    class IdleState:

        image = None

        TIME_PER_ACTION = 1.0
        ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
        FRAMES_PER_ACTION = 1

        def __init__(self):
            SmallSlime.IdleState.__instance = self
            if SmallSlime.IdleState.image == None:
                SmallSlime.IdleState.image = defaultdict(list)
                SmallSlime.IdleState.image[-1].append(load_image('sprite\monster\Babyslime_idle.png'))
                SmallSlime.IdleState.image[1].append(load_image('sprite\monster\Babyslime_idle.png'))
                SmallSlime.IdleState.image[-10].append(load_image('sprite\monster\Babyslime_idle.png'))
                SmallSlime.IdleState.image[10].append(load_image('sprite\monster\Babyslime_idle.png'))
                SmallSlime.IdleState.image[0] = SmallSlime.IdleState.image[-1]
            

        def enter(babeslime, event):
            babeslime.frame = 0
            babeslime.IdleState.image[0] = babeslime.IdleState.image[babeslime.previous_direct[0]*10+babeslime.previous_direct[1]]
            babeslime.previous_direct = babeslime.direct
                
            babeslime.direct[0] = clamp(-1, babeslime.direct[0], 1)
            babeslime.direct[1] = clamp(-1, babeslime.direct[1], 1)
        

        def exit(babeslime, event):
            pass

        def do(babeslime, deltatime):
            babeslime.frame = (babeslime.frame + babeslime.IdleState.FRAMES_PER_ACTION * babeslime.IdleState.ACTION_PER_TIME * deltatime) % babeslime.IdleState.FRAMES_PER_ACTION
            left_a, bottom_a, right_a, top_a = babeslime.get_rect()
            my_rect = (left_a - 200, bottom_a - 200, right_a + 200, top_a + 200)
            if babeslime.collider(my_rect, game_world.get_player_instacne()):
                if babeslime.atk_delay < 0.0:
                    babeslime.add_event(2)

        def draw(babeslime):
            if babeslime.direct[0]*10+babeslime.direct[1]:
                babeslime.IdleState.image[babeslime.direct[0]*10+babeslime.direct[1]][int(babeslime.frame)].draw_to_origin(babeslime.locate[0], babeslime.locate[1], babeslime.rect_size[0], babeslime.rect_size[1])
            else:
                babeslime.IdleState.image[babeslime.previous_direct[0]*10+babeslime.previous_direct[1]][int(babeslime.frame)].draw_to_origin(babeslime.locate[0], babeslime.locate[1], babeslime.rect_size[0], babeslime.rect_size[1])


    class AttackState:

        image = None

        TIME_PER_ACTION = 1
        ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
        FRAMES_PER_ACTION = 9

        def __init__(self):
            SmallSlime.AttackState.__instance = self
            if SmallSlime.AttackState.image == None:
                SmallSlime.AttackState.image = defaultdict(list)
                for i in range(0+1, 10):
                    SmallSlime.AttackState.image[-1].append(load_image('sprite\monster\BabySlime_Attack_Down_'+str(i)+'.png'))
                    SmallSlime.AttackState.image[1].append(load_image('sprite\monster\BabySlime_Attack_Up_'+str(i)+'.png'))
                    SmallSlime.AttackState.image[-10].append(load_image('sprite\monster\BabySlime_Attack_Left_'+str(i)+'.png'))
                    SmallSlime.AttackState.image[10].append(load_image('sprite\monster\BabySlime_Attack_Right_'+str(i)+'.png'))
                    SmallSlime.AttackState.image[0] = SmallSlime.AttackState.image[-1]

                
            

        def enter(bbslime, event):
            bbslime.frame = 0
            bbslime.AttackState.image[0] = bbslime.AttackState.image[bbslime.previous_direct[0]*10+bbslime.previous_direct[1]]
            bbslime.previous_direct = bbslime.direct
                
            bbslime.direct[0] = clamp(-1, bbslime.direct[0], 1)
            bbslime.direct[1] = clamp(-1, bbslime.direct[1], 1)
        

        def exit(bbslime, event):
            bbslime.atk_delay = 5.0
            pass

        def do(bbslime, deltatime):

            if bbslime.frame > bbslime.AttackState.FRAMES_PER_ACTION - 0.5:
                bbslime.add_event(0)

            bbslime.frame = (bbslime.frame + bbslime.AttackState.FRAMES_PER_ACTION * bbslime.AttackState.ACTION_PER_TIME * deltatime) % bbslime.AttackState.FRAMES_PER_ACTION


            # left_a, bottom_a, right_a, top_a = gollem.get_rect()
            # my_rect = (left_a - 50, bottom_a - 50, right_a + 50, top_a + 50)
            # if gollem.collider(my_rect, Player._instance):
            #     gollem.add_event(1)


        def draw(bbslime):
            w, h = bbslime.AttackState.image[bbslime.direct[0]*10+bbslime.direct[1]][int(bbslime.frame)].w, bbslime.AttackState.image[bbslime.direct[0]*10+bbslime.direct[1]][int(bbslime.frame)].h
            if bbslime.direct[0]*10+bbslime.direct[1]:
                bbslime.AttackState.image[bbslime.direct[0]*10+bbslime.direct[1]][int(bbslime.frame)].draw_to_origin(bbslime.locate[0], bbslime.locate[1], w*s_size, h*s_size)
            else:
                bbslime.AttackState.image[bbslime.previous_direct[0]*10+bbslime.previous_direct[1]][int(bbslime.frame)].draw_to_origin(bbslime.locate[0], bbslime.locate[1], w*s_size, h*s_size)


    class RunState:
        pass


    class ChaseState:

        image = None

        TIME_PER_ACTION = 1.0
        ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
        FRAMES_PER_ACTION = 5

        def __init__(self):
            SmallSlime.ChaseState.__instance = self
            if SmallSlime.ChaseState.image == None:
                SmallSlime.ChaseState.image = defaultdict(list)
                for i in range(0+1, 6):
                    SmallSlime.ChaseState.image[-1].append(load_image('sprite\monster\Babyslime_walk_'+str(i)+'.png'))
                    SmallSlime.ChaseState.image[1].append(load_image('sprite\monster\Babyslime_walk_'+str(i)+'.png'))
                    SmallSlime.ChaseState.image[-10].append(load_image('sprite\monster\Babyslime_walk_'+str(i)+'.png'))
                    SmallSlime.ChaseState.image[10].append(load_image('sprite\monster\Babyslime_walk_'+str(i)+'.png'))
                    SmallSlime.ChaseState.image[0] = SmallSlime.ChaseState.image[-1]
            

        def enter(bbslime, event):
            bbslime.frame = 0
            bbslime.ChaseState.image[0] = bbslime.ChaseState.image[bbslime.previous_direct[0]*10+bbslime.previous_direct[1]]
            bbslime.previous_direct = bbslime.direct
                
            bbslime.direct[0] = clamp(-1, bbslime.direct[0], 1)
            bbslime.direct[1] = clamp(-1, bbslime.direct[1], 1)
        

        def exit(bbslime, event):
            pass

        def do(bbslime, deltatime):
            bbslime.frame = (bbslime.frame + bbslime.ChaseState.FRAMES_PER_ACTION * bbslime.ChaseState.ACTION_PER_TIME * deltatime) % bbslime.ChaseState.FRAMES_PER_ACTION

            vector = [game_world.get_player_instacne().locate[0] - bbslime.locate[0], game_world.get_player_instacne().locate[1] - bbslime.locate[1]]
            weight = sqrt(vector[0]**2 + vector[1]**2)
            vector = [vector[0]/ weight * bbslime.RUN_SPEED_PPS, vector[1]/ weight * bbslime.RUN_SPEED_PPS]

            bbslime.locate[0] += vector[0] * deltatime
            bbslime.locate[1] += vector[1] * deltatime

            if abs(vector[0]) > abs(vector[1]):
                if vector[0] > 0: bbslime.direct = [1, 0]
                else : bbslime.direct = [-1, 0]
            else :
                if vector[1] > 0: bbslime.direct = [0, 1]
                else : bbslime.direct = [0, -1]

            left_a, bottom_a, right_a, top_a = bbslime.get_rect()
            my_rect = (left_a - 30, bottom_a - 30, right_a + 30, top_a + 30)
            if bbslime.collider(my_rect, game_world.get_player_instacne()) and bbslime.atk_delay <= 0.0:
                bbslime.add_event(1)


        def draw(bbslime):
            w, h = bbslime.ChaseState.image[bbslime.direct[0]*10+bbslime.direct[1]][int(bbslime.frame)].w, bbslime.ChaseState.image[bbslime.direct[0]*10+bbslime.direct[1]][int(bbslime.frame)].h
            if bbslime.direct[0]*10+bbslime.direct[1]:
                bbslime.ChaseState.image[bbslime.direct[0]*10+bbslime.direct[1]][int(bbslime.frame)].draw_to_origin(bbslime.locate[0], bbslime.locate[1],w*s_size, h*s_size)
            else:
                bbslime.ChaseState.image[bbslime.previous_direct[0]*10+bbslime.previous_direct[1]][int(bbslime.frame)].draw_to_origin(bbslime.locate[0], bbslime.locate[1], w*s_size, h*s_size)


    class HitState:

        image = None

        TIME_PER_ACTION = 1.0
        ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
        FRAMES_PER_ACTION = 1

        hit_timer = None
        knockback_trigger = False

        def __init__(self):
            SmallSlime.HitState.__instance = self
            if SmallSlime.HitState.image == None:
                SmallSlime.HitState.image = defaultdict(list)
                SmallSlime.HitState.image[-1].append(load_image('sprite\monster\Babyslime_idle.png'))
                SmallSlime.HitState.image[1].append(load_image('sprite\monster\Babyslime_idle.png'))
                SmallSlime.HitState.image[-10].append(load_image('sprite\monster\Babyslime_idle.png'))
                SmallSlime.HitState.image[10].append(load_image('sprite\monster\Babyslime_idle.png'))
                SmallSlime.HitState.image[0] = SmallSlime.HitState.image[-1]
            

        def enter(babeslime, event):
            print(babeslime)
            babeslime.frame = 0
            babeslime.HitState.image[0] = babeslime.HitState.image[babeslime.previous_direct[0]*10+babeslime.previous_direct[1]]
            babeslime.previous_direct = babeslime.direct
                
            babeslime.direct[0] = clamp(-1, babeslime.direct[0], 1)
            babeslime.direct[1] = clamp(-1, babeslime.direct[1], 1)

            babeslime.hit_timer = 1.0
            babeslime.knockback_trigger = False
            
            print('Enter HitState!!!!!!!!!!')
        

        def exit(babeslime, event):
            pass

        def do(babeslime, deltatime):
            babeslime.frame = (babeslime.frame + babeslime.HitState.FRAMES_PER_ACTION * babeslime.HitState.ACTION_PER_TIME * deltatime) % babeslime.HitState.FRAMES_PER_ACTION
            if babeslime.knockback_trigger == False:
                vector = [-babeslime.direct[0]*babeslime.RUN_SPEED_PPS, -babeslime.direct[1]*babeslime.RUN_SPEED_PPS]

                babeslime.locate[0] +=  vector[0]
                babeslime.locate[1] +=  vector[1]
                babeslime.knockback_trigger = True
            
            if babeslime.hit_timer <= 0.0:
                babeslime.add_event(4)
            babeslime.hit_timer -= game_framework.frame_time

        def draw(babeslime):
            if babeslime.direct[0]*10+babeslime.direct[1]:
                babeslime.HitState.image[babeslime.direct[0]*10+babeslime.direct[1]][int(babeslime.frame)].draw_to_origin(babeslime.locate[0], babeslime.locate[1], babeslime.rect_size[0], babeslime.rect_size[1])
            else:
                babeslime.HitState.image[babeslime.previous_direct[0]*10+babeslime.previous_direct[1]][int(babeslime.frame)].draw_to_origin(babeslime.locate[0], babeslime.locate[1], babeslime.rect_size[0], babeslime.rect_size[1])


    direct = None

    atk_delay = 0

    def __init__(self, _x, _y, _health, _speed, _direct=[0, -1]):
        super().__init__(_x, _y, _health, _speed, _direct)
        self.IdleState()
        self.AttackState()
        self.RunState()
        self.ChaseState()
        self.HitState()
        N_table = {
            self.IdleState : {self.my_event_list['faraway'] : self.IdleState, self.my_event_list['near'] : self.AttackState, self.my_event_list['detect'] : self.ChaseState, self.my_event_list['hit'] : self.HitState },
            self.RunState : {self.my_event_list['faraway'] : self.IdleState, self.my_event_list['near'] : self.AttackState, self.my_event_list['hit'] : self.HitState },
            self.AttackState : {self.my_event_list['faraway'] : self.IdleState, self.my_event_list['near'] : self.AttackState },
            self.ChaseState : {self.my_event_list['near'] : self.AttackState, self.my_event_list['faraway'] : self.IdleState, self.my_event_list['hit'] : self.HitState},
            self.HitState : {self.my_event_list['hitTimer'] : self.IdleState}
        }
        # self.my_state_table()
        self.direct = self.get_direct()
        self.Set_next_state_table(N_table)
        self.Set_rectSize(self.IdleState.image[-1][0].w*s_size, self.IdleState.image[-1][0].h*s_size)
        self.Set_cur_state(self.IdleState)
        self.cur_state.enter(self, None)
        

    def rendering(self):
        return super().rendering()

    def update(self, deltatime):
        self.atk_delay -= game_framework.frame_time
        return super().update(deltatime)

    def hit(self, demage):
        self.add_event(3)
        return super().hit(demage)

class BigSlime(Monster):

    class IdleState:

        image = None

        TIME_PER_ACTION = 1.0
        ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
        FRAMES_PER_ACTION = 1

        def __init__(self):
            BigSlime.IdleState.__instance = self
            if BigSlime.IdleState.image == None:
                BigSlime.IdleState.image = defaultdict(list)
                BigSlime.IdleState.image[-1].append(load_image('sprite\monster\slime_walk_1.png'))
                BigSlime.IdleState.image[1].append(load_image('sprite\monster\slime_walk_1.png'))
                BigSlime.IdleState.image[-10].append(load_image('sprite\monster\slime_walk_1.png'))
                BigSlime.IdleState.image[10].append(load_image('sprite\monster\slime_walk_1.png'))
                BigSlime.IdleState.image[0] = BigSlime.IdleState.image[-1]
            

        def enter(babeslime, event):
            babeslime.frame = 0
            babeslime.IdleState.image[0] = babeslime.IdleState.image[babeslime.previous_direct[0]*10+babeslime.previous_direct[1]]
            babeslime.previous_direct = babeslime.direct
                
            babeslime.direct[0] = clamp(-1, babeslime.direct[0], 1)
            babeslime.direct[1] = clamp(-1, babeslime.direct[1], 1)
        

        def exit(babeslime, event):
            pass

        def do(babeslime, deltatime):
            babeslime.frame = (babeslime.frame + babeslime.IdleState.FRAMES_PER_ACTION * babeslime.IdleState.ACTION_PER_TIME * deltatime) % babeslime.IdleState.FRAMES_PER_ACTION
            left_a, bottom_a, right_a, top_a = babeslime.get_rect()
            my_rect = (left_a - 200, bottom_a - 200, right_a + 200, top_a + 200)
            if babeslime.collider(my_rect, game_world.get_player_instacne()):
                if babeslime.atk_delay < 0.0:
                    babeslime.add_event(2)

        def draw(babeslime):
            if babeslime.direct[0]*10+babeslime.direct[1]:
                babeslime.IdleState.image[babeslime.direct[0]*10+babeslime.direct[1]][int(babeslime.frame)].draw_to_origin(babeslime.locate[0], babeslime.locate[1], babeslime.rect_size[0], babeslime.rect_size[1])
            else:
                babeslime.IdleState.image[babeslime.previous_direct[0]*10+babeslime.previous_direct[1]][int(babeslime.frame)].draw_to_origin(babeslime.locate[0], babeslime.locate[1], babeslime.rect_size[0], babeslime.rect_size[1])


    class AttackState:

        image = None

        TIME_PER_ACTION = 1.5
        ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
        FRAMES_PER_ACTION = 16

        def __init__(self):
            BigSlime.AttackState.__instance = self
            if BigSlime.AttackState.image == None:
                BigSlime.AttackState.image = defaultdict(list)
                for i in range(0+1, 17):
                    BigSlime.AttackState.image[-1].append(load_image('sprite\monster\slime_hit_attack_'+str(i)+'.png'))
                    BigSlime.AttackState.image[1].append(load_image('sprite\monster\slime_hit_attack_'+str(i)+'.png'))
                    BigSlime.AttackState.image[-10].append(load_image('sprite\monster\slime_hit_attack_'+str(i)+'.png'))
                    BigSlime.AttackState.image[10].append(load_image('sprite\monster\slime_hit_attack_'+str(i)+'.png'))
                    BigSlime.AttackState.image[0] = BigSlime.AttackState.image[-1]

                
            

        def enter(bbslime, event):
            bbslime.frame = 0
            bbslime.AttackState.image[0] = bbslime.AttackState.image[bbslime.previous_direct[0]*10+bbslime.previous_direct[1]]
            bbslime.previous_direct = bbslime.direct
                
            bbslime.direct[0] = clamp(-1, bbslime.direct[0], 1)
            bbslime.direct[1] = clamp(-1, bbslime.direct[1], 1)
        

        def exit(bbslime, event):
            bbslime.atk_delay = 5.0
            pass

        def do(bbslime, deltatime):

            if bbslime.frame > bbslime.AttackState.FRAMES_PER_ACTION - 0.5:
                bbslime.add_event(0)

            bbslime.frame = (bbslime.frame + bbslime.AttackState.FRAMES_PER_ACTION * bbslime.AttackState.ACTION_PER_TIME * deltatime) % bbslime.AttackState.FRAMES_PER_ACTION


            # left_a, bottom_a, right_a, top_a = gollem.get_rect()
            # my_rect = (left_a - 50, bottom_a - 50, right_a + 50, top_a + 50)
            # if gollem.collider(my_rect, Player._instance):
            #     gollem.add_event(1)


        def draw(bbslime):
            w, h = bbslime.AttackState.image[bbslime.direct[0]*10+bbslime.direct[1]][int(bbslime.frame)].w, bbslime.AttackState.image[bbslime.direct[0]*10+bbslime.direct[1]][int(bbslime.frame)].h
            if bbslime.direct[0]*10+bbslime.direct[1]:
                bbslime.AttackState.image[bbslime.direct[0]*10+bbslime.direct[1]][int(bbslime.frame)].draw_to_origin(bbslime.locate[0], bbslime.locate[1], w*s_size, h*s_size)
            else:
                bbslime.AttackState.image[bbslime.previous_direct[0]*10+bbslime.previous_direct[1]][int(bbslime.frame)].draw_to_origin(bbslime.locate[0], bbslime.locate[1], w*s_size, h*s_size)


    class RunState:
        pass


    class ChaseState:

        image = None

        TIME_PER_ACTION = 1.0
        ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
        FRAMES_PER_ACTION = 8

        def __init__(self):
            BigSlime.ChaseState.__instance = self
            if BigSlime.ChaseState.image == None:
                BigSlime.ChaseState.image = defaultdict(list)
                for i in range(0+1, 9):
                    BigSlime.ChaseState.image[-1].append(load_image('sprite\monster\slime_walk_'+str(i)+'.png'))
                    BigSlime.ChaseState.image[1].append(load_image('sprite\monster\slime_walk_'+str(i)+'.png'))
                    BigSlime.ChaseState.image[-10].append(load_image('sprite\monster\slime_walk_'+str(i)+'.png'))
                    BigSlime.ChaseState.image[10].append(load_image('sprite\monster\slime_walk_'+str(i)+'.png'))
                    BigSlime.ChaseState.image[0] = BigSlime.ChaseState.image[-1]
            

        def enter(bbslime, event):
            bbslime.frame = 0
            bbslime.ChaseState.image[0] = bbslime.ChaseState.image[bbslime.previous_direct[0]*10+bbslime.previous_direct[1]]
            bbslime.previous_direct = bbslime.direct
                
            bbslime.direct[0] = clamp(-1, bbslime.direct[0], 1)
            bbslime.direct[1] = clamp(-1, bbslime.direct[1], 1)
        

        def exit(bbslime, event):
            pass

        def do(bbslime, deltatime):
            bbslime.frame = (bbslime.frame + bbslime.ChaseState.FRAMES_PER_ACTION * bbslime.ChaseState.ACTION_PER_TIME * deltatime) % bbslime.ChaseState.FRAMES_PER_ACTION

            vector = [game_world.get_player_instacne().locate[0] - bbslime.locate[0], game_world.get_player_instacne().locate[1] - bbslime.locate[1]]
            weight = sqrt(vector[0]**2 + vector[1]**2)
            vector = [vector[0]/ weight * bbslime.RUN_SPEED_PPS, vector[1]/ weight * bbslime.RUN_SPEED_PPS]

            bbslime.locate[0] += vector[0] * deltatime
            bbslime.locate[1] += vector[1] * deltatime

            if abs(vector[0]) > abs(vector[1]):
                if vector[0] > 0: bbslime.direct = [1, 0]
                else : bbslime.direct = [-1, 0]
            else :
                if vector[1] > 0: bbslime.direct = [0, 1]
                else : bbslime.direct = [0, -1]

            left_a, bottom_a, right_a, top_a = bbslime.get_rect()
            my_rect = (left_a - 50, bottom_a - 50, right_a + 50, top_a + 50)
            if bbslime.collider(my_rect, game_world.get_player_instacne()) and bbslime.atk_delay <= 0.0:
                bbslime.add_event(1)


        def draw(bbslime):
            w, h = bbslime.ChaseState.image[bbslime.direct[0]*10+bbslime.direct[1]][int(bbslime.frame)].w, bbslime.ChaseState.image[bbslime.direct[0]*10+bbslime.direct[1]][int(bbslime.frame)].h
            if bbslime.direct[0]*10+bbslime.direct[1]:
                bbslime.ChaseState.image[bbslime.direct[0]*10+bbslime.direct[1]][int(bbslime.frame)].draw_to_origin(bbslime.locate[0], bbslime.locate[1],w*s_size, h*s_size)
            else:
                bbslime.ChaseState.image[bbslime.previous_direct[0]*10+bbslime.previous_direct[1]][int(bbslime.frame)].draw_to_origin(bbslime.locate[0], bbslime.locate[1], w*s_size, h*s_size)


    direct = None

    atk_delay = 0

    def __init__(self, _x, _y, _health, _speed, _direct=[0, -1]):
        super().__init__(_x, _y, _health, _speed, _direct)
        self.IdleState()
        self.AttackState()
        self.RunState()
        self.ChaseState()
        N_table = {
            self.IdleState : {self.my_event_list['faraway'] : self.IdleState, self.my_event_list['near'] : self.AttackState, self.my_event_list['detect'] : self.ChaseState },
            self.RunState : {self.my_event_list['faraway'] : self.IdleState, self.my_event_list['near'] : self.AttackState },
            self.AttackState : {self.my_event_list['faraway'] : self.IdleState, self.my_event_list['near'] : self.AttackState },
            self.ChaseState : {self.my_event_list['near'] : self.AttackState, self.my_event_list['faraway'] : self.IdleState}
        }
        # self.my_state_table()
        self.direct = self.get_direct()
        self.Set_next_state_table(N_table)
        self.Set_rectSize(self.IdleState.image[-1][0].w*s_size, self.IdleState.image[-1][0].h*s_size)
        self.Set_cur_state(self.IdleState)
        self.cur_state.enter(self, None)
        

    def rendering(self):
        return super().rendering()

    def update(self, deltatime):
        self.atk_delay -= game_framework.frame_time
        return super().update(deltatime)

class GollemKnight(Monster):

    class IdleState:

        __instance = None

        image = None

        TIME_PER_ACTION = 1.5
        ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
        FRAMES_PER_ACTION = 8

        def __init__(self):
            GollemKnight.IdleState.__instance = self
            if GollemKnight.IdleState.image == None:
                GollemKnight.IdleState.image = defaultdict(list)
                for i in range(0+1, 9):
                    GollemKnight.IdleState.image[-1].append(load_image('sprite\monster\Enemies_StoneSoldier_Floating_Down_'+str(i)+'.png'))
                    GollemKnight.IdleState.image[1].append(load_image('sprite\monster\Enemies_StoneSoldier_Floating_Up_'+str(i)+'.png'))
                    GollemKnight.IdleState.image[-10].append(load_image('sprite\monster\Enemies_StoneSoldier_Floating_Left_'+str(i)+'.png'))
                    GollemKnight.IdleState.image[10].append(load_image('sprite\monster\Enemies_StoneSoldier_Floating_Right_'+str(i)+'.png'))
                    GollemKnight.IdleState.image[0] = GollemKnight.IdleState.image[-1]
            

        def enter(gollem, event):
            gollem.frame = 0
            gollem.IdleState.image[0] = gollem.IdleState.image[gollem.previous_direct[0]*10+gollem.previous_direct[1]]
            gollem.previous_direct = gollem.direct
                
            gollem.direct[0] = clamp(-1, gollem.direct[0], 1)
            gollem.direct[1] = clamp(-1, gollem.direct[1], 1)
        

        def exit(gollem, event):
            pass

        def do(gollem, deltatime):
            gollem.frame = (gollem.frame + gollem.IdleState.FRAMES_PER_ACTION * gollem.IdleState.ACTION_PER_TIME * deltatime) % gollem.IdleState.FRAMES_PER_ACTION
            left_a, bottom_a, right_a, top_a = gollem.get_rect()
            my_rect = (left_a - 200, bottom_a - 200, right_a + 200, top_a + 200)
            if gollem.collider(my_rect, game_world.get_player_instacne()):
                if gollem.atk_delay < 0.0:
                    gollem.add_event(2)

        def draw(gollem):
            if gollem.direct[0]*10+gollem.direct[1]:
                gollem.IdleState.image[gollem.direct[0]*10+gollem.direct[1]][int(gollem.frame)].draw_to_origin(gollem.locate[0], gollem.locate[1], gollem.rect_size[0], gollem.rect_size[1])
            else:
                gollem.IdleState.image[gollem.previous_direct[0]*10+gollem.previous_direct[1]][int(gollem.frame)].draw_to_origin(gollem.locate[0], gollem.locate[1], gollem.rect_size[0], gollem.rect_size[1])


        def GetInstance(self):
            return self.__instance
        pass

    class AttackState:

        image = None

        TIME_PER_ACTION = 2.5
        ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
        FRAMES_PER_ACTION = 13

        def __init__(self):
            GollemKnight.AttackState.__instance = self
            if GollemKnight.AttackState.image == None:
                GollemKnight.AttackState.image = defaultdict(list)
                for i in range(0+1, 14):
                    GollemKnight.AttackState.image[-1].append(load_image('sprite\monster\Enemies_GolemSoldier_Attack_Down_'+str(i)+'.png'))
                    GollemKnight.AttackState.image[1].append(load_image('sprite\monster\Enemies_GolemSoldier_Attack_Up'+str(i)+'.png'))
                    GollemKnight.AttackState.image[-10].append(load_image('sprite\monster\Enemies_GolemSoldier_Attack_Left_'+str(i)+'.png'))
                    GollemKnight.AttackState.image[10].append(load_image('sprite\monster\Enemies_GolemSoldier_Attack_Right_'+str(i)+'.png'))
                    GollemKnight.AttackState.image[0] = GollemKnight.AttackState.image[-1]
            

        def enter(gollem, event):
            gollem.frame = 0
            gollem.AttackState.image[0] = gollem.AttackState.image[gollem.previous_direct[0]*10+gollem.previous_direct[1]]
            gollem.previous_direct = gollem.direct
                
            gollem.direct[0] = clamp(-1, gollem.direct[0], 1)
            gollem.direct[1] = clamp(-1, gollem.direct[1], 1)
        

        def exit(gollem, event):
            gollem.atk_delay = 5.0
            pass

        def do(gollem, deltatime):

            if gollem.frame > gollem.AttackState.FRAMES_PER_ACTION - 0.5:
                gollem.add_event(0)

            gollem.frame = (gollem.frame + gollem.AttackState.FRAMES_PER_ACTION * gollem.AttackState.ACTION_PER_TIME * deltatime) % gollem.AttackState.FRAMES_PER_ACTION


            # left_a, bottom_a, right_a, top_a = gollem.get_rect()
            # my_rect = (left_a - 50, bottom_a - 50, right_a + 50, top_a + 50)
            # if gollem.collider(my_rect, Player._instance):
            #     gollem.add_event(1)


        def draw(gollem):
            w, h = gollem.AttackState.image[gollem.direct[0]*10+gollem.direct[1]][int(gollem.frame)].w, gollem.AttackState.image[gollem.direct[0]*10+gollem.direct[1]][int(gollem.frame)].h
            if gollem.direct[0]*10+gollem.direct[1]:
                gollem.AttackState.image[gollem.direct[0]*10+gollem.direct[1]][int(gollem.frame)].draw_to_origin(gollem.locate[0], gollem.locate[1], w*s_size, h*s_size)
            else:
                gollem.AttackState.image[gollem.previous_direct[0]*10+gollem.previous_direct[1]][int(gollem.frame)].draw_to_origin(gollem.locate[0], gollem.locate[1], w*s_size, h*s_size)


        __instance = None
        

        def GetInstance(self):
            return self.__instance
        pass

    class RunState:
        __instance = None
        def __init__(self):
            self.__instance = self

        def GetInstance(self):
            return self.__instance
        pass

    class ChaseState:

        image = None

        TIME_PER_ACTION = 1.5
        ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
        FRAMES_PER_ACTION = 8

        def __init__(self):
            GollemKnight.ChaseState.__instance = self
            if GollemKnight.ChaseState.image == None:
                GollemKnight.ChaseState.image = defaultdict(list)
                for i in range(0+1, 9):
                    GollemKnight.ChaseState.image[-1].append(load_image('sprite\monster\Enemies_StoneSoldier_Floating_Down_'+str(i)+'.png'))
                    GollemKnight.ChaseState.image[1].append(load_image('sprite\monster\Enemies_StoneSoldier_Floating_Up_'+str(i)+'.png'))
                    GollemKnight.ChaseState.image[-10].append(load_image('sprite\monster\Enemies_StoneSoldier_Floating_Left_'+str(i)+'.png'))
                    GollemKnight.ChaseState.image[10].append(load_image('sprite\monster\Enemies_StoneSoldier_Floating_Right_'+str(i)+'.png'))
                    GollemKnight.ChaseState.image[0] = GollemKnight.ChaseState.image[-1]
            

        def enter(gollem, event):
            gollem.frame = 0
            gollem.ChaseState.image[0] = gollem.ChaseState.image[gollem.previous_direct[0]*10+gollem.previous_direct[1]]
            gollem.previous_direct = gollem.direct
                
            gollem.direct[0] = clamp(-1, gollem.direct[0], 1)
            gollem.direct[1] = clamp(-1, gollem.direct[1], 1)
        

        def exit(gollem, event):
            pass

        def do(gollem, deltatime):
            gollem.frame = (gollem.frame + gollem.ChaseState.FRAMES_PER_ACTION * gollem.ChaseState.ACTION_PER_TIME * deltatime) % gollem.ChaseState.FRAMES_PER_ACTION

            vector = [game_world.get_player_instacne().locate[0] - gollem.locate[0], game_world.get_player_instacne().locate[1] - gollem.locate[1]]
            weight = sqrt(vector[0]**2 + vector[1]**2)
            vector = [vector[0]/ weight * gollem.RUN_SPEED_PPS, vector[1]/ weight * gollem.RUN_SPEED_PPS]

            gollem.locate[0] += vector[0] * deltatime
            gollem.locate[1] += vector[1] * deltatime

            if abs(vector[0]) > abs(vector[1]):
                if vector[0] > 0: gollem.direct = [1, 0]
                else : gollem.direct = [-1, 0]
            else :
                if vector[1] > 0: gollem.direct = [0, 1]
                else : gollem.direct = [0, -1]

            left_a, bottom_a, right_a, top_a = gollem.get_rect()
            my_rect = (left_a - 50, bottom_a - 50, right_a + 50, top_a + 50)
            if gollem.collider(my_rect, game_world.get_player_instacne()) and gollem.atk_delay <= 0.0:
                gollem.add_event(1)


        def draw(gollem):
            w, h = gollem.ChaseState.image[gollem.direct[0]*10+gollem.direct[1]][int(gollem.frame)].w, gollem.ChaseState.image[gollem.direct[0]*10+gollem.direct[1]][int(gollem.frame)].h
            if gollem.direct[0]*10+gollem.direct[1]:
                gollem.ChaseState.image[gollem.direct[0]*10+gollem.direct[1]][int(gollem.frame)].draw_to_origin(gollem.locate[0], gollem.locate[1],w*s_size, h*s_size)
            else:
                gollem.ChaseState.image[gollem.previous_direct[0]*10+gollem.previous_direct[1]][int(gollem.frame)].draw_to_origin(gollem.locate[0], gollem.locate[1], w*s_size, h*s_size)



        __instance = None

        def GetInstance(self):
            return self.__instance
        pass

    direct = None

    atk_delay = 0

    def __init__(self, _x, _y, _health, _speed, _direct=[0, -1]):
        super().__init__(_x, _y, _health, _speed, _direct)
        self.IdleState()
        self.AttackState()
        self.RunState()
        self.ChaseState()
        N_table = {
            self.IdleState : {self.my_event_list['faraway'] : self.IdleState, self.my_event_list['near'] : self.AttackState, self.my_event_list['detect'] : self.ChaseState },
            self.RunState : {self.my_event_list['faraway'] : self.IdleState, self.my_event_list['near'] : self.AttackState },
            self.AttackState : {self.my_event_list['faraway'] : self.IdleState, self.my_event_list['near'] : self.AttackState },
            self.ChaseState : {self.my_event_list['near'] : self.AttackState, self.my_event_list['faraway'] : self.IdleState}
        }
        # self.my_state_table()
        self.direct = self.get_direct()
        self.Set_next_state_table(N_table)
        self.Set_rectSize(self.IdleState.image[-1][0].w*s_size, self.IdleState.image[-1][0].h*s_size)
        self.Set_cur_state(self.IdleState)
        self.cur_state.enter(self, None)
        

    def rendering(self):
        return super().rendering()

    def update(self, deltatime):
        self.atk_delay -= game_framework.frame_time
        return super().update(deltatime)
        

    pass


