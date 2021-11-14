from random import randint
from modules import *
from object import Object

class stage(Object):
    background_image = None
    rooms = []
    room_indexs = {}

    cur_room = None

    def __init__(self):
        if stage.background_image == None:
            stage.background_image = load_image('sprite\stage\Background.png')
        
        stage.MakeRooms(1)
        pass

    def show_rooms_info(self):
        for i in stage.rooms:
            print(str(i.get_ID()) + " ",end='')
            i.show_gates_info()
            print('')

    def MakeRooms(level):
        rm_count = random.randint(0,2) + 5 + level * 2
        n_id = 35
        stage.rooms.append(Room(n_id,stage.background_image))
        stage.cur_room = stage.rooms[0]
        ids = [-1,1,-10,10]
        while len(stage.rooms) < rm_count:
            flag = True
            while flag:
                dir = random.randint(0,3)
                new_roomId = n_id + ids[dir]
                adjacent_count = 0
                same_flag = False
                for i in stage.rooms:
                    if i.get_ID() == new_roomId:
                        same_flag = True
                        break
                if same_flag == False:
                    for i in stage.rooms:
                        t_id = i.get_ID()
                        if t_id == new_roomId+ids[0] or t_id == new_roomId+ids[1] or t_id == new_roomId+ids[2] or t_id == new_roomId+ids[3]:
                            adjacent_count += 1
                    if adjacent_count < 3:
                        stage.rooms.append(Room(new_roomId,stage.background_image))
                        stage.room_indexs[new_roomId] = len(stage.rooms)-1
                        flag = False
                room_index = random.randint(0,len(stage.rooms)-1)
                n_id = stage.rooms[room_index].get_ID()
                pass
            pass

        for i in range(len(stage.rooms)):
            n_ID = stage.rooms[i].get_ID()
            for rm in stage.rooms:
                t_id = rm.get_ID()
                if t_id == n_ID+ids[0] or t_id == n_ID+ids[1] or t_id == n_ID+ids[2] or t_id == n_ID+ids[3]:
                    stage.rooms[i].add_gate(t_id)
            pass


    def EnterRoom(self, dir_ID):
        gates = self.now_Room.get_gateList()
        now_ID = self.now_Room.get_ID()
        new_ID = now_ID + dir_ID
        if new_ID in gates:
            self.now_Room = self.rooms[self.rooms[new_ID]]
            pass
        pass

    def update(self, deltatime):
        stage.cur_room.update(deltatime)

    def rendering(self):
        stage.cur_room.rendering()

            
    

class Room(Object):
    moster_list = []
    Door_image = None
    
    def __init__(self, _id, _bkimage):
        # if Room.Door_image == None:
        #     Room.Door_image = []
        #     for i in range(1, 11+1):
        #         Room.Door_image.append(load_image('golem_basic_doors'+str(i)+'.png'))
        self.room_Id = _id
        Room.image = _bkimage
        self.gates = []
        pass

    def add_gate(self, _ID):
        self.gates.append(_ID)

    def get_gateList(self):
        return self.gates

    def show_gates_info(self):
        for i in self.gates:
            print(str(i) + " ",end='')

    def get_ID(self):
        return self.room_Id

    def update(self, deltatime):
        return super().update(deltatime)

    def rendering(self):
        self.image.draw_to_origin(-5,-5,Screen_size[0]+10, Screen_size[1]+10)
    pass

class Gate(object):
    pass

if __name__ == '__main__':
    open_canvas()
    test_stage = stage()
    test_stage.MakeRooms(1)
    test_stage.show_rooms_info()
    close_canvas()