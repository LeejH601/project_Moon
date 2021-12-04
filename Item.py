from collections import defaultdict
from math import sqrt
from random import randint, random
from typing import DefaultDict
from pico2d.pico2d import Image, load_image
from pico2d.sdl2 import timer
from modules import PIXEL_PER_METER

Item_Id_Name_Table = { 
    10001: 'RichJelly', 10002: 'item_golem_core', 10003: 'item_GolemChisel', 10004: 'item_reinforced_steel_01',\
        20001: 'Item_Potion_Heal_3', \
            
}



class Item:

    image = None
    
    def __init__(self, _id, _name, _price = 10, _value = 0, x = None, y = None):
        self.item_Id = _id
        self.name = _name
        self.price = _price
        self.value = _value
        self.x, self.y = x, y
        self.vector = [randint(-1000000, 1000000)/1000000, randint(-1000000, 1000000)/1000000]
        vector_size = sqrt(self.vector[0]**2 + self.vector[1]**2)
        if not (vector_size == 0):
            self.vector = [self.vector[0]/vector_size, self.vector[1]/vector_size]
        if x and y:
            self.timer = 0.3
        else: self.timer = 0
        if Item.image == None:
            Item.image = defaultdict()
            for id in Item_Id_Name_Table.keys():
                Item.image[id] = load_image("sprite\item\\" + Item_Id_Name_Table[id] + '.png')

        RUN_SPEED_KMPH = 5.0
        RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
        RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
        self.RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)
        self.deltaspeed = -self.timer/self.RUN_SPEED_PPS
            
    def update(self, deltatime):
        if self.timer > 0:
            self.timer -= deltatime
            self.x, self.y = self.x + self.vector[0]*deltatime*self.RUN_SPEED_PPS, self.y + self.vector[1]*deltatime*self.RUN_SPEED_PPS
            self.RUN_SPEED_PPS -= self.deltaspeed
        pass

    def rendering(self, x = None, y = None):
        if x and y:
            Item.image[self.item_Id].draw(x, y, 25*2, 25*2)
        else:
            Item.image[self.item_Id].draw(self.x, self.y, Item.image[self.item_Id].w*2, Item.image[self.item_Id].h*2)


    def get_rect(self):
        return self.x, self.y, self.x + Item.image[self.item_Id].w*2, self.y + Item.image[self.item_Id].h*2



    pass


class equip(Item):

    def __init__(self, _id, _name,  _atk, _dff, _spd ,_price = 10):
        super().__init__(_id, _name, _price=_price)
        self.atk, self.dff, self.spd = _atk, _dff, _spd



    pass


