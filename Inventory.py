import pico2d
from pico2d.pico2d import Font, debug_print
from pico2d import *
from Item import *
from modules import Screen_size
import Server

RIGHT_DOWN, LEFT_DOWN, RIGHT_UP, LEFT_UP, SPACE, TOP_UP, TOP_DOWN, BOTTOM_UP, BOTTOM_DOWN, HANDLING_DOWN, HANDLING_UP = range(11)


key_event_table = {
    (SDL_KEYDOWN, SDLK_d): RIGHT_DOWN,
    (SDL_KEYDOWN, SDLK_a): LEFT_DOWN,
    (SDL_KEYUP, SDLK_d): RIGHT_UP,
    (SDL_KEYUP, SDLK_a): LEFT_UP,
    (SDL_KEYDOWN, SDLK_w): TOP_DOWN,
    (SDL_KEYDOWN, SDLK_s): BOTTOM_DOWN,
    (SDL_KEYUP, SDLK_w): TOP_UP,
    (SDL_KEYUP, SDLK_s): BOTTOM_UP,
    (SDL_KEYDOWN, SDLK_j): HANDLING_DOWN,
    (SDL_KEYDOWN, SDLK_k): HANDLING_UP,
}

class Inventory:
    handing_item = None

    slot_effect_image = None
    back_image = None
    
    inven_cursor = 5
    
    inven_player = None
    inven_bag = None
    
    image_rect_size = [523, 271]

    Top_place = [185, 530]

    box_size = 25*2

    box_interval = 10*2 + 1

    gold = 1000

    inven_potion = None

    def __init__(self) -> None:
        
        Inventory.inven_player = [ Item_box(i,0) for i in range(5)]
        Inventory.inven_bag = [ Item_box(i, i//5 + 1) for i in range(15)]
        Inventory.inven_potion = Potion_Box(10, 0)
        if Inventory.back_image == None:
            Inventory.back_image = load_image('sprite\inventory\SpriteAtlasTexture-inventory (Group 2)-1024x1024-fmt25.png')
        if Inventory.slot_effect_image == None:
            Inventory.slot_effect_image = load_image("sprite\inventory\Bag_slot_Affected.png")

        test_item1 = Item(10001, Item_Id_Name_Table[10001], 10)
        test_item2 = Item(10002, Item_Id_Name_Table[10002], 10)
        test_item3 = Item(10003, Item_Id_Name_Table[10003], 10)
        test_item4 = Item(10004, Item_Id_Name_Table[10004], 10)
        test_item5 = Item(20001, Item_Id_Name_Table[20001], 10, 30)

        Inventory.add_item(test_item1)
        Inventory.add_item(test_item2)
        Inventory.add_item(test_item3)
        Inventory.add_item(test_item4)
        Inventory.add_item(test_item3)
        Inventory.add_item(test_item3)
        Inventory.add_item(test_item3)
        Inventory.add_item(test_item3)
        Inventory.add_item(test_item3)

        Inventory.inven_potion.insertItem(test_item5)
        pass


    def update(self, deltatime):
        if Inventory.handing_item:
            Inventory.handing_item.rendering_place = Inventory.inven_cursor%5, Inventory.inven_cursor//5
            if Inventory.inven_cursor < 5: Inventory.handing_item.correction_place = 15
            else: Inventory.handing_item.correction_place = 30

    def rendering(self):
        debug_print(str(Inventory.inven_cursor))
        Inventory.back_image.clip_draw(501, 0, 523, 271, Screen_size[0]/2, Screen_size[1]/2, Inventory.image_rect_size[0]*2, Inventory.image_rect_size[1]*2 )
        Inventory.inven_potion.rendering()
        for i in range(len(Inventory.inven_player)):
            Inventory.inven_player[i].rendering()
            if i == Inventory.inven_cursor:
                x, y = Inventory.inven_player[i].rendering_place
                x = x % 5
                correction_place = Inventory.inven_player[i].correction_place
                x, y = x, y = x*Inventory.box_interval + x*Inventory.box_size + Inventory.Top_place[0], Inventory.Top_place[1] - y*Inventory.box_interval - y*Inventory.box_size - correction_place
                w, h = Inventory.slot_effect_image.w, Inventory.slot_effect_image.h
                Inventory.slot_effect_image.draw(x-1, y,w*2,h*2)
        for i in range(len(Inventory.inven_bag)):
            Inventory.inven_bag[i].rendering()
            if i+5 == Inventory.inven_cursor:
                x, y = Inventory.inven_bag[i].rendering_place
                x = x % 5
                correction_place = Inventory.inven_bag[i].correction_place
                x, y = x, y = x*Inventory.box_interval + x*Inventory.box_size + Inventory.Top_place[0], Inventory.Top_place[1] - y*Inventory.box_interval - y*Inventory.box_size - correction_place
                w, h = Inventory.slot_effect_image.w, Inventory.slot_effect_image.h
                Inventory.slot_effect_image.draw(x-1, y,w*2,h*2)
        if Inventory.handing_item:
            Inventory.handing_item.rendering()
        # Inventory.back_image.draw_to_origin(0,0)
        pass


    def handle_event(self, event):
        if (event.type, event.key) in key_event_table:
            key_event = key_event_table[(event.type, event.key)]
            if RIGHT_DOWN == key_event or LEFT_DOWN == key_event or TOP_DOWN == key_event or BOTTOM_DOWN == key_event:
                self.move_cursor(key_event)
            elif key_event == HANDLING_DOWN:
                Inventory.on_handing_of_item()
            elif key_event == HANDLING_UP:
                Inventory.down_handing_item()

    
    def move_cursor(self, event):
        if event == RIGHT_DOWN:
            Inventory.inven_cursor += 1
        elif event == LEFT_DOWN:
            Inventory.inven_cursor -= 1
        elif event == TOP_DOWN:
            Inventory.inven_cursor -= 5
        elif event == BOTTOM_DOWN:
            Inventory.inven_cursor += 5
        Inventory.inven_cursor = Inventory.inven_cursor % 20

    
    def add_item(item):
        flag, inven_ref = Inventory.check_add_bag_place(item)
        if flag:
            inven_ref.insertItem(item)


    def on_handing_of_item():
        if Inventory.handing_item == None:
            Inventory.handing_item = Item_box(Inventory.inven_cursor%5, Inventory.inven_cursor//5)
            Inventory.handing_item.insertItem(Inventory.Popitem_by_cursor())
        else:
            if Inventory.handing_item.count < Inventory.handing_item.Max_count:
                Inventory.handing_item.insertItem(Inventory.Popitem_by_cursor(Inventory.handing_item.item.item_Id))


    def down_handing_item():
        if Inventory.handing_item:
            if Inventory.inven_cursor < 5:
                Inventory.inven_player[Inventory.inven_cursor].insertItem(Inventory.handing_item.PopItem())
            else:
                Inventory.inven_bag[Inventory.inven_cursor - 5].insertItem(Inventory.handing_item.PopItem())
            if Inventory.handing_item.count <= 0:
                Inventory.handing_item = None
            

    
    def Popitem_by_cursor(item_id = None):
        if item_id == None:
            if Inventory.inven_cursor < 5:
                if Inventory.inven_player[Inventory.inven_cursor].item:
                    return Inventory.inven_player[Inventory.inven_cursor].PopItem()
            else:
                if Inventory.inven_bag[Inventory.inven_cursor - 5].item:
                    return Inventory.inven_bag[Inventory.inven_cursor - 5].PopItem()
        else:
            if Inventory.inven_cursor < 5:
                if Inventory.inven_player[Inventory.inven_cursor].item:
                    if Inventory.inven_player[Inventory.inven_cursor].item.item_Id == item_id:
                        return Inventory.inven_player[Inventory.inven_cursor].PopItem()
            else:
                if Inventory.inven_bag[Inventory.inven_cursor - 5].item:
                    if Inventory.inven_bag[Inventory.inven_cursor - 5].item.item_Id == item_id:
                        return Inventory.inven_bag[Inventory.inven_cursor - 5].PopItem()
            return None


    def check_add_bag_place(item):
        for inven in Inventory.inven_player:
            if inven.item and inven.item.item_Id == item.item_Id and inven.is_add_item() : return True, inven
        for inven in Inventory.inven_bag:
            if inven.item and inven.item.item_Id == item.item_Id and inven.is_add_item() : return True, inven

        for inven in Inventory.inven_player:
            if inven.item == None: return True, inven
        for inven in Inventory.inven_bag:
            if inven.item == None: return True, inven
        
        return False, None

    def show_inventory_for_Test():
        for inven in Inventory.inven_player:
            if inven.item:
                print(inven.item.name, inven.count)
        for inven in Inventory.inven_bag:
            if inven.item:
                print(inven.item.name, inven.count)

  


class Item_box:

    item_max_count_table = {
        10001: 10, 10002: 5, 10003: 5, 10004: 10,\
        20001: 5
    }


    def __init__(self, x = -1, y = -1) :
        self.item = None
        self.count = 0
        self.Max_count = None
        self.rendering_place = x, y
        if y > 0:
            self.correction_place = 15
        else:
            self.correction_place = 0
        self.rect_size = None
        

    def update(self):
        pass

    def rendering(self):
        if self.item:
            x, y = self.rendering_place
            x = x % 5
            x, y = x*Inventory.box_interval + x*Inventory.box_size + Inventory.Top_place[0], Inventory.Top_place[1] - y*Inventory.box_interval - y*Inventory.box_size - self.correction_place
            self.item.rendering(x, y)
            Server.font.draw(x+12,y-15,str(self.count))
            # Font.draw(Font, x, y, str(self.count))


    def is_add_item(self):
        if self.count < self.Max_count:
            return True
        return False

    def insertItem(self, item):
        if item:
            if self.Max_count == None:
                self.Max_count = Item_box.item_max_count_table[item.item_Id]
            if self.item == None:
                self.count += 1
                self.item = item
                return True
            else:
                if self.item.item_Id == item.item_Id:
                    if self.count < self.Max_count:
                        self.count += 1
                        return True

        return False


    def PopItem(self, item = 'any'):
        if item == 'any':
            item = self.item
        if self.item and (self.item.item_Id == item.item_Id) :
            if self.count > 0:
                temp_item = self.item
                self.count -= 1
                if self.count == 0:
                    self.Max_count = None
                    self.item = None
                return temp_item
        
        return None


    def deleteItem(self, item = 'any'):
        if self.item and (self.item.item_Id == item.item_Id or item == 'any') :
            if self.count > 0:
                self.count -= 1
                if self.count == 0:
                    self.Max_count = None
                    self.item = None
                return True
        
        return False
        

class Potion_Box(Item_box):

    def __init__(self, x=-1, y=-1):
        super().__init__(x=Screen_size[0]/2 + 65*2, y=Screen_size[1]/2 + 85*2)

    def rendering(self):
        if self.item:
            x, y = self.rendering_place
            
            self.item.rendering(x, y)
            Server.font.draw(x+12,y-15,str(self.count))
            # Font.draw(Font, x, y, str(self.count))
    

        

if __name__ == '__main__':
    pico2d.open_canvas()
    print('test')

    test_item1 = Item(10001, Item_Id_Name_Table[10001], 10)
    test_item2 = Item(10002, Item_Id_Name_Table[10002], 10)
    test_item3 = Item(10003, Item_Id_Name_Table[10003], 10)
    test_item4 = Item(10004, Item_Id_Name_Table[10004], 10)

    Inventory()
    Inventory.add_item(test_item1)
    Inventory.add_item(test_item2)
    Inventory.add_item(test_item3)
    Inventory.add_item(test_item4)
    Inventory.add_item(test_item3)
    Inventory.add_item(test_item3)
    Inventory.add_item(test_item3)
    Inventory.add_item(test_item3)
    Inventory.add_item(test_item3)
    Inventory.show_inventory_for_Test()
    pico2d.close_canvas()
        