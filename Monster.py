from math import degrees, dist, sqrt
from random import sample
from Item import Item
from object import *
from BehaviorTree import LeafNode, SelectorNode, SequenceNode, BehaviorTree
import Server
from modules import item_price_table
from Item import Item_Id_Name_Table

drap_table = {
    0 : [10001],
    1 : [10002, 10003, 10004]
}


class Monster(Object):

    
    
    def __init__(self, _x, _y, _health, _speed, d_table, _direct=[0, -1], ):
        super().__init__(_x, _y, _health, _speed, _direct=_direct)
        # self.Set_Speed(_speed)
        self.cur_images = None
        self.Timer_Dead = 2.0
        self.is_dead = False
        self.bt = None
        self.Actions = None
        self.vector = [0, 0]
        self.Timer_Attack = 0.0
        self.m_deltatime = 0.0
        self.Atk = 0.0
        self.atk_delay = 0.0
        self.atk_rate = 0.0
        self.Timer_Hit = 0.0
        self.bounding_box = None
        self.is_myAtkHit = False
        self.is_stiffness = True
        self.Attack_Frame = 0
        self.now_offensing = False
        self.drap_table = d_table

        self.hit_sound = None
        self.atk_sound = None
        self.idle_sound = None

        self.hit_soundflag = True
        self.atk_soundflag = True
        self.idle_soundflag = True

        self.hit_able = True

    def Set_Speed(self, _speed = 1):
        RUN_SPEED_KMPH = _speed
        RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
        RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
        self.RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)  

    def reset_pps(self):
        self.RUN_SPEED_PPS = None

    def update(self, deltatime):
        self.m_deltatime = deltatime
        self.atk_delay -= self.m_deltatime
        self.bt.run()

        # if self.vector != 0:
        #     print(0)
        # print( 'mobdirect: ',self.direct)
        self.frame = (self.frame + self.Actions.FRAMES_PER_ACTION *self.Actions.ACTION_PER_TIME * deltatime) % self.Actions.FRAMES_PER_ACTION
        self.locate[0] += self.RUN_SPEED_PPS * math.cos(self.vector) * deltatime
        self.locate[1] += self.RUN_SPEED_PPS * math.sin(self.vector) * deltatime
        self.myclamp()


    def rendering(self):
        if self.cur_images:
            w, h = self.cur_images[self.direct[0]*10+self.direct[1]][int(self.frame)].w*s_size, self.cur_images[self.direct[0]*10+self.direct[1]][int(self.frame)].h*s_size
            self.cur_images[self.direct[0]*10+self.direct[1]][int(self.frame)].draw_to_origin(self.locate[0], self.locate[1], w, h)
        # draw_rectangle(*self.get_rect())
        if self.bounding_box:
            # draw_rectangle(*self.bounding_box)
            pass
            

    def build_behavior_tree(self):
        pass

    
    def collider(self, my_rect, b):
        left_a, bottom_a, right_a, top_a = my_rect
        left_b, bottom_b, right_b, top_b = b.get_rect()

        if left_a > right_b: return False
        if right_a < left_b: return False
        if top_a < bottom_b: return False
        if bottom_a > top_b: return False
    
        return True

    def set_hitsound(self, sound):
        self.hit_sound = sound
    
    def set_atksound(self, sound):
        self.atk_sound = sound

    def Find_Player(self):
        if self.atk_soundflag and self.hit_soundflag and self.idle_soundflag:
            if self.idle_sound:
                self.idle_sound.play()
            self.idle_soundflag = False
        if self.is_dead : return BehaviorTree.FAIL
        distance = (Server.player.locate[0] - self.locate[0])**2 + (Server.player.locate[1] - self.locate[1])**2
        if distance < (PIXEL_PER_METER * 10)**2:
            self.Set_Speed(self.speed)
            return BehaviorTree.SUCCESS
        else:
            self.reset_pps()
            return BehaviorTree.FAIL

    def move_to_player(self):
        if self.is_dead : return BehaviorTree.FAIL
        self.vector = math.atan2(Server.player.locate[1] - self.locate[1], Server.player.locate[0] - self.locate[0])
        degree = abs(self.vector * 180 / math.pi)
        if degree < 45: self.direct = [1, 0]
        elif degree > 135: self.direct = [-1, 0]
        else:
            if self.vector > 0: self.direct = [0, 1]
            else: self.direct = [0, -1]

        # if abs(self.vector % (math.pi / 2)) <= 45*math.pi/180:
        #     if self.vector < math.pi/2: self.direct = [1, 0]
        #     else : self.direct = [-1, 0]
        # else :
        #     if self.vector > 0: self.direct = [0, 1]
        #     else : self.direct = [0, -1]
        # if self.vector > -(math.pi / 4) and self.vector <= (math.pi / 4): self.direct = [1, 0]
        # if self.vector > (math.pi/4) and self.vector <= (math.pi/2*3) : self.direct [0, 1]
        # if self.vector > (math.pi/2*3) and 
        return BehaviorTree.RUNNING
        pass

    def check_my_health(self):
        if self.health <= 0.0:
            if not self.is_dead : self.Timer_Dead = self.Actions.TIME_PER_ACTION
            return BehaviorTree.SUCCESS
        return BehaviorTree.FAIL
        pass

    def motioning_of_Dead(self):
        if self.Timer_Dead <= 0.0:
            return BehaviorTree.SUCCESS
        else:
            self.Timer_Dead -= self.m_deltatime
            return BehaviorTree.RUNNING
        

    def dead(self):
        if self.is_dead == False:
            drap_count = random.randint(1, len(self.drap_table))
            for i in range(drap_count):
                drap_index = random.randint(0, len(self.drap_table) - 1)
                drap_item_code = self.drap_table[drap_index]
                item = Item(drap_item_code, Item_Id_Name_Table[drap_item_code], item_price_table[drap_item_code], 0, self.locate[0], self.locate[1])
                game_world.add_object(item, 1)
                Server.fieldItem.append(item)
        self.is_dead = True
        return BehaviorTree.SUCCESS
        pass

    def check_Hit(self):
        if Server.player.bounding_box:
            if self.collider(self.get_rect(), Server.player):
                if self.hit_able:
                    self.health -= Server.player.Atk
                    self.hit_able = False
                print('mobhealth: ', self.health)
                if not self.is_stiffness :
                    return BehaviorTree.FAIL
                dl = [Server.player.direct[0]*(self.rect_size[0]/2), Server.player.direct[1]*(self.rect_size[1]/2)]
                self.locate[0] +=  dl[0]
                self.locate[1] +=  dl[1]
                self.myclamp()
                self.Timer_Hit = self.Actions.TIME_PER_ACTION
                if self.hit_soundflag:
                    if self.hit_sound:
                        self.hit_sound.play()
                    self.hit_soundflag = False
                    self.idle_soundflag = True
                return BehaviorTree.SUCCESS
        return BehaviorTree.FAIL
        
    
    def Hit(self):
        self.RUN_SPEED_PPS = 0.0
        if self.Timer_Hit <= 0.0:
            self.hit_soundflag = True
            self.hit_able = True
            return BehaviorTree.SUCCESS
        self.Timer_Hit -= self.m_deltatime
        return BehaviorTree.RUNNING

    def Attack_to_Player(self):
        if self.atk_soundflag:
            if self.atk_sound:
                self.atk_sound.play()
            self.atk_soundflag = False
            self.idle_soundflag = True
        self.RUN_SPEED_PPS = 0.0
        self.is_stiffness = False
        if self.collider(self.bounding_box, Server.player) and not self.is_myAtkHit and self.Attack_Frame <= int(self.frame):
            Server.player.demaged_by_mob(self.Atk)
            self.is_myAtkHit = True
        if self.Timer_Attack <= 0.0:
            self.atk_delay = self.atk_rate
            self.bounding_box = None
            self.is_stiffness = True
            self.now_offensing = False
            self.atk_soundflag = True
            return BehaviorTree.SUCCESS
        else:
            self.Timer_Attack -= self.m_deltatime
            return BehaviorTree.RUNNING


    def Idle(self):
        return BehaviorTree.SUCCESS
        pass

    pass


class SmallSlime(Monster):

    image_idle = None
    image_attack = None
    image_move = None
    image_hit = None
    image_dead = None

    hit_sound = None
    atk_sound = None

    class IdleAction:
        TIME_PER_ACTION = 1.0
        ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
        FRAMES_PER_ACTION = 1

    class AttackAction:
        TIME_PER_ACTION = 1
        ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
        FRAMES_PER_ACTION = 9

    class MoveAction:
        TIME_PER_ACTION = 1.0
        ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
        FRAMES_PER_ACTION = 5

    class HitAction:
        TIME_PER_ACTION = 1.0
        ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
        FRAMES_PER_ACTION = 1

    class DeadAction:
        TIME_PER_ACTION = 1.0
        ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
        FRAMES_PER_ACTION = 1


    def __init__(self, _x, _y, _health, _speed, _direct=[0, -1]):
        super().__init__(_x, _y, _health, _speed, drap_table[0], _direct=_direct)
        if SmallSlime.image_idle == None:
            SmallSlime.image_idle = defaultdict(list)
            SmallSlime.image_idle[-1].append(load_image('sprite\monster\Babyslime_idle.png'))
            SmallSlime.image_idle[1].append(load_image('sprite\monster\Babyslime_idle.png'))
            SmallSlime.image_idle[-10].append(load_image('sprite\monster\Babyslime_idle.png'))
            SmallSlime.image_idle[10].append(load_image('sprite\monster\Babyslime_idle.png'))

        if SmallSlime.image_attack == None:
            SmallSlime.image_attack = defaultdict(list)
            for i in range(0+1, 10):
                SmallSlime.image_attack[-1].append(load_image('sprite\monster\BabySlime_Attack_Down_'+str(i)+'.png'))
                SmallSlime.image_attack[1].append(load_image('sprite\monster\BabySlime_Attack_Up_'+str(i)+'.png'))
                SmallSlime.image_attack[-10].append(load_image('sprite\monster\BabySlime_Attack_Left_'+str(i)+'.png'))
                SmallSlime.image_attack[10].append(load_image('sprite\monster\BabySlime_Attack_Right_'+str(i)+'.png'))

        if SmallSlime.image_move == None:
            SmallSlime.image_move = defaultdict(list)
            for i in range(0+1, 6):
                SmallSlime.image_move[-1].append(load_image('sprite\monster\Babyslime_walk_'+str(i)+'.png'))
                SmallSlime.image_move[1].append(load_image('sprite\monster\Babyslime_walk_'+str(i)+'.png'))
                SmallSlime.image_move[-10].append(load_image('sprite\monster\Babyslime_walk_'+str(i)+'.png'))
                SmallSlime.image_move[10].append(load_image('sprite\monster\Babyslime_walk_'+str(i)+'.png'))

        if SmallSlime.image_hit == None:
            SmallSlime.image_hit = defaultdict(list)
            SmallSlime.image_hit[-1].append(load_image('sprite\monster\Babyslime_idle.png'))
            SmallSlime.image_hit[1].append(load_image('sprite\monster\Babyslime_idle.png'))
            SmallSlime.image_hit[-10].append(load_image('sprite\monster\Babyslime_idle.png'))
            SmallSlime.image_hit[10].append(load_image('sprite\monster\Babyslime_idle.png'))

        if SmallSlime.image_dead == None:
            SmallSlime.image_dead = defaultdict(list)
            SmallSlime.image_dead[-1].append(load_image('sprite\monster\deadenemy_slimes.png'))
            SmallSlime.image_dead[1].append(load_image('sprite\monster\deadenemy_slimes.png'))
            SmallSlime.image_dead[-10].append(load_image('sprite\monster\deadenemy_slimes.png'))
            SmallSlime.image_dead[10].append(load_image('sprite\monster\deadenemy_slimes.png'))

        SmallSlime.hit_sound = load_wav('sound\golem_dungeon_slime_hit.wav')
        SmallSlime.atk_sound = load_wav('sound\golem_dungeon_slime_attack.wav')
        SmallSlime.hit_sound.set_volume(32)
        SmallSlime.atk_sound.set_volume(32)
        
        self.set_hitsound(SmallSlime.hit_sound)
        self.set_atksound(SmallSlime.atk_sound)

        self.Atk = 5
        self.Set_rectSize(self.image_idle[-1][0].w*s_size, self.image_idle[-1][0].h*s_size)
        self.atk_rate = 3.0
        self.build_behavior_tree()

    def update(self, deltatime):
        return super().update(deltatime)

    def rendering(self):
        return super().rendering()

    def motioning_of_Dead(self):
        self.cur_images = SmallSlime.image_dead
        self.Actions = SmallSlime.DeadAction
        return super().motioning_of_Dead()

    def dead(self):
        self.cur_images = SmallSlime.image_dead
        self.Actions = SmallSlime.DeadAction
        return super().dead()


    def move_to_player(self):
        self.cur_images = SmallSlime.image_move
        self.Actions = SmallSlime.MoveAction
        left_a, bottom_a, right_a, top_a = self.get_rect()
        my_rect = (left_a - 25, bottom_a - 25, right_a + 25, top_a + 25)
        if self.collider(my_rect, Server.player) :
            self.RUN_SPEED_PPS = 0.0
            if self.atk_delay <= 0.0:
                self.Timer_Attack = self.Actions.TIME_PER_ACTION
                self.is_myAtkHit = False
                return BehaviorTree.SUCCESS
            return BehaviorTree.FAIL
        return super().move_to_player()

    def Attack_to_Player(self):
        self.Attack_Frame = 3
        self.cur_images = SmallSlime.image_attack
        self.Actions = SmallSlime.AttackAction
        x, y = self.locate[0] + self.direct[0] * self.rect_size[0], self.locate[1] + self.direct[1] * self.rect_size[1]
        self.bounding_box = [x, y, x + self.rect_size[0], y + self.rect_size[1]]
        return super().Attack_to_Player()
        
    def check_Hit(self):
        self.cur_images = SmallSlime.image_hit
        self.Actions = SmallSlime.HitAction
        return super().check_Hit()

    def Idle(self):
        self.cur_images = SmallSlime.image_idle
        self.Actions = SmallSlime.IdleAction
        return super().Idle()

    def build_behavior_tree(self):
        Idle_and_Chase_node = SelectorNode('IdleAndChase')

        Check_Dead_node = SequenceNode('CheckDead')
        Check_Health_node = LeafNode('CheckHealth', self.check_my_health)
        motion_of_Dead_node = LeafNode('motionDead', self.motioning_of_Dead)
        Dead_node = LeafNode('Dead', self.dead)

        Check_Hit_node = SequenceNode('CheckHit')
        Check_Crash_node = LeafNode('CheckCrash', self.check_Hit)
        Hit_node = LeafNode('Hit', self.Hit)

        Chase_and_Attack_node = SequenceNode('IdleAndAttack')
        chase_node = SequenceNode('Chase')
        Find_player_node = LeafNode('FindPlayer', self.Find_Player)
        move_to_player_node = LeafNode('MoveToPlayer',self.move_to_player)
        attack_to_player_node = LeafNode('AttackToPlayer', self.Attack_to_Player)

        Idle_node = LeafNode('Idle', self.Idle)

        Idle_and_Chase_node.add_children(Check_Dead_node, Check_Hit_node, Chase_and_Attack_node, Idle_node)
        Check_Dead_node.add_children(Check_Health_node, motion_of_Dead_node, Dead_node)
        Check_Hit_node.add_children(Check_Crash_node, Hit_node)
        Chase_and_Attack_node.add_children(chase_node, attack_to_player_node)
        chase_node.add_children(Find_player_node, move_to_player_node)

        self.bt = BehaviorTree(Idle_and_Chase_node)


class GollemKnight(Monster):

    image_idle = None
    image_attack = None
    image_move = None
    image_hit = None
    image_dead = None

    hit_sound = None
    atk_sound = None

    class IdleAction:
        TIME_PER_ACTION = 1.5
        ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
        FRAMES_PER_ACTION = 8

    class AttackAction:
        TIME_PER_ACTION = 2.5
        ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
        FRAMES_PER_ACTION = 13

    class MoveAction:
        TIME_PER_ACTION = 1.5
        ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
        FRAMES_PER_ACTION = 8

    class HitAction:
        TIME_PER_ACTION = 0.5
        ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
        FRAMES_PER_ACTION = 1

    class DeadAction:
        TIME_PER_ACTION = 2.0
        ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
        FRAMES_PER_ACTION = 4


    def __init__(self, _x, _y, _health, _speed, _direct=[0, -1]):
        super().__init__(_x, _y, _health, _speed,  drap_table[1], _direct=_direct)
        if GollemKnight.image_idle == None:
            GollemKnight.image_idle = defaultdict(list)
            for i in range(0+1, 9):
                GollemKnight.image_idle[-1].append(load_image('sprite\monster\Enemies_StoneSoldier_Floating_Down_'+str(i)+'.png'))
                GollemKnight.image_idle[1].append(load_image('sprite\monster\Enemies_StoneSoldier_Floating_Up_'+str(i)+'.png'))
                GollemKnight.image_idle[-10].append(load_image('sprite\monster\Enemies_StoneSoldier_Floating_Left_'+str(i)+'.png'))
                GollemKnight.image_idle[10].append(load_image('sprite\monster\Enemies_StoneSoldier_Floating_Right_'+str(i)+'.png'))
        

        if GollemKnight.image_attack == None:
            GollemKnight.image_attack = defaultdict(list)
            for i in range(0+1, 14):
                GollemKnight.image_attack[-1].append(load_image('sprite\monster\Enemies_GolemSoldier_Attack_Down_'+str(i)+'.png'))
                GollemKnight.image_attack[1].append(load_image('sprite\monster\Enemies_GolemSoldier_Attack_Up'+str(i)+'.png'))
                GollemKnight.image_attack[-10].append(load_image('sprite\monster\Enemies_GolemSoldier_Attack_Left_'+str(i)+'.png'))
                GollemKnight.image_attack[10].append(load_image('sprite\monster\Enemies_GolemSoldier_Attack_Right_'+str(i)+'.png'))
               

        if GollemKnight.image_move == None:
            GollemKnight.image_move = defaultdict(list)
            for i in range(0+1, 9):
                GollemKnight.image_move[-1].append(load_image('sprite\monster\Enemies_StoneSoldier_Floating_Down_'+str(i)+'.png'))
                GollemKnight.image_move[1].append(load_image('sprite\monster\Enemies_StoneSoldier_Floating_Up_'+str(i)+'.png'))
                GollemKnight.image_move[-10].append(load_image('sprite\monster\Enemies_StoneSoldier_Floating_Left_'+str(i)+'.png'))
                GollemKnight.image_move[10].append(load_image('sprite\monster\Enemies_StoneSoldier_Floating_Right_'+str(i)+'.png'))


        if GollemKnight.image_hit == None:
            GollemKnight.image_hit = defaultdict(list)
            for i in range(0+1, 2):
                GollemKnight.image_hit[-1].append(load_image('sprite\monster\Enemies_StoneSoldier_Floating_Down_'+str(i)+'.png'))
                GollemKnight.image_hit[1].append(load_image('sprite\monster\Enemies_StoneSoldier_Floating_Up_'+str(i)+'.png'))
                GollemKnight.image_hit[-10].append(load_image('sprite\monster\Enemies_StoneSoldier_Floating_Left_'+str(i)+'.png'))
                GollemKnight.image_hit[10].append(load_image('sprite\monster\Enemies_StoneSoldier_Floating_Right_'+str(i)+'.png'))

        if GollemKnight.image_dead == None:
            GollemKnight.image_dead = defaultdict(list)
            for i in range(0+1, 9):
                GollemKnight.image_dead[-1].append(load_image('sprite\monster\Enemies_StoneSoldier_Floating_Down_'+str(i)+'.png'))
                GollemKnight.image_dead[1].append(load_image('sprite\monster\Enemies_StoneSoldier_Floating_Up_'+str(i)+'.png'))
                GollemKnight.image_dead[-10].append(load_image('sprite\monster\Enemies_StoneSoldier_Floating_Left_'+str(i)+'.png'))
                GollemKnight.image_dead[10].append(load_image('sprite\monster\Enemies_StoneSoldier_Floating_Right_'+str(i)+'.png'))

        GollemKnight.hit_sound = load_wav('sound\golem_dungeon_golem_crash.wav')
        # GollemKnight.atk_sound = load_wav('sound\golem_dungeon_slime_attack.wav')
        GollemKnight.hit_sound.set_volume(32)
        # GollemKnight.atk_sound.set_volume(32)
        
        self.set_hitsound(GollemKnight.hit_sound)
        # self.set_atksound(GollemKnight.atk_sound)

        self.Atk = 5
        self.Set_rectSize(self.image_idle[-1][0].w*s_size, self.image_idle[-1][0].h*s_size)
        self.atk_rate = 3.0
        self.build_behavior_tree()

    def update(self, deltatime):
        return super().update(deltatime)

    def rendering(self):
        return super().rendering()

    def motioning_of_Dead(self):
        self.cur_images = GollemKnight.image_dead
        self.Actions = GollemKnight.DeadAction
        return super().motioning_of_Dead()

    def dead(self):
        self.cur_images = None
        self.Actions = GollemKnight.DeadAction
        return super().dead()


    def move_to_player(self):
        self.cur_images = GollemKnight.image_move
        self.Actions = GollemKnight.MoveAction
        left_a, bottom_a, right_a, top_a = self.get_rect()
        my_rect = (left_a - 25, bottom_a - 25, right_a + 25, top_a + 25)
        if self.collider(my_rect, Server.player) :
            self.RUN_SPEED_PPS = 0.0
            if self.atk_delay <= 0.0:
                self.Timer_Attack = self.Actions.TIME_PER_ACTION
                self.is_myAtkHit = False
                return BehaviorTree.SUCCESS
            return BehaviorTree.FAIL
        return super().move_to_player()

    def Attack_to_Player(self):
        self.Attack_Frame = 8
        self.cur_images = GollemKnight.image_attack
        self.Actions = GollemKnight.AttackAction
        x, y = self.locate[0] + self.direct[0] * self.rect_size[0], self.locate[1] + self.direct[1] * self.rect_size[1]
        self.bounding_box = [x, y, x + self.rect_size[0], y + self.rect_size[1]]
        return super().Attack_to_Player()
        
    def check_Hit(self):
        self.cur_images = GollemKnight.image_hit
        self.Actions = GollemKnight.HitAction
        return super().check_Hit()

    def Idle(self):
        self.cur_images = GollemKnight.image_idle
        self.Actions = GollemKnight.IdleAction
        return super().Idle()

    def build_behavior_tree(self):
        Idle_and_Chase_node = SelectorNode('IdleAndChase')

        Check_Dead_node = SequenceNode('CheckDead')
        Check_Health_node = LeafNode('CheckHealth', self.check_my_health)
        motion_of_Dead_node = LeafNode('motionDead', self.motioning_of_Dead)
        Dead_node = LeafNode('Dead', self.dead)

        Check_Hit_node = SequenceNode('CheckHit')
        Check_Crash_node = LeafNode('CheckCrash', self.check_Hit)
        Hit_node = LeafNode('Hit', self.Hit)

        Chase_and_Attack_node = SequenceNode('IdleAndAttack')
        chase_node = SequenceNode('Chase')
        Find_player_node = LeafNode('FindPlayer', self.Find_Player)
        move_to_player_node = LeafNode('MoveToPlayer',self.move_to_player)
        attack_to_player_node = LeafNode('AttackToPlayer', self.Attack_to_Player)

        Idle_node = LeafNode('Idle', self.Idle)

        Idle_and_Chase_node.add_children(Check_Dead_node, Check_Hit_node, Chase_and_Attack_node, Idle_node)
        Check_Dead_node.add_children(Check_Health_node, motion_of_Dead_node, Dead_node)
        Check_Hit_node.add_children(Check_Crash_node, Hit_node)
        Chase_and_Attack_node.add_children(chase_node, attack_to_player_node)
        chase_node.add_children(Find_player_node, move_to_player_node)

        self.bt = BehaviorTree(Idle_and_Chase_node)


class BigSlime(Monster):

    image_idle = None
    image_attack = None
    image_move = None
    image_hit = None
    image_dead = None

    hit_sound = None
    atk_sound = None

    class IdleAction:
        TIME_PER_ACTION = 1.0
        ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
        FRAMES_PER_ACTION = 1

    class AttackAction:
        TIME_PER_ACTION = 1.5
        ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
        FRAMES_PER_ACTION = 16

    class MoveAction:
        TIME_PER_ACTION = 1.0
        ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
        FRAMES_PER_ACTION = 8

    class HitAction:
        TIME_PER_ACTION = 1.0
        ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
        FRAMES_PER_ACTION = 1

    class DeadAction:
        TIME_PER_ACTION = 1.0
        ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
        FRAMES_PER_ACTION = 1


    def __init__(self, _x, _y, _health, _speed, _direct=[0, -1]):
        super().__init__(_x, _y, _health, _speed,  drap_table[0], _direct=_direct)
        if BigSlime.image_idle == None:
            BigSlime.image_idle = defaultdict(list)
            BigSlime.image_idle[-1].append(load_image('sprite\monster\slime_walk_1.png'))
            BigSlime.image_idle[1].append(load_image('sprite\monster\slime_walk_1.png'))
            BigSlime.image_idle[-10].append(load_image('sprite\monster\slime_walk_1.png'))
            BigSlime.image_idle[10].append(load_image('sprite\monster\slime_walk_1.png'))


        if BigSlime.image_attack == None:
            BigSlime.image_attack = defaultdict(list)
            for i in range(0+1, 17):
                BigSlime.image_attack[-1].append(load_image('sprite\monster\slime_hit_attack_'+str(i)+'.png'))
                BigSlime.image_attack[1].append(load_image('sprite\monster\slime_hit_attack_'+str(i)+'.png'))
                BigSlime.image_attack[-10].append(load_image('sprite\monster\slime_hit_attack_'+str(i)+'.png'))
                BigSlime.image_attack[10].append(load_image('sprite\monster\slime_hit_attack_'+str(i)+'.png'))


        if BigSlime.image_move == None:
            BigSlime.image_move = defaultdict(list)
            for i in range(0+1, 9):
                BigSlime.image_move[-1].append(load_image('sprite\monster\slime_walk_'+str(i)+'.png'))
                BigSlime.image_move[1].append(load_image('sprite\monster\slime_walk_'+str(i)+'.png'))
                BigSlime.image_move[-10].append(load_image('sprite\monster\slime_walk_'+str(i)+'.png'))
                BigSlime.image_move[10].append(load_image('sprite\monster\slime_walk_'+str(i)+'.png'))

            
        if BigSlime.image_hit == None:
            BigSlime.image_hit = defaultdict(list)
            BigSlime.image_hit[-1].append(load_image('sprite\monster\slime_walk_1.png'))
            BigSlime.image_hit[1].append(load_image('sprite\monster\slime_walk_1.png'))
            BigSlime.image_hit[-10].append(load_image('sprite\monster\slime_walk_1.png'))
            BigSlime.image_hit[10].append(load_image('sprite\monster\slime_walk_1.png'))


        if BigSlime.image_dead == None:
            BigSlime.image_dead = defaultdict(list)
            BigSlime.image_dead[-1].append(load_image('sprite\monster\deadenemy_slimes.png'))
            BigSlime.image_dead[1].append(load_image('sprite\monster\deadenemy_slimes.png'))
            BigSlime.image_dead[-10].append(load_image('sprite\monster\deadenemy_slimes.png'))
            BigSlime.image_dead[10].append(load_image('sprite\monster\deadenemy_slimes.png'))

        BigSlime.hit_sound = load_wav('sound\\bigslime_hit.wav')
        BigSlime.atk_sound = load_wav('sound\\bigslime_split.wav')
        BigSlime.hit_sound.set_volume(32)
        BigSlime.atk_sound.set_volume(32)
        
        self.set_hitsound(BigSlime.hit_sound)
        self.set_atksound(BigSlime.atk_sound)

        self.Atk = 5
        self.Set_rectSize(self.image_idle[-1][0].w*s_size, self.image_idle[-1][0].h*s_size)
        self.atk_rate = 3.0
        self.build_behavior_tree()

    def update(self, deltatime):
        return super().update(deltatime)

    def rendering(self):
        return super().rendering()

    def motioning_of_Dead(self):
        self.cur_images = BigSlime.image_dead
        self.Actions = BigSlime.DeadAction
        return super().motioning_of_Dead()

    def dead(self):
        self.cur_images = BigSlime.image_dead
        self.Actions = BigSlime.DeadAction
        return super().dead()


    def move_to_player(self):
        self.cur_images = BigSlime.image_move
        self.Actions = BigSlime.MoveAction
        left_a, bottom_a, right_a, top_a = self.get_rect()
        my_rect = (left_a - 15, bottom_a - 15, right_a + 15, top_a + 15)
        if self.collider(my_rect, Server.player) :
            self.RUN_SPEED_PPS = 0.0
            if self.atk_delay <= 0.0:
                self.Timer_Attack = self.Actions.TIME_PER_ACTION
                self.is_myAtkHit = False
                return BehaviorTree.SUCCESS
            return BehaviorTree.FAIL
        return super().move_to_player()

    def Attack_to_Player(self):
        self.Attack_Frame = 3
        self.cur_images = BigSlime.image_attack
        self.Actions = BigSlime.AttackAction
        x, y = self.locate[0] + self.rect_size[0]/2, self.locate[1] +self.rect_size[1]/2
        self.bounding_box = [x - self.rect_size[0], y - self.rect_size[1], x + self.rect_size[0], y + self.rect_size[1]]
        return super().Attack_to_Player()
        
    def check_Hit(self):
        self.cur_images = BigSlime.image_hit
        self.Actions = BigSlime.HitAction
        return super().check_Hit()

    def Idle(self):
        self.cur_images = BigSlime.image_idle
        self.Actions = BigSlime.IdleAction
        return super().Idle()

    def build_behavior_tree(self):
        Idle_and_Chase_node = SelectorNode('IdleAndChase')

        Check_Dead_node = SequenceNode('CheckDead')
        Check_Health_node = LeafNode('CheckHealth', self.check_my_health)
        motion_of_Dead_node = LeafNode('motionDead', self.motioning_of_Dead)
        Dead_node = LeafNode('Dead', self.dead)

        Check_Hit_node = SequenceNode('CheckHit')
        Check_Crash_node = LeafNode('CheckCrash', self.check_Hit)
        Hit_node = LeafNode('Hit', self.Hit)

        Chase_and_Attack_node = SequenceNode('IdleAndAttack')
        chase_node = SequenceNode('Chase')
        Find_player_node = LeafNode('FindPlayer', self.Find_Player)
        move_to_player_node = LeafNode('MoveToPlayer',self.move_to_player)
        attack_to_player_node = LeafNode('AttackToPlayer', self.Attack_to_Player)

        Idle_node = LeafNode('Idle', self.Idle)

        Idle_and_Chase_node.add_children(Check_Dead_node, Check_Hit_node, Chase_and_Attack_node, Idle_node)
        Check_Dead_node.add_children(Check_Health_node, motion_of_Dead_node, Dead_node)
        Check_Hit_node.add_children(Check_Crash_node, Hit_node)
        Chase_and_Attack_node.add_children(chase_node, attack_to_player_node)
        chase_node.add_children(Find_player_node, move_to_player_node)

        self.bt = BehaviorTree(Idle_and_Chase_node)


class GolemBoss(Monster):

    image_idle = None
    image_attack = None
    image_move = None
    image_hit = None
    image_dead = None
    image_smash = None

    hit_sound = None
    atk_sound = None

    class IdleAction:
        TIME_PER_ACTION = 1.5
        ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
        FRAMES_PER_ACTION = 8

    class AttackAction:
        TIME_PER_ACTION = 1.8
        ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
        FRAMES_PER_ACTION = 15

    class MoveAction:
        TIME_PER_ACTION = 1.5
        ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
        FRAMES_PER_ACTION = 8

    class HitAction:
        TIME_PER_ACTION = 0.5
        ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
        FRAMES_PER_ACTION = 1

    class SmashAction:
        TIME_PER_ACTION = 1.5
        ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
        FRAMES_PER_ACTION = 15

    class DeadAction:
        TIME_PER_ACTION = 2.0
        ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
        FRAMES_PER_ACTION = 4


    def __init__(self, _x, _y, _health, _speed, _direct=[0, -1]):
        super().__init__(_x, _y, _health, _speed,  drap_table[1], _direct=_direct)
        if GolemBoss.image_idle == None:
            GolemBoss.image_idle = defaultdict(list)
            for i in range(0+1, 9):
                GolemBoss.image_idle[-1].append(load_image('sprite\Boss\GolemCorrupt_MiniBoss_Idle_Down_'+str(i)+'.png'))
                GolemBoss.image_idle[1].append(load_image('sprite\Boss\GolemCorrupt_MiniBoss_Idle_Up_'+str(i)+'.png'))
                GolemBoss.image_idle[-10].append(load_image('sprite\Boss\GolemCorrupt_MiniBoss_Idle_Left_'+str(i)+'.png'))
                GolemBoss.image_idle[10].append(load_image('sprite\Boss\GolemCorrupt_MiniBoss_Idle_Right_'+str(i)+'.png'))
        

        if GolemBoss.image_attack == None:
            GolemBoss.image_attack = defaultdict(list)
            for i in range(0+1, 16):
                GolemBoss.image_attack[-1].append(load_image('sprite\Boss\GolemCorrupt_MiniBoss_Sword_Down_'+str(i)+'.png'))
                GolemBoss.image_attack[1].append(load_image('sprite\Boss\GolemCorrupt_MiniBoss_Sword_Up_'+str(i)+'.png'))
                GolemBoss.image_attack[-10].append(load_image('sprite\Boss\GolemCorrupt_MiniBoss_Sword_Left_'+str(i)+'.png'))
                GolemBoss.image_attack[10].append(load_image('sprite\Boss\GolemCorrupt_MiniBoss_Sword_Right_'+str(i)+'.png'))

        
        if GolemBoss.image_smash == None:
            GolemBoss.image_smash = defaultdict(list)
            for i in range(0+1, 16):
                GolemBoss.image_smash[-1].append(load_image('sprite\Boss\GolemCorrupt_MiniBoss_Smash_Down_'+str(i)+'.png'))
                GolemBoss.image_smash[1].append(load_image('sprite\Boss\GolemCorrupt_MiniBoss_Smash_Up_'+str(i)+'.png'))
                GolemBoss.image_smash[-10].append(load_image('sprite\Boss\GolemCorrupt_MiniBoss_Smash_Left_'+str(i)+'.png'))
                GolemBoss.image_smash[10].append(load_image('sprite\Boss\GolemCorrupt_MiniBoss_Smash_Right_'+str(i)+'.png'))
               

        if GolemBoss.image_move == None:
            GolemBoss.image_move = GolemBoss.image_idle


        if GolemBoss.image_hit == None:
            GolemBoss.image_hit = GolemBoss.image_idle


        if GolemBoss.image_dead == None:
            GolemBoss.image_dead = GolemBoss.image_idle

        GolemBoss.hit_sound = load_wav('sound\golem_dungeon_golem_crash.wav')
        GolemBoss.atk_sound = load_wav('sound\Miniboss_golemwarrior_sword.wav')
        GolemBoss.idle_sound = load_wav('sound\Miniboss_golemwarrior_idle_corrupted.wav')
        GolemBoss.hit_sound.set_volume(32)
        GolemBoss.atk_sound.set_volume(32)
        GolemBoss.idle_sound.set_volume(32)

        self.set_hitsound(GolemBoss.hit_sound)
        self.set_atksound(GolemBoss.atk_sound)

        self.vector = 0
        self.Atk = 5
        self.atk_pettern = 0
        self.Set_rectSize(self.image_idle[-1][0].w*s_size, self.image_idle[-1][0].h*s_size)
        self.atk_rate = 3.0
        self.build_behavior_tree()
        

    def update(self, deltatime):
        debug_print(self.health)
        print(self.health)
        return super().update(deltatime)

    def rendering(self):
        return super().rendering()

    def motioning_of_Dead(self):
        self.cur_images = GolemBoss.image_dead
        self.Actions = GolemBoss.DeadAction
        return super().motioning_of_Dead()

    def dead(self):
        self.cur_images = None
        self.Actions = GolemBoss.DeadAction
        return super().dead()

    def Find_Player(self):
        if self.now_offensing:
            return BehaviorTree.SUCCESS
        return super().Find_Player()


    def move_to_player(self):
        if self.now_offensing:
            return BehaviorTree.SUCCESS
        self.cur_images = GolemBoss.image_move
        self.Actions = GolemBoss.MoveAction
        left_a, bottom_a, right_a, top_a = self.get_rect()
        my_rect = (left_a - 25, bottom_a - 25, right_a + 25, top_a + 25)
        if self.collider(my_rect, Server.player) :
            self.RUN_SPEED_PPS = 0.0
            if self.atk_delay <= 0.0:
                if not self.now_offensing:
                    self.atk_pettern = random.randint(0, 1)
                    if self.atk_pettern == 0:
                        self.Timer_Attack = self.AttackAction.TIME_PER_ACTION
                    else:
                        self.Timer_Attack = self.SmashAction.TIME_PER_ACTION
                    self.is_myAtkHit = False
                return BehaviorTree.SUCCESS
            else:
                self.now_offensing = False
            return BehaviorTree.FAIL
        return super().move_to_player()

    def Attack_to_Player(self):
        self.Attack_Frame = 8
        self.cur_images = GolemBoss.image_attack
        self.Actions = GolemBoss.AttackAction
        x, y = self.locate[0] + self.direct[0] * self.rect_size[0], self.locate[1] + self.direct[1] * self.rect_size[1]
        self.bounding_box = [x, y, x + self.rect_size[0], y + self.rect_size[1]]
        return super().Attack_to_Player()
        
    def check_Hit(self):
        self.cur_images = GolemBoss.image_hit
        self.Actions = GolemBoss.HitAction
        return super().check_Hit()

    def Idle(self):
        self.cur_images = GolemBoss.image_idle
        self.Actions = GolemBoss.IdleAction
        return super().Idle()

    def Smash(self):
        self.cur_images = GolemBoss.image_smash
        self.Actions = GolemBoss.SmashAction
        x, y = self.locate[0] + self.rect_size[0]/2, self.locate[1] + self.rect_size[1]/2
        if self.bounding_box == None:
            self.bounding_box = [x, y, x, y]
        if self.frame >= 5:   
            self.bounding_box = [self.bounding_box[0] - Screen_size[0]*self.m_deltatime/3, self.bounding_box[1] - Screen_size[1]*self.m_deltatime/3,\
                self.bounding_box[2] + Screen_size[0]*self.m_deltatime/3, self.bounding_box[3] + Screen_size[1]*self.m_deltatime/3]
        return super().Attack_to_Player()

    def Attack_Pattern(self):
        self.now_offensing = True
        if self.atk_pettern == 0:
            self.Attack_to_Player()
        else:
            self.Smash()

    def build_behavior_tree(self):
        Idle_and_Chase_node = SelectorNode('IdleAndChase')

        Check_Dead_node = SequenceNode('CheckDead')
        Check_Health_node = LeafNode('CheckHealth', self.check_my_health)
        motion_of_Dead_node = LeafNode('motionDead', self.motioning_of_Dead)
        Dead_node = LeafNode('Dead', self.dead)

        Check_Hit_node = SequenceNode('CheckHit')
        Check_Crash_node = LeafNode('CheckCrash', self.check_Hit)
        Hit_node = LeafNode('Hit', self.Hit)

        Chase_and_Attack_node = SequenceNode('IdleAndAttack')
        chase_node = SequenceNode('Chase')
        Find_player_node = LeafNode('FindPlayer', self.Find_Player)
        move_to_player_node = LeafNode('MoveToPlayer',self.move_to_player)

        Smash_or_Attack_node = LeafNode('SmashOrAttack', self.Attack_Pattern)
        # smash_node = LeafNode('Smash', self.Smash)
        # attack_to_player_node = LeafNode('AttackToPlayer', self.Attack_to_Player)

        Idle_node = LeafNode('Idle', self.Idle)

        Idle_and_Chase_node.add_children(Check_Dead_node, Check_Hit_node, Chase_and_Attack_node, Idle_node)
        Check_Dead_node.add_children(Check_Health_node, motion_of_Dead_node, Dead_node)
        Check_Hit_node.add_children(Check_Crash_node, Hit_node)
        Chase_and_Attack_node.add_children(chase_node, Smash_or_Attack_node)
        # Smash_or_Attack_node.add_children(smash_node, attack_to_player_node)
        chase_node.add_children(Find_player_node, move_to_player_node)

        self.bt = BehaviorTree(Idle_and_Chase_node)
