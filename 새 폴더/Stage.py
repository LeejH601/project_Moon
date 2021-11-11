from random import randint
from modules import *

class stage:
    background_image = None
    rooms = []
    room_indexs = {}
    def __init__(self):
        stage.background_image = load_image('sprite\stage\Background.png')
        pass

    def show_rooms_info(self):
        for i in self.rooms:
            print(str(i.get_ID()) + " ",end='')
            i.show_gates_info()
            print('')

    def MakeRooms(self, level):
        rm_count = random.randint(0,2) + 5 + level * 2
        n_id = 35
        self.rooms.append(Room(n_id,self.background_image))
        ids = [-1,1,-10,10]
        while len(self.rooms) < rm_count:
            flag = True
            while flag:
                dir = random.randint(0,3)
                new_roomId = n_id + ids[dir]
                adjacent_count = 0
                same_flag = False
                for i in self.rooms:
                    if i.get_ID() == new_roomId:
                        same_flag = True
                        break
                if same_flag == False:
                    for i in self.rooms:
                        t_id = i.get_ID()
                        if t_id == new_roomId+ids[0] or t_id == new_roomId+ids[1] or t_id == new_roomId+ids[2] or t_id == new_roomId+ids[3]:
                            adjacent_count += 1
                    if adjacent_count < 3:
                        self.rooms.append(Room(new_roomId,self.background_image))
                        self.room_indexs[new_roomId] = len(self.rooms)-1
                        flag = False
                room_index = random.randint(0,len(self.rooms)-1)
                n_id = self.rooms[room_index].get_ID()
                pass
            pass

        for i in range(len(self.rooms)):
            n_ID = self.rooms[i].get_ID()
            for rm in self.rooms:
                t_id = rm.get_ID()
                if t_id == n_ID+ids[0] or t_id == n_ID+ids[1] or t_id == n_ID+ids[2] or t_id == n_ID+ids[3]:
                    self.rooms[i].add_gate(t_id)
            pass


    def EnterRoom(self, dir_ID):
        gates = self.now_Room.get_gateList()
        now_ID = self.now_Room.get_ID()
        new_ID = now_ID + dir_ID
        if new_ID in gates:
            self.now_Room = self.rooms[self.rooms[new_ID]]
            pass
        pass
            
    

class Room:
    moster_list = []
    
    def __init__(self, _id, _bkimage):
        self.room_Id = _id
        self.image = _bkimage
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
    pass


if __name__ == '__main__':
    open_canvas()
    test_stage = stage()
    test_stage.MakeRooms(1)
    test_stage.show_rooms_info()
    close_canvas()