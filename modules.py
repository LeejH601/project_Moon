from pico2d import *
import random
from collections import defaultdict
import math
import game_world
import game_framework


PIXEL_PER_METER = (10.0 / 0.1)

states = {'NONE': 'NONE','MOVE': 'MOVE','DEAD': 'DEAD','ATTACK': 'ATTACK', 'SATTACK': 'SATTACK','IDLE': 'IDLE', 'ROLL': 'ROLL', 'SSWORD': 'SSWORD', 'SSHIELD': 'SSHIELD','HSHIELD': 'HSHIELD', 'SHEILDWALK': 'SHEILDWALK'}
directs = {'up':0,'right':1,'down':2,'left':3}
Screen_size = x, y = 1160, 728
s_size = 2

item_price_table = {
    10001: 10, 10002: 100, 10003: 50, 10004: 150,\
        20001: 50,
}

