import random
import json
import os
from Inventory import Inventory
from Player import Player
from Stage import stage

from modules import *
import Server
import title_state



name = "HomeState"


font = None


def enter():
    if Server.player == None:
        player = Player(Screen_size[0]/2, Screen_size[1]/2, 100,5)
        Server.player = player
    game_world.add_object(Server.player, 1)
    if Server.stage == None:
        _stage = stage()
        Server.stage = _stage
    game_world.add_object(Server.stage, 0)
    # game_world.add_object(stage(), 0)
    print(game_world.objects)
    # stage.show_rooms_info(stage)
    if Server.inventory == None:
        _inventory = Inventory()
        Server.inventory = _inventory
    # game_world.add_object(_inventory, 2)
    if Server.font == None:
        font = Font("ENCR10B.TTF")
        Server.font = font



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
        elif event.type == SDL_KEYDOWN and event.key == SDLK_i:
            Server.inven_trigger = not Server.inven_trigger
            if Server.inven_trigger == True:
                game_world.add_object(Server.inventory, 2)
            else:
                game_world.remove_object(Server.inventory)
        else:
            if Server.inven_trigger:
                Server.inventory.handle_event(event)
            else:
                Player._instance.handle_event(event)
    pass


def update(deltatime):
    if not Server.inven_trigger:
        for game_object in game_world.all_objects():
            game_object.update(deltatime)
    else:
        Server.inventory.update(deltatime)


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

