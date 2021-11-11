#from os import get_exec_path
import time
from Monster import Monster
from Object import *
from Player import *

animation_rate = 0
    
event_queue = []

def myRender():    
    global p1
    clear_canvas()
    #character.clip_draw(frame * 100, 100 * 1, 100, 100, x, 90)
    b_w, b_h = background.w, background.h
    plus_size = 5
    background.draw_to_origin(0-plus_size,0-plus_size,b_w*2+plus_size*2, b_h*2+plus_size*2)
    for o in game_world.all_objects():
        o.rendering()
    # mob.rendering()
    # p1.rendering()
    update_canvas()


def update():
    global mob, p1
    for o in game_world.all_objects():
        o.update()
    # p1.update()
    # mob.update()
    # print(player.animation_frame)


def input():
    global p1, event_queue
    # if len(event_queue) == 0:
    events = get_events()
    # else:
    #     events = event_queue()
    for event in events:
        if event.type == SDL_KEYDOWN:
            # print(p1.get_state())
            if p1.state == 'SSHEILD':
                print('ssthild')
            if p1.get_state() == states['IDLE'] or p1.get_state() == states['MOVE']:
                if event.key == SDLK_d:
                    p1.set_direct('right')
                    p1.move_right()
                    p1.set_move_flag(True)
                if event.key == SDLK_a:
                    p1.set_direct('left')
                    p1.move_left()
                    p1.set_move_flag(True)
                if event.key == SDLK_w:
                    p1.set_direct('up')
                    p1.move_up()
                    p1.set_move_flag(True)
                if event.key == SDLK_s:
                    p1.set_direct('down')
                    p1.move_down()
                    p1.set_move_flag(True)
                if event.key == SDLK_SPACE:
                    p1.set_Roll()
                if event.key == SDLK_k:
                    p1.S_attack()
            if p1.get_state() == states['SSHIELD'] or p1.get_state() == 'SHEILDWALK':
                print('swali_IN')
                if event.key == SDLK_d:
                    p1.set_direct('right')
                    p1.move_right()
                    p1.set_move_shield(True)
                if event.key == SDLK_a:
                    p1.set_direct('left')
                    p1.move_left()
                    p1.set_move_shield(True)
                if event.key == SDLK_w:
                    p1.set_direct('up')
                    p1.move_up()
                    p1.set_move_shield(True)
                if event.key == SDLK_s:
                    p1.set_direct('down')
                    p1.move_down()
                    p1.set_move_shield(True)
            if (p1.get_state() == 'IDLE' or p1.get_state() == 'MOVE') and p1.get_state() != 'ATTACK':
                if event.key == SDLK_j:
                    p1.attack()
            if p1.get_state() == states['IDLE']:
                pass
        if event.type == SDL_KEYUP:
            if p1.get_state() == states['MOVE']:
                if event.key == SDLK_d:
                    p1.set_move_flag(False,'right')
                if event.key == SDLK_a:
                    p1.set_move_flag(False,'left')
                if event.key == SDLK_w:
                    p1.set_move_flag(False,'up')
                if event.key == SDLK_s:
                    p1.set_move_flag(False,'down')
            if p1.get_state() == states['SSHIELD'] or p1.get_state() == 'SHEILDWALK':
                if event.key == SDLK_d:
                    p1.set_move_shield(False,'right')
                if event.key == SDLK_a:
                    p1.set_move_shield(False,'left')
                if event.key == SDLK_w:
                    p1.set_move_shield(False,'up')
                if event.key == SDLK_s:
                    p1.set_move_shield(False,'down')
                if event.key == SDLK_k:
                    p1.switch_state('IDLE')
                    p1.Holded_flag = False
        # event_queue = events





        

if __name__ == '__main__':
    open_canvas(Screen_size[0], Screen_size[1])
    # p1 = player()
    # p1.__init__('testname',100,10)
    p1 = Player('testname',100,5)
    mob = Monster(100,5,'baby_slime')
    game_world.add_object(p1,1)
    game_world.add_object(mob,1)
    background = load_image('sprite\stage\Background.png')
    current_time = time()
    while True:
        clear_canvas()
        input()

        newTime = time()
        frame_time = newTime - current_time
        current_time = newTime

        while frame_time > 0.0:
            deltatime = min(frame_time, dt)
            update()
            frame_time -= dt
            t += deltatime

        myRender()
        update_canvas()
        # delay(0.01)
    pass





# handle_events()
# frame = (frame + 1) % 8
# x += dir * 5

