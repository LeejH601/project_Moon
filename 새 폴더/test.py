#from os import get_exec_path
import time
import multiprocessing
from object import *




    

def myRender():    
    global p1
    while True:
        clear_canvas()
        #character.clip_draw(frame * 100, 100 * 1, 100, 100, x, 90)
        p1.sprite_idle_down[p1.animation_frame].clip_composite_draw(0, 0 , 24, 41, 0, 'c', 300, 400,72,123)
        update_canvas()
        delay(0.01)


def update(queues):
    while True:
        player = queues.get()
        player.animation_frame = (player.animation_frame+1) % 9
        print(player.animation_frame)
        queues.put(player)
        delay(0.1)



        

if __name__ == '__main__':
    open_canvas()
    p1 = player('testname',100,10)
    queues = multiprocessing.Queue()
    queues.put(p1)
    if queues.empty():
        print('000000')
    #process_render = multiprocessing.Process(name="renderProcess",target=myRender)
    process_update = multiprocessing.Process(name="updateProcess",target=update,args=(queues,))

    #process_render.start()
    process_update.start()
    while True:
        clear_canvas()
        #character.clip_draw(frame * 100, 100 * 1, 100, 100, x, 90)
        _player = queues.get()
        _player.sprite_idle_down[_player.animation_frame].clip_composite_draw(0, 0 , 24, 41, 0, 'c', 300, 400,72,123)
        queues.put(_player)
        update_canvas()
        get_events()
        delay(0.01)
    pass





# handle_events()
# frame = (frame + 1) % 8
# x += dir * 5

