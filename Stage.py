from random import randint
from Monster import *
from modules import *
from object import Object
import Server

class stage(Object):
    background_image = None
    rooms = []
    room_indexs = {}
    home = None
    home_image = None

    cur_room = None

    place_trigger = 0

    def __init__(self):
        if stage.background_image == None:
            stage.background_image = load_image('sprite\stage\Background.png')
        if stage.home_image == None: 
            stage.home_image = load_image('sprite\shop\shop_new_version_lv1_background_ok.png')
        game_world.add_object(self, 0)
        stage.place_trigger = 0
        stage.home = Room(100,stage.home_image,0)
        stage.set_name(self, 'stage')
        # stage.MakeRooms(1)
        # self.cur_room.room_in()
        # game_world.add_objects(self.cur_room.get_gateList(), 0)
        pass

    def get_name(self):
        return super().get_name()

    def in_to_dungeon():
        stage.MakeRooms(1)
        stage.place_trigger = 1
        stage.cur_room.room_in()

    def show_rooms_info(self):
        print('now_room: ', self.cur_room.get_ID())
        for i in stage.rooms:
            print(str(i.get_ID()) + " ",end='')
            i.show_gates_info()
            print('')

    def MakeRooms(level):
        healPlace_flag = False
        rm_count = random.randint(0,2) + 5 + level * 2
        n_id = 35
        stage.rooms.append(Room(n_id,stage.background_image, 1))
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
                        if len(stage.rooms)+1 == rm_count : stage.rooms.append(Room(new_roomId,stage.background_image, 3))
                        else : stage.rooms.append(Room(new_roomId,stage.background_image, 1))
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
        game_world.get_player_instacne().locate = [Screen_size[0]/2, Screen_size[1]/2]
        gates = self.cur_room.get_gateList()
        now_ID = self.cur_room.get_ID()
        new_ID = dir_ID
        for gate in gates:
            if new_ID == gate.get_linked_ID():
                self.cur_room.room_out()
                self.cur_room = self.rooms[self.room_indexs[new_ID]]
                self.cur_room.room_in()
                pass
        self.show_rooms_info(self)
        pass

    def update(self, deltatime):
        if stage.place_trigger == 1:
            stage.cur_room.update(deltatime)
        else:
            stage.home.update(deltatime)

    def rendering(self):
        if stage.place_trigger == 1:
            stage.cur_room.rendering()
        else:
            stage.home.rendering()

            
    

class Room(Object):
    image = None

    dungeon_light = None
    dungeon_shadow = None

    bk_light = None
    bk_shadow = None
    
    def __init__(self, _id, _bkimage, flag):
        # if Room.Door_image == None:
        #     Room.Door_image = []
        #     for i in range(1, 11+1):
        #         Room.Door_image.append(load_image('golem_basic_doors'+str(i)+'.png'))
        if Room.dungeon_light == None:
            Room.dungeon_light = []
            for i in range(1, 8):
                Room.dungeon_light.append( load_image('sprite\stage\Golem_Lights_' + str(i) +'.png'))
        if Room.dungeon_shadow == None:
            Room.dungeon_shadow = []
            for i in range(1, 7):
                Room.dungeon_shadow.append( load_image('sprite\stage\Golem_Shadow_' + str(i) +'.png'))
        self.room_Id = _id
        Room.image = _bkimage
        self.bk_light = Room.dungeon_light[randint(0, 6)]
        self.bk_shadow = Room.dungeon_shadow[randint(0, 5)]
        self.gates = []
        self.flag = flag
        if flag == 1:
            room_pattern = randint(0,2)
            # room_pattern = 2
            self.monster_list = []
            if room_pattern == 0:
                self.monster_list.append(SmallSlime(200, 500, 50, 3))
                self.monster_list.append(SmallSlime(200, 200, 50, 3))
                self.monster_list.append(SmallSlime(800, 200, 50, 3))
                self.monster_list.append(SmallSlime(800, 500, 50, 3))
                pass
            elif room_pattern == 1:
                self.monster_list.append(GollemKnight(200, 500, 100, 3))
                self.monster_list.append(SmallSlime(200, 200, 25, 3))
                self.monster_list.append(GollemKnight(800, 200, 100, 3))
                self.monster_list.append(SmallSlime(800, 500, 25, 3))
                pass
            elif room_pattern == 2:
                self.monster_list.append(BigSlime(500, 300, 50, 3))
                self.monster_list.append(SmallSlime(200, 500, 25, 3))
                self.monster_list.append(SmallSlime(200, 200, 25, 3))
                self.monster_list.append(SmallSlime(800, 200, 25, 3))
                self.monster_list.append(SmallSlime(800, 500, 25, 3))
        elif flag == 3:
            self.monster_list = []
            self.monster_list.append(GolemBoss(500, 300, 400, 3))
            #     pass
            # self.monster_list.append(GollemKnight(200, 400, 50, 5))
            # self.monster_list.append(BigSlime(600, 100, 50, 3))
        # self.monster_on_world()
        self.set_name('room')
        pass

    def room_in(self):
        self.monster_on_world()
        Server.monsters = self.monster_list
        

    def room_out(self):
        self.monster_out_world()
        Server.monsters = None

    def monster_on_world(self):
        game_world.add_objects(self.monster_list, 1)

    def monster_out_world(self):
        for i in range(len(self.monster_list)):
            game_world.remove_object(self.monster_list[i])

    def get_monsterList(self):
        return self.monster_list

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
        if self.flag == 1:
            self.image.draw_to_origin(-5,-5,Screen_size[0]+10, Screen_size[1]+10)
            self.bk_shadow.draw_to_origin(-5,-5,Screen_size[0]+10, Screen_size[1]+10)
            self.bk_light.draw_to_origin(-5,-5,Screen_size[0]+10, Screen_size[1]+10)
        else:
            self.image.draw_to_origin(0,0, self.image.w*s_size, self.image.h*s_size)
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
        self.set_name('gate')

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