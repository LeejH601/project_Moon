from math import dist, sqrt
from object import *
from Player import Player


monster_status_table = {'slime': [50, 5], 'gollem': [100, 10]}

class Monster(Object):

    RUN_SPEED_KMPH = 1.0
    RUN_SPEED_MPM = 0
    RUN_SPEED_MPS = 0
    RUN_SPEED_PPS = 0

    event_que = []
    cur_state = None

    vector = None

    my_event_list = {'faraway': 0, 'near': 1, 'detect': 2}
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

    def rendering(self):
        self.cur_state.draw(self)
        draw_rectangle(*self.get_rect())

    def update(self, deltatime):
        self.cur_state.do(self, deltatime)
        if len(self.event_que) > 0:
            event = self.event_que.pop()
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

    pass

class SmallSlime(Monster):
    pass

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
            if gollem.collider(my_rect, Player._instance):
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

        TIME_PER_ACTION = 4
        ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
        FRAMES_PER_ACTION = 13

        def __init__(self):
            GollemKnight.ChaseState.__instance = self
            if GollemKnight.ChaseState.image == None:
                GollemKnight.ChaseState.image = defaultdict(list)
                for i in range(0+1, 14):
                    GollemKnight.ChaseState.image[-1].append(load_image('sprite\monster\Enemies_GolemSoldier_Attack_Down_'+str(i)+'.png'))
                    GollemKnight.ChaseState.image[1].append(load_image('sprite\monster\Enemies_GolemSoldier_Attack_Up'+str(i)+'.png'))
                    GollemKnight.ChaseState.image[-10].append(load_image('sprite\monster\Enemies_GolemSoldier_Attack_Left_'+str(i)+'.png'))
                    GollemKnight.ChaseState.image[10].append(load_image('sprite\monster\Enemies_GolemSoldier_Attack_Right_'+str(i)+'.png'))
                    GollemKnight.ChaseState.image[0] = GollemKnight.ChaseState.image[-1]
            

        def enter(gollem, event):
            gollem.frame = 0
            gollem.ChaseState.image[0] = gollem.ChaseState.image[gollem.previous_direct[0]*10+gollem.previous_direct[1]]
            gollem.previous_direct = gollem.direct
                
            gollem.direct[0] = clamp(-1, gollem.direct[0], 1)
            gollem.direct[1] = clamp(-1, gollem.direct[1], 1)
        

        def exit(gollem, event):
            gollem.atk_delay = 5.0
            pass

        def do(gollem, deltatime):

            if gollem.frame > gollem.ChaseState.FRAMES_PER_ACTION - 0.5:
                gollem.add_event(0)

            gollem.frame = (gollem.frame + gollem.ChaseState.FRAMES_PER_ACTION * gollem.ChaseState.ACTION_PER_TIME * deltatime) % gollem.ChaseState.FRAMES_PER_ACTION


            # left_a, bottom_a, right_a, top_a = gollem.get_rect()
            # my_rect = (left_a - 50, bottom_a - 50, right_a + 50, top_a + 50)
            # if gollem.collider(my_rect, Player._instance):
            #     gollem.add_event(1)


        def draw(gollem):
            w, h = gollem.ChaseState.image[gollem.direct[0]*10+gollem.direct[1]][int(gollem.frame)].w, gollem.ChaseState.image[gollem.direct[0]*10+gollem.direct[1]][int(gollem.frame)].h
            if gollem.direct[0]*10+gollem.direct[1]:
                gollem.ChaseState.image[gollem.direct[0]*10+gollem.direct[1]][int(gollem.frame)].draw_to_origin(gollem.locate[0], gollem.locate[1], w*s_size, h*s_size)
            else:
                gollem.ChaseState.image[gollem.previous_direct[0]*10+gollem.previous_direct[1]][int(gollem.frame)].draw_to_origin(gollem.locate[0], gollem.locate[1], w*s_size, h*s_size)


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

            vector = [Player._instance.locate[0] - gollem.locate[0], Player._instance.locate[1] - gollem.locate[1]]
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
            if gollem.collider(my_rect, Player._instance) and gollem.atk_delay <= 0.0:
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


