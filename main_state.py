import random
import json
import os
from Player import Player
from Stage import stage

from modules import *
import title_state



name = "MainState"


font = None


def enter():
    player = Player(Screen_size[0]/2, Screen_size[1]/2, 100,5)
    
    _stage = stage()
    game_world.add_object(Player._instance, 1)
    # game_world.add_object(stage(), 0)
    print(game_world.objects)
    stage.in_to_dungeon()
    # stage.show_rooms_info(stage)


def exit():
    game_world.clear()


def pause():
    pass


def resume():
    pass


def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        else:
            Player._instance.handle_event(event)
    pass


def update(deltatime):
    for game_object in game_world.all_objects():
        game_object.update(deltatime)

    if stage.place_trigger == 1:
        gates = stage.cur_room.get_gateList()
        for gate in gates:
            if collider(gate, Player._instance):
                # print("!!!collsion!!!!")
                stage.EnterRoom(stage, gate.get_linked_ID())


def draw():
    clear_canvas()
    for game_object in game_world.all_objects():
        game_object.rendering()
    update_canvas()



def collider(a, b):
    left_a, bottom_a, right_a, top_a = a.get_rect()
    left_b, bottom_b, right_b, top_b = b.get_rect()

    if left_a > right_b: return False
    if right_a < left_b: return False
    if top_a < bottom_b: return False
    if bottom_a > top_b: return False
    

    return True

