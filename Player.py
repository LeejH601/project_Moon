from object import *


RIGHT_DOWN, LEFT_DOWN, RIGHT_UP, LEFT_UP, SPACE, TOP_UP, TOP_DOWN, BOTTOM_UP, BOTTOM_DOWN, \
    ATTACK_DOWN, ATTACK_UP, SATTACK_DOWN, SATTACK_UP, INVENTORY_DOWN, INVENTORY_UP, EVASION_TIMER  = range(16)

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
}

class IdleState:
    def enter(boy, event):
        if event == RIGHT_DOWN:
            boy.velocity += RUN_SPEED_PPS
        elif event == LEFT_DOWN:
            boy.velocity -= RUN_SPEED_PPS
        elif event == RIGHT_UP:
            boy.velocity -= RUN_SPEED_PPS
        elif event == LEFT_UP:
            boy.velocity += RUN_SPEED_PPS
        boy.timer = 1000

    def exit(boy, event):
        if event == SPACE:
            boy.fire_ball()
        pass

    def do(boy):
        boy.frame = (boy.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 8
        boy.timer -= 1
        if boy.timer == 0:
            boy.add_event(SLEEP_TIMER)

    def draw(boy):
        if boy.dir == 1:
            boy.image.clip_draw(int(boy.frame) * 100, 300, 100, 100, boy.x, boy.y)
        else:
            boy.image.clip_draw(int(boy.frame) * 100, 200, 100, 100, boy.x, boy.y)

class RunState:
    pass

class EvasionState:
    pass

class SwordAttackState:
    pass

class SwordDeffenseState:
    pass

class DeffesedRunState:
    pass


next_state_table = {
    IdleState: {RIGHT_DOWN: RunState, LEFT_DOWN: RunState, RIGHT_UP: RunState, LEFT_UP: RunState, TOP_UP: RunState, TOP_DOWN: RunState, BOTTOM_UP: RunState, BOTTOM_DOWN: RunState,
                 SPACE: EvasionState, ATTACK_DOWN: SwordAttackState, ATTACK_UP: SwordAttackState, SATTACK_DOWN: SwordDeffenseState, SATTACK_UP: SwordDeffenseState},
    RunState: {RIGHT_DOWN: IdleState, LEFT_DOWN: IdleState, RIGHT_UP: IdleState, LEFT_UP: IdleState, TOP_UP: IdleState, TOP_DOWN: IdleState, BOTTOM_UP: IdleState, BOTTOM_DOWN: IdleState,
                 SPACE: EvasionState, ATTACK_DOWN: SwordAttackState, ATTACK_UP: SwordAttackState, SATTACK_DOWN: SwordDeffenseState, SATTACK_UP: SwordDeffenseState},
    EvasionState : {RIGHT_DOWN: EvasionState, LEFT_DOWN: EvasionState, RIGHT_UP: EvasionState, LEFT_UP: EvasionState, TOP_UP: EvasionState, TOP_DOWN: EvasionState, BOTTOM_UP: EvasionState, BOTTOM_DOWN: EvasionState,
                 SPACE: EvasionState, ATTACK_DOWN: EvasionState, ATTACK_UP: EvasionState, SATTACK_DOWN: EvasionState, SATTACK_UP: EvasionState, EVASION_TIMER: IdleState},
    SwordAttackState: {RIGHT_DOWN: SwordAttackState, LEFT_DOWN: SwordAttackState, RIGHT_UP: SwordAttackState, LEFT_UP: SwordAttackState, TOP_UP: SwordAttackState, TOP_DOWN: SwordAttackState, BOTTOM_UP: SwordAttackState, BOTTOM_DOWN: SwordAttackState,
                 SPACE: SwordAttackState, ATTACK_DOWN: SwordAttackState, ATTACK_UP: SwordAttackState, SATTACK_DOWN: SwordAttackState, SATTACK_UP: SwordAttackState, EVASION_TIMER: SwordAttackState},
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


    def __init__(self, _x, _y, _health, _speed):
        super().__init__(_x, _y, _health, _speed)

    def rendering(self):
        return super().rendering()

    def handle_event(self, event):
        if (event.type, event.key) in key_event_table:
            key_event = key_event_table[(event.type, event.key)]
            self.add_event(key_event)

    def update(self):
        return super().update()

    def add_event(self):
        pass

    pass