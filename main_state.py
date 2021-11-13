import random
import json
import os
from Player import Player

from modules import *
import title_state



name = "MainState"


font = None


def enter():
    player = Player(Screen_size[0]/2, Screen_size[1]/2, 100,5)
    game_world.add_object(Player._instance, 1)


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


def update():
    for game_object in game_world.all_objects():
        game_object.update()


def draw():
    clear_canvas()
    for game_object in game_world.all_objects():
        game_object.rendering()
    update_canvas()





