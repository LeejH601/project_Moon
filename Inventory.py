import pico2d
from pico2d.pico2d import Font
from Item import *
from modules import Screen_size
import Server

class Inventory:
    
    inven_player = None
    inven_bag = None

    inven_cursor = 0

    handing_item = None

    back_image = None
    image_rect_size = [523, 271]

    Top_place = [185, 530]

    box_size = 25*2

    box_interval = 10*2

    def __init__(self) -> None:
        
        Inventory.inven_player = [ Item_box(i,0) for i in range(5)]
        Inventory.inven_bag = [ Item_box(i, i/5 + 1) for i in range(15)]
        if Inventory.back_image == None:
            Inventory.back_image = load_image('sprite\inventory\SpriteAtlasTexture-inventory (Group 2)-1024x1024-fmt25.png')

        test_item1 = Item(10001, Item_Id_Name_Table[10001], 10)
        test_item2 = Item(10002, Item_Id_Name_Table[10002], 10)
        test_item3 = Item(10003, Item_Id_Name_Table[10003], 10)
        test_item4 = Item(10004, Item_Id_Name_Table[10004], 10)
        test_item5 = Item(20001, Item_Id_Name_Table[20001], 10)

        Inventory.add_item(test_item1)
        Inventory.add_item(test_item2)
        Inventory.add_item(test_item3)
        Inventory.add_item(test_item4)
        Inventory.add_item(test_item3)
        Inventory.add_item(test_item3)
        Inventory.add_item(test_item3)
        Inventory.add_item(test_item3)
        Inventory.add_item(test_item3)
        Inventory.add_item(test_item5)
        pass


    def update(self, deltatime):
        pass
        

    def rendering(self):
        Inventory.back_image.clip_draw(501, 0, 523, 271, Screen_size[0]/2, Screen_size[1]/2, Inventory.image_rect_size[0]*2, Inventory.image_rect_size[1]*2 )
        for inven in Inventory.inven_player:
            inven.rendering()
        for inven in Inventory.inven_bag:
            inven.rendering()
        # Inventory.back_image.draw_to_origin(0,0)
        pass

    
    def add_item(item):
        flag, inven_ref = Inventory.check_add_bag_place(item)
        if flag:
            inven_ref.insertItem(item)


    def on_handing_of_item():
        if Inventory.handing_item == None:
            Inventory.handing_item = Item_box()
            Inventory.handing_item.insertItem(Inventory.Popitem_by_cursor())
            

    
    def Popitem_by_cursor():
        if Inventory.inven_cursor < 5:
            return Inventory.inven_player[Inventory.inven_cursor].PopItem()
        else:
            return Inventory.inven_bag[Inventory.inven_cursor - 5].PopItem()


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
            self.correction_place = 20
        else:
            self.correction_place = 0
        self.rect_size = None

    def update(self):
        pass

    def rendering(self):
        if self.item:
            x, y = self.rendering_place
            x, y = x*Inventory.box_interval + x*Inventory.box_size + Inventory.Top_place[0], Inventory.Top_place[1] - y*Inventory.box_interval - y*Inventory.box_size - self.correction_place
            self.item.rendering(x, y)
            # Font.draw(Font, x, y, str(self.count))


    def is_add_item(self):
        if self.count < self.Max_count:
            return True
        return False

    def insertItem(self, item):
        
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
        if self.item and (self.item.item_Id == item.item_Id or item == 'any') :
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
        