from math import fabs
from object import *

history = []

RIGHT_DOWN, LEFT_DOWN, RIGHT_UP, LEFT_UP, SPACE, TOP_UP, TOP_DOWN, BOTTOM_UP, BOTTOM_DOWN, \
    ATTACK_DOWN, ATTACK_UP, SATTACK_DOWN, SATTACK_UP, INVENTORY_DOWN, INVENTORY_UP, EVASION_TIMER, DEBUG_KEY, ATK_TIMER  = range(18)


event_name = ['RIGHT_DOWN', 'LEFT_DOWN', 'RIGHT_UP', 'LEFT_UP', 'SPACE', 'TOP_UP', 'TOP_DOWN', 'BOTTOM_UP', 'BOTTOM_DOWN', \
    'ATTACK_DOWN', 'ATTACK_UP', 'SATTACK_DOWN', 'SATTACK_UP', 'INVENTORY_DOWN', 'INVENTORY_UP', 'EVASION_TIMER', 'DEBUG_KEY', 'ATK_TIMER']

key_event_table = {
    (SDL_KEYDOWN, SDLK_d): RIGHT_DOWN,
    (SDL_KEYDOWN, SDLK_a): LEFT_DOWN,
    (SDL_KEYUP, SDLK_d): RIGHT_UP,
    (SDL_KEYUP, SDLK_a): LEFT_UP,
    (SDL_KEYDOWN, SDLK_w): TOP_DOWN,
    (SDL_KEYDOWN, SDLK_s): BOTTOM_DOWN,
    (SDL_KEYUP, SDLK_w): TOP_UP,
    (SDL_KEYUP, SDLK_s): BOTTOM_UP,
    (SDL_KEYDOWN, SDLK_SPACE): SPACE,
    (SDL_KEYDOWN, SDLK_j): ATTACK_DOWN,
    (SDL_KEYDOWN, SDLK_k): SATTACK_DOWN,
    (SDL_KEYUP, SDLK_j): ATTACK_UP,
    (SDL_KEYUP, SDLK_k): SATTACK_UP,
    (SDL_KEYDOWN, SDLK_i): INVENTORY_DOWN,
    (SDL_KEYDOWN, SDLK_0): DEBUG_KEY
}

RUN_SPEED_KMPH = 20.0
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)


EVA_SPEED_KMPH = 40.0
EVA_SPEED_MPM = (EVA_SPEED_KMPH * 1000.0 / 60.0)
EVA_SPEED_MPS = (EVA_SPEED_MPM / 60.0)
EVA_SPEED_PPS = (EVA_SPEED_MPS * PIXEL_PER_METER)

class IdleState:

    TIME_PER_ACTION = 1.5
    ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
    FRAMES_PER_ACTION = 9

    image = None

    def __init__(self):
        if IdleState.image == None:
            IdleState.image = defaultdict(list)
            for i in range(0+1, 10):
                IdleState.image[-1].append(load_image('sprite\Will_Idle_Down_'+str(i)+'.png'))
                IdleState.image[1].append(load_image('sprite\Will_Idle_Up_'+str(i)+'.png'))
                IdleState.image[-10].append(load_image('sprite\Will_Idle_Left_'+str(i)+'.png'))
                IdleState.image[10].append(load_image('sprite\Will_Idle_Right_'+str(i)+'.png'))
                IdleState.image[0] = IdleState.image[-1]


    def enter(player, event):
        player.frame = 0
        IdleState.image[0] = IdleState.image[player.previous_direct[0]*10+player.previous_direct[1]]
        print("now direct : " , player.previous_direct)
        player.previous_direct = player.direct
        if event == RIGHT_DOWN:
                player.velocity[0] += 1
        elif event == LEFT_DOWN:
                player.velocity[0] -= 1    
        elif event == RIGHT_UP:
                player.velocity[0] -= 1
        elif event == LEFT_UP:
                player.velocity[0] += 1
        elif event == TOP_DOWN:
                player.velocity[1] += 1
        elif event == BOTTOM_DOWN:
                player.velocity[1] -= 1
        elif event == TOP_UP:
                player.velocity[1] -= 1
        elif event == BOTTOM_UP:
                player.velocity[1] += 1
            
        player.direct[0] = clamp(-1, player.direct[0], 1)
        player.direct[1] = clamp(-1, player.direct[1], 1)
        

    def exit(player, event):
        pass

    def do(player):
        player.frame = (player.frame + IdleState.FRAMES_PER_ACTION * IdleState.ACTION_PER_TIME * game_framework.frame_time) % IdleState.FRAMES_PER_ACTION

    def draw(player):
        if player.direct[0]*10+player.direct[1]:
            IdleState.image[player.direct[0]*10+player.direct[1]][int(player.frame)].draw_to_origin(player.locate[0], player.locate[1], player.rect_size[0], player.rect_size[1])
        else:
            IdleState.image[player.previous_direct[0]*10+player.previous_direct[1]][int(player.frame)].draw_to_origin(player.locate[0], player.locate[1], player.rect_size[0], player.rect_size[1])

class RunState:

    TIME_PER_ACTION = 1
    ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
    FRAMES_PER_ACTION = 8

    image = None

    key_able = [False, False, False, False]

    def __init__(self):
        if RunState.image == None:
            RunState.image = defaultdict(list)
            for i in range(0+1, 9):
                RunState.image[-1].append(load_image('sprite\will animation cycle front dungeon_0'+str(i)+'.png'))
                RunState.image[1].append(load_image('sprite\will walking cycle back_0'+str(i)+'.png'))
                RunState.image[-10].append(load_image('sprite\will_walking cycle_left side0'+str(i)+'.png'))
                RunState.image[10].append(load_image('sprite\will_walking cycle_right side0'+str(i)+'.png'))
                RunState.image[0] = RunState.image[-1]

    def enter(player, event):
        # player.frame = 0
        player.previous_direct = player.direct
        # player.direct = [0, 0]
        if event == RIGHT_DOWN:
            player.velocity[0] += 1
            player.direct[0] += 1
            RunState.key_able[0] = True
        elif event == LEFT_DOWN:
            player.velocity[0] -= 1    
            player.direct[0] -= 1
            RunState.key_able[1] = True
        elif event == RIGHT_UP:
            player.velocity[0] -= 1
            player.direct[0] -= 1
            RunState.key_able[0] = False
        elif event == LEFT_UP:
            player.velocity[0] += 1
            player.direct[0] += 1
            RunState.key_able[1] = False
        elif event == TOP_DOWN :
            player.velocity[1] += 1
            player.direct[1] += 1
            RunState.key_able[2] = True
        elif event == BOTTOM_DOWN:
            player.velocity[1] -= 1
            player.direct[1] -= 1
            RunState.key_able[3] = True
        elif event == TOP_UP :
            player.velocity[1] -= 1
            player.direct[1]-= 1
            RunState.key_able[2] = False
        elif event == BOTTOM_UP:
            player.velocity[1] += 1
            player.direct[1] += 1
            RunState.key_able[3] = False
        # if player.direct == [0, 0]:
        #     player.direct = [0, -1]
        player.direct[0] = clamp(-1, player.direct[0], 1)
        player.direct[1] = clamp(-1, player.direct[1], 1)
        player.velocity[0] = clamp(-1, player.velocity[0], 1)
        player.velocity[1] = clamp(-1, player.velocity[1], 1)
        RunState.image[0] = RunState.image[player.direct[0]*10+player.direct[1]]
        distance = math.sqrt(player.velocity[0]**2 + player.velocity[1]**2)
        if distance != 0:
            player.vector = [player.velocity[0] / distance, player.velocity[1]/distance]
        else:
            player.vector = [player.velocity[0], player.velocity[1]]
        player.vector = [player.vector[0]* RUN_SPEED_PPS, player.vector[1]* RUN_SPEED_PPS]
        if abs(player.vector[0]) > abs(player.vector[1]):
            if player.vector[0] > 0:
                player.direct = [1,0]
            else:
                player.direct = [-1,0]
        else:
            if player.vector[1] > 0:
                player.direct = [0,1]
            else:
                player.direct = [0,-1]

        print(event, player.velocity)
        pass

    def exit(player, event):
        if event == RIGHT_UP:
            RunState.key_able[0] = False
        elif event == LEFT_UP:
            RunState.key_able[1] = False
        elif event == TOP_UP :
            RunState.key_able[2] = False
        elif event == BOTTOM_UP:
            RunState.key_able[3] = False

    def do(player):
        player.frame = (player.frame + RunState.FRAMES_PER_ACTION * RunState.ACTION_PER_TIME * game_framework.frame_time) % RunState.FRAMES_PER_ACTION
        player.locate[0] += player.vector[0] * game_framework.frame_time
        player.locate[1] += player.vector[1] * game_framework.frame_time
        player.locate = player.myclamp()

    def draw(player):
        if player.direct[0]*10+player.direct[1] in RunState.image and player.vector != [0,0]:
            RunState.image[player.direct[0]*10+player.direct[1]][int(player.frame)].draw_to_origin(player.locate[0], player.locate[1], player.rect_size[0], player.rect_size[1])
        elif player.vector == [0, 0]:
            IdleState.image[player.direct[0]*10+player.direct[1]][int(player.frame)].draw_to_origin(player.locate[0], player.locate[1], player.rect_size[0], player.rect_size[1])
        # else:
        #     RunState.image[player.previous_direct[0]*10+player.previous_direct[1]][int(player.frame)].draw_to_origin(player.locate[0], player.locate[1], player.rect_size[0], player.rect_size[1])




class EvasionState:
    TIME_PER_ACTION = 0.5
    ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
    FRAMES_PER_ACTION = 8

    image = None

    E_timer = 0.0

    now_evasion = False

    def __init__(self):
        if EvasionState.image == None:
            EvasionState.image = defaultdict(list)
            for i in range(0+1, 9):
                EvasionState.image[-1].append(load_image('sprite\Will_Roll_Down_'+str(i)+'.png'))
                EvasionState.image[1].append(load_image('sprite\Will_Roll_Up_'+str(i)+'.png'))
                EvasionState.image[-10].append(load_image('sprite\Will_Roll_Left_'+str(i)+'.png'))
                EvasionState.image[10].append(load_image('sprite\Will_Roll_Right_'+str(i)+'.png'))
                EvasionState.image[0] = EvasionState.image[-1]



    def enter(player, event):
        if EvasionState.now_evasion == False:
            player.frame = 0
            if player.direct == [0, 0]:
                player.direct = player.previous_direct
                
            player.direct[0] = clamp(-1, player.direct[0], 1)
            player.direct[1] = clamp(-1, player.direct[1], 1)
            EvasionState.image[0] = EvasionState.image[player.direct[0]*10+player.direct[1]]

            EvasionState.E_timer = EvasionState.TIME_PER_ACTION
            EvasionState.now_evasion = True
            if player.vector != [0, 0]:
                player.vector = [player.vector[0]/RUN_SPEED_PPS*EVA_SPEED_PPS,player.vector[1]/RUN_SPEED_PPS*EVA_SPEED_PPS]
            else:
                player.vector = [player.direct[0]*EVA_SPEED_PPS, player.direct[1]*EVA_SPEED_PPS]
        

    def exit(player, event):
        pass

    def do(player):
        player.frame = (player.frame + EvasionState.FRAMES_PER_ACTION * EvasionState.ACTION_PER_TIME * game_framework.frame_time) % EvasionState.FRAMES_PER_ACTION

        player.locate[0] += player.vector[0] * game_framework.frame_time
        player.locate[1] += player.vector[1] * game_framework.frame_time
        player.locate = player.myclamp()

        EvasionState.E_timer -= game_framework.frame_time
        print(EvasionState.E_timer)
        if EvasionState.E_timer <= 0.0:
            player.add_event(EVASION_TIMER)
            player.vector = [player.vector[0]/EVA_SPEED_PPS*RUN_SPEED_PPS,player.vector[1]/EVA_SPEED_PPS*RUN_SPEED_PPS]
            player.velocity = [0, 0]
            player.vector = [0, 0]
            EvasionState.now_evasion = False

    def draw(player):
        if player.direct[0]*10+player.direct[1] in EvasionState.image:
            EvasionState.image[player.direct[0]*10+player.direct[1]][int(player.frame)].draw_to_origin(player.locate[0], player.locate[1], player.rect_size[0], player.rect_size[1])
        else:
            EvasionState.image[player.previous_direct[0]*10+player.previous_direct[1]][int(player.frame)].draw_to_origin(player.locate[0], player.locate[1], player.rect_size[0], player.rect_size[1])


class SwordAttackState:
    TIME_PER_ACTION = 2.3
    ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
    FRAMES_PER_ACTION = 18

    image = None

    Start_Frame = 0
    Stack_to_image_Table = { 0: 5, 1: 4, 2: 9}

    Atk_Timer = 0
    Atk_Stack = 0

    now_Atk = False
    is_continue_1 = False
    is_continue_2 = False

    def __init__(self):
        if SwordAttackState.image == None:
            SwordAttackState.image = defaultdict(list)
            for i in range(0+1, 19):
                SwordAttackState.image[-1].append(load_image('sprite\Will_ShortSwordCombo_Animation_Down_'+str(i)+'.png'))
                SwordAttackState.image[1].append(load_image('sprite\Will_ShortSwordCombo_Animation_Up_'+str(i)+'.png'))
                SwordAttackState.image[-10].append(load_image('sprite\Will_ShortSwordCombo_Animation_Left_'+str(i)+'.png'))
                SwordAttackState.image[10].append(load_image('sprite\Will_ShortSwordCombo_Animation_Right_'+str(i)+'.png'))
                SwordAttackState.image[0] = SwordAttackState.image[-1]



    def enter(player, event):
        if SwordAttackState.now_Atk == False:

            # if SwordAttackState.Atk_Stack >= 3:
            #     SwordAttackState.Atk_Stack = 0

            # SwordAttackState.FRAMES_PER_ACTION = SwordAttackState.Stack_to_image_Table[SwordAttackState.Atk_Stack]
            # SwordAttackState.TIME_PER_ACTION = SwordAttackState.FRAMES_PER_ACTION / 10
            # print('TimePerAction: ', SwordAttackState.TIME_PER_ACTION)
            # SwordAttackState.ACTION_PER_TIME = 1.0 / SwordAttackState.TIME_PER_ACTION
            # SwordAttackState.Atk_Stack += 1
            

            SwordAttackState.Start_Frame = 0
            # for i in range(0, SwordAttackState.Atk_Stack - 1):
            #     SwordAttackState.Start_Frame += SwordAttackState.Stack_to_image_Table[i]
            
            player.frame = 0
            print(SwordAttackState.Start_Frame)
            print('action timer print: ', SwordAttackState.FRAMES_PER_ACTION, SwordAttackState.TIME_PER_ACTION,  SwordAttackState.TIME_PER_ACTION)
            if player.direct == [0, 0]:
                player.direct = player.previous_direct
                
            player.direct[0] = clamp(-1, player.direct[0], 1)
            player.direct[1] = clamp(-1, player.direct[1], 1)
            SwordAttackState.image[0] = SwordAttackState.image[player.direct[0]*10+player.direct[1]]
 

            SwordAttackState.Atk_Timer = SwordAttackState.TIME_PER_ACTION
            SwordAttackState.now_Atk = True
        

    def exit(player, event):
        pass

    def do(player):
        player.frame = SwordAttackState.Start_Frame + ((player.frame + SwordAttackState.FRAMES_PER_ACTION * SwordAttackState.ACTION_PER_TIME * game_framework.frame_time) % SwordAttackState.FRAMES_PER_ACTION)
        # print(player.frame)
        SwordAttackState.Atk_Timer -= game_framework.frame_time
        if SwordAttackState.Atk_Timer <= 0.0 and SwordAttackState.now_Atk:
            player.add_event(ATK_TIMER)
            SwordAttackState.now_Atk = False
            SwordAttackState.is_continue_1 = False
            SwordAttackState.is_continue_2 = False
        elif player.frame > 5 and SwordAttackState.is_continue_1 == False:
            player.add_event(ATK_TIMER)
            SwordAttackState.now_Atk = False
        elif player.frame > 9 and SwordAttackState.is_continue_2 == False:
            player.add_event(ATK_TIMER)
            SwordAttackState.now_Atk = False
        if player.frame < 5:
            events = get_events()
            for event in events:
                if event.type == SDL_KEYDOWN and event.key == SDLK_j:
                   SwordAttackState.is_continue_1 = True
        elif player.frame > 5 and player.frame < 9:
            events = get_events()
            for event in events:
                if event.type == SDL_KEYDOWN and event.key == SDLK_j:
                   SwordAttackState.is_continue_2 = True


        
        player.locate = player.myclamp()

        

    def draw(player):
        if player.direct[0]*10+player.direct[1] in SwordAttackState.image:
            SwordAttackState.image[player.direct[0]*10+player.direct[1]][int(player.frame)].draw_to_origin(player.locate[0], player.locate[1], player.rect_size[0], player.rect_size[1])
        else:
            SwordAttackState.image[player.previous_direct[0]*10+player.previous_direct[1]][int(player.frame)].draw_to_origin(player.locate[0], player.locate[1], player.rect_size[0], player.rect_size[1])


class SwordDeffenseState:
    pass

class DeffesedRunState:
    pass


next_state_table = {
    IdleState: {RIGHT_DOWN: RunState, LEFT_DOWN: RunState, TOP_DOWN: RunState, BOTTOM_DOWN: RunState,
                 SPACE: EvasionState, ATTACK_DOWN: SwordAttackState, ATTACK_UP: SwordAttackState, SATTACK_DOWN: SwordDeffenseState, SATTACK_UP: SwordDeffenseState},
    RunState: {RIGHT_DOWN: RunState, LEFT_DOWN: RunState, RIGHT_UP: IdleState, LEFT_UP: IdleState, TOP_UP: IdleState, TOP_DOWN: RunState, BOTTOM_UP: IdleState, BOTTOM_DOWN: RunState,
                 SPACE: EvasionState, ATTACK_DOWN: SwordAttackState, ATTACK_UP: SwordAttackState, SATTACK_DOWN: SwordDeffenseState, SATTACK_UP: SwordDeffenseState},
    EvasionState : {RIGHT_DOWN: EvasionState, LEFT_DOWN: EvasionState, RIGHT_UP: EvasionState, LEFT_UP: EvasionState, TOP_UP: EvasionState, TOP_DOWN: EvasionState, BOTTOM_UP: EvasionState, BOTTOM_DOWN: EvasionState,
                 SPACE: EvasionState, ATTACK_DOWN: EvasionState, ATTACK_UP: EvasionState, SATTACK_DOWN: EvasionState, SATTACK_UP: EvasionState, EVASION_TIMER: IdleState},
    SwordAttackState: {RIGHT_DOWN: SwordAttackState, LEFT_DOWN: SwordAttackState, RIGHT_UP: SwordAttackState, LEFT_UP: SwordAttackState, TOP_UP: SwordAttackState, TOP_DOWN: SwordAttackState, BOTTOM_UP: SwordAttackState, BOTTOM_DOWN: SwordAttackState,
                 SPACE: SwordAttackState, ATTACK_DOWN: SwordAttackState, ATTACK_UP: SwordAttackState, SATTACK_DOWN: SwordAttackState, SATTACK_UP: SwordAttackState, EVASION_TIMER: SwordAttackState,
                    ATK_TIMER: IdleState},
    SwordDeffenseState : {RIGHT_DOWN: DeffesedRunState, LEFT_DOWN: DeffesedRunState, RIGHT_UP: DeffesedRunState, LEFT_UP: DeffesedRunState, TOP_UP: DeffesedRunState, TOP_DOWN: DeffesedRunState, BOTTOM_UP: DeffesedRunState, BOTTOM_DOWN: DeffesedRunState,
                 SPACE: EvasionState, ATTACK_DOWN: SwordAttackState, ATTACK_UP: SwordAttackState, SATTACK_DOWN: SwordDeffenseState, SATTACK_UP: IdleState},
    DeffesedRunState : {RIGHT_DOWN: SwordDeffenseState, LEFT_DOWN: SwordDeffenseState, RIGHT_UP: SwordDeffenseState, LEFT_UP: SwordDeffenseState, TOP_UP: SwordDeffenseState, TOP_DOWN: SwordDeffenseState, BOTTOM_UP: SwordDeffenseState, BOTTOM_DOWN: SwordDeffenseState,
                 SPACE: EvasionState, ATTACK_DOWN: SwordAttackState, ATTACK_UP: SwordAttackState, SATTACK_DOWN: DeffesedRunState, SATTACK_UP: IdleState},
}




class Singleton():
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not isinstance(cls._instance, cls):
            print('create')
            cls._instance = super(Singleton, cls).__new__(cls)
        else:
            print('recycle')
        return cls._instance


class Player(Object, Singleton):

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
    
    velocity = [0, 0]
    frame = 0
    event_que = []
    cur_state = IdleState   

    previous_direct = None
    vector = [0, 0]

    def __init__(self, _x, _y, _health, _speed):
        super().__init__(_x, _y, _health, _speed)
        IdleState()
        RunState()
        EvasionState()
        SwordAttackState()
        self.rect_size = [IdleState.image[1][0].w*s_size, IdleState.image[1][0].h*s_size]
        Player.previous_direct = self.direct
        self.cur_state.enter(self, None)
        print(self.locate)

    def rendering(self):
        self.cur_state.draw(self)

    def handle_event(self, event):
        if (event.type, event.key) in key_event_table:
            key_event = key_event_table[(event.type, event.key)]
            if DEBUG_KEY == key_event:
                print(history[-10:])
            else:
                self.add_event(key_event)

    def update(self):
        self.cur_state.do(self)
        if len(self.event_que) > 0:
            event = self.event_que.pop()
            if event in next_state_table[self.cur_state]:
                # print("카운트 출력 : ", RunState.key_able.count(True))
                if self.cur_state == RunState and RunState.key_able.count(True) > 1 and \
                    (event == RIGHT_UP or event == LEFT_UP or event == TOP_UP or event == BOTTOM_UP):
                    pass
                else:
                    self.cur_state.exit(self, event)
                    try:
                        self.cur_state = next_state_table[self.cur_state][event]
                        history.append(   (self.cur_state.__name__, event_name[event])   )
                    except:
                        print('State : ' + self.cur_state.__name__ + 'Event: ' + event_name[event])
                        exit(-1)
                self.cur_state.enter(self, event)

    def add_event(self, event):
        self.event_que.insert(0, event)

    pass