from pico2d import *
import random
from collections import defaultdict
import math
import game_world
import game_framework


PIXEL_PER_METER = (10.0 / 0.2)

states = {'NONE': 'NONE','MOVE': 'MOVE','DEAD': 'DEAD','ATTACK': 'ATTACK', 'SATTACK': 'SATTACK','IDLE': 'IDLE', 'ROLL': 'ROLL', 'SSWORD': 'SSWORD', 'SSHIELD': 'SSHIELD','HSHIELD': 'HSHIELD', 'SHEILDWALK': 'SHEILDWALK'}
directs = {'up':0,'right':1,'down':2,'left':3}
Screen_size = x, y = 1160, 728
s_size = 3



