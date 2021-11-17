from math import dist, sqrt
from object import *



monster_status_table = {'slime': [50, 5], 'gollem': [100, 10]}

class Monster(Object):

    RUN_SPEED_KMPH = 1.0
    RUN_SPEED_MPM = 0
    RUN_SPEED_MPS = 0
    RUN_SPEED_PPS = 0

    event_que = []
    cur_state = None

    vector = None

    my_event_list = {'faraway': 0, 'near': 1}
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

    def update(self, deltatime):
        self.cur_state.do(self, deltatime)
        if len(self.event_que) > 0:
            event = self.event_que.pop()
            if event in self.my_next_state_table[self.cur_state]:
                pass
    
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
            if self.image == None:
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

        def draw(gollem):
            if gollem.direct[0]*10+gollem.direct[1]:
                gollem.IdleState.image[gollem.direct[0]*10+gollem.direct[1]][int(gollem.frame)].draw_to_origin(gollem.locate[0], gollem.locate[1], gollem.rect_size[0], gollem.rect_size[1])
            else:
                gollem.IdleState.image[gollem.previous_direct[0]*10+gollem.previous_direct[1]][int(gollem.frame)].draw_to_origin(gollem.locate[0], gollem.locate[1], gollem.rect_size[0], gollem.rect_size[1])


        def GetInstance(self):
            return self.__instance
        pass

    class AttackState:
        __instance = None
        def __init__(self):
            self.__instance = self

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
        __instance = None
        def __init__(self):
            self.__instance = self

        def GetInstance(self):
            return self.__instance
        pass


    rect_size = None
    direct = None

    def __init__(self, _x, _y, _health, _speed, _direct=[0, -1]):
        super().__init__(_x, _y, _health, _speed, _direct)
        self.IdleState()
        self.AttackState()
        self.RunState()
        self.ChaseState()
        N_table = {
            self.IdleState : {self.my_event_list['faraway'] : self.IdleState, self.my_event_list['near'] : self.AttackState },
            self.RunState : {self.my_event_list['faraway'] : self.IdleState, self.my_event_list['near'] : self.AttackState },
            self.AttackState : {self.my_event_list['faraway'] : self.IdleState, self.my_event_list['near'] : self.AttackState }
        }
        # self.my_state_table()
        self.direct = self.get_direct()
        self.Set_next_state_table(N_table)
        self.rect_size = [self.IdleState.image[-1][0].w*s_size, self.IdleState.image[-1][0].h*s_size]
        self.Set_cur_state(self.IdleState)
        self.cur_state.enter(self, None)
        

    def rendering(self):
        return super().rendering()

    def update(self, deltatime):
        return super().update(deltatime)

    pass