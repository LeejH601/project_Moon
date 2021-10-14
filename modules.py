from pico2d import *
import random
from collections import defaultdict
from time import time

states = {'NONE': 'NONE','MOVE': 'MOVE','DEAD': 'DEAD','ATTACK': 'ATTACK', 'IDLE': 'IDLE', 'ROLL': 'ROLL', 'SSWORD': 'SSWORD'}
directs = {'up':0,'right':1,'down':2,'left':3}
