from random import randint
from Player import Player
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
        game_world.add_object(self, 0)
        stage.MakeRooms(1)
        # game_world.add_objects(self.cur_room.get_gateList(), 0)
        pass

    def show_rooms_info(self):
        print('now_room: ', self.cur_room.get_ID())
        for i in stage.rooms:
            print(str(i.get_ID()) + " ",end='')
            i.show_gates_info()
            print('')

    def MakeRooms(level):
        rm_count = random.randint(0,2) + 5 + level * 2
        n_id = 35
        stage.rooms.append(Room(n_id,stage.background_image))
        stage.room_indexs[n_id] = 0
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
        Player._instance.locate = [Screen_size[0]/2, Screen_size[1]/2]
        gates = self.cur_room.get_gateList()
        now_ID = self.cur_room.get_ID()
        new_ID = dir_ID
        for gate in gates:
            if new_ID == gate.get_linked_ID():
                self.cur_room = self.rooms[self.room_indexs[new_ID]]
                pass
        self.show_rooms_info(self)
        pass

    def update(self, deltatime):
        stage.cur_room.update(deltatime)

    def rendering(self):
        stage.cur_room.rendering()

            
    

class Room(Object):
    moster_list = []
    
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
        ngate = Gate(_ID, self.room_Id)
        self.gates.append(ngate)
        # game_world.add_object(ngate, 0)

    def get_gateList(self):
        return self.gates

    def show_gates_info(self):
        for i in self.gates:
            i.my_info()

    def get_ID(self):
        return self.room_Id

    def update(self, deltatime):
        return super().update(deltatime)

    def rendering(self):
        self.image.draw_to_origin(-5,-5,Screen_size[0]+10, Screen_size[1]+10)
        for gate in self.gates:
            gate.rendering()
        pass

class Gate(Object):
    image = None

    def __init__(self, lk_id, my_id):
        direct = [(my_id - lk_id) // 10, (my_id - lk_id) % 10]
        if direct == [-1, 9] :
            direct = [0, -1]
        
        self.Linked_id = lk_id
        self.my_id = my_id
        if Gate.image == None:
            Gate.image = []
            for i in range(1, 11+1):
                Gate.image.append(load_image('sprite\stage\golem_basic_doors'+str(i)+'.png'))
        super().__init__(0,0,1,1, direct)
        if self.direct == [0,-1]: # 0
            self.locate = [Screen_size[0] / 2 , self.image[0].h]
            self.rad = math.pi
        elif self.direct == [0, 1]: # 180
            self.locate = [Screen_size[0] / 2, Screen_size[1] - self.image[0].h]
            self.rad = 0
        elif self.direct == [-1,0]: # -90
            self.locate = [self.image[0].h , Screen_size[1] / 2]
            self.rad = math.pi/2
        elif self.direct == [1, 0]: # 90
            self.locate = [Screen_size[0] - self.image[0].h, Screen_size[1] / 2]
            self.rad = -math.pi/2


        pass

    def my_info(self):
        print(str(self.Linked_id) + " ",end='')

    def get_my_ID(self):
        return self.room_Id

    def get_linked_ID(self):
        return self.Linked_id

    def update(self, deltatime):
        return super().update(deltatime)

    def rendering(self):
        # print(self.locate)
        self.image[0].rotate_draw(self.rad ,*self.locate,Gate.image[0].w*s_size/2, Gate.image[0].h*s_size/2)

    def get_rect(self):
        return self.locate[0] - 20, self.locate[1] - 20, self.locate[0] + 20, self.locate[1] + 20
    
    pass

if __name__ == '__main__':
    open_canvas()
    stage()
    # stage.MakeRooms(1)
    stage.show_rooms_info(stage)
    close_canvas()