#from os import get_exec_path
import time
from object import *


animation_rate = 0
    

def myRender():    
    global p1
    clear_canvas()
    #character.clip_draw(frame * 100, 100 * 1, 100, 100, x, 90)
    p1.rendering()
    update_canvas()


def update():
    p1.update()
    # print(player.animation_frame)


def input():
    global p1
    events = get_events()
    for event in events:
        if event.type == SDL_KEYDOWN:
            print(p1.get_state())
            if p1.get_state() == states['IDLE'] or p1.get_state() == states['MOVE']:
                if event.key == SDLK_d:
                    p1.set_direct('right')
                    p1.move_right
                    p1.set_move_flag(True)
                elif event.key == SDLK_a:
                    p1.set_direct('left')
                    p1.move_left
                    p1.set_move_flag(True)
                elif event.key == SDLK_w:
                    p1.set_direct('up')
                    p1.move_up
                    p1.set_move_flag(True)
                elif event.key == SDLK_s:
                    p1.set_direct('down')
                    p1.move_down
                    p1.set_move_flag(True)
                elif event.key == SDLK_SPACE:
                    p1.set_Roll()
            if p1.get_state() == 'IDLE' and p1.get_state() != 'ATTACK':
                if event.key == SDLK_j:
                    p1.attack()
            if p1.get_state() == states['IDLE']:
                pass
        elif event.type == SDL_KEYUP:
            if p1.get_state() == states['MOVE']:
                if event.key == SDLK_d:
                    p1.set_move_flag(False)
                elif event.key == SDLK_a:
                    p1.set_move_flag(False)
                elif event.key == SDLK_w:
                    p1.set_move_flag(False)
                elif event.key == SDLK_s:
                    p1.set_move_flag(False)





        

if __name__ == '__main__':
    open_canvas(1920,1080)
    p1 = player('testname',100,10)

    while True:
        clear_canvas()
        input()
        update()
        myRender()
        update_canvas()
        delay(0.01)
    pass





# handle_events()
# frame = (frame + 1) % 8
# x += dir * 5

