from collections import defaultdict
from typing import DefaultDict
from pico2d.pico2d import Image, load_image


Item_Id_Name_Table = { 
    10001: 'RichJelly', 10002: 'item_golem_core', 10003: 'item_GolemChisel', 10004: 'item_reinforced_steel_01',\
        20001: 'Item_Potion_Heal_3', \
            
}

class Item:

    image = None
    
    def __init__(self, _id, _name, _price = 10, _value = 0):
        self.item_Id = _id
        self.name = _name
        self.price = _price
        self.value = _value
        if Item.image == None:
            Item.image = defaultdict()
            for id in Item_Id_Name_Table.keys():
                Item.image[id] = load_image("sprite\item\\" + Item_Id_Name_Table[id] + '.png')
    
    def update(self, deltatime):
        pass

    def rendering(self, x, y):
        Item.image[self.item_Id].draw(x, y, 25*2, 25*2)




    pass


class equip(Item):

    def __init__(self, _id, _name,  _atk, _dff, _spd ,_price = 10):
        super().__init__(_id, _name, _price=_price)
        self.atk, self.dff, self.spd = _atk, _dff, _spd



    pass


