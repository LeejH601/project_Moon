from math import dist, sqrt
from random import sample
from object import *
from BehaviorTree import LeafNode, SelectorNode, SequenceNode, BehaviorTree
import Server


class Monster(Object):

    
    
    def __init__(self, _x, _y, _health, _speed, _direct=[0, -1]):
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

    def Set_Speed(self, _speed = 1):
        RUN_SPEED_KMPH = _speed
        RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
        RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
        self.RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)  

    def reset_pps(self):
        self.RUN_SPEED_PPS = None

    def update(self, deltatime):
        self.m_deltatime = deltatime
        self.bt.run()

        # if self.vector != 0:
        #     print(0)
        self.frame = (self.frame + self.Actions.FRAMES_PER_ACTION *self.Actions.ACTION_PER_TIME * deltatime) % self.Actions.FRAMES_PER_ACTION
        self.locate[0] += self.RUN_SPEED_PPS * math.cos(self.vector) * deltatime
        self.locate[1] += self.RUN_SPEED_PPS * math.sin(self.vector) * deltatime


    def rendering(self):
        w, h = self.cur_images[self.direct[0]*10+self.direct[1]][int(self.frame)].w*s_size, self.cur_images[self.direct[0]*10+self.direct[1]][int(self.frame)].h*s_size
        self.cur_images[self.direct[0]*10+self.direct[1]][int(self.frame)].draw_to_origin(self.locate[0], self.locate[1], w, h)

    def build_behavior_tree(self):
        pass

    def Find_Player(self):
        distance = (Server.player.locate[0] - self.locate[0])**2 + (Server.player.locate[1] - self.locate[1])**2
        if distance < (PIXEL_PER_METER * 10)**2:
            self.Set_Speed(self.speed)
            return BehaviorTree.SUCCESS
        else:
            self.reset_pps()
            return BehaviorTree.FAIL

    def move_to_player(self):
        self.vector = math.atan2(Server.player.locate[1] - self.locate[1], Server.player.locate[0] - self.locate[0])
        return BehaviorTree.RUNNING
        pass

    def check_my_health(self):
        if self.health <= 0.0:
            return BehaviorTree.SUCCESS
        return BehaviorTree.FAIL
        pass

    def motioning_of_Dead(self):
        if self.Timer_Dead <= 0.0:
            return BehaviorTree.SUCCESS
        else:
            return BehaviorTree.RUNNING
        pass

    def dead(self):
        self.is_dead = True
        return BehaviorTree.SUCCESS
        pass

    def check_Hit(self):
        pass
    
    def Hit(self):
        pass

    def Attack_to_Player(self):
        self.RUN_SPEED_PPS = 0.0
        if self.Timer_Attack <= 0.0:
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
        super().__init__(_x, _y, _health, _speed, _direct=_direct)
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
        
        self.build_behavior_tree()

    def update(self, deltatime):
        return super().update(deltatime)

    def rendering(self):
        return super().rendering()

    def collider(self, my_rect, b):
        left_a, bottom_a, right_a, top_a = my_rect
        left_b, bottom_b, right_b, top_b = b.get_rect()

        if left_a > right_b: return False
        if right_a < left_b: return False
        if top_a < bottom_b: return False
        if bottom_a > top_b: return False
    
        return True

    def move_to_player(self):
        self.cur_images = SmallSlime.image_move
        self.Actions = SmallSlime.MoveAction
        left_a, bottom_a, right_a, top_a = self.get_rect()
        my_rect = (left_a - 50, bottom_a - 50, right_a + 50, top_a + 50)
        if self.collider(my_rect, Server.player) :
            # if self.atk_delay <= 0.0:
                self.Timer_Attack = self.Actions.TIME_PER_ACTION
                return BehaviorTree.SUCCESS
        return super().move_to_player()

    def Attack_to_Player(self):
        self.cur_images = SmallSlime.image_attack
        self.Actions = SmallSlime.AttackAction
        return super().Attack_to_Player()

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
        Hit_node = LeafNode('Hit', self.hit)

        Chase_and_Attack_node = SequenceNode('IdleAndAttack')
        chase_node = SequenceNode('Chase')
        Find_player_node = LeafNode('FindPlayer', self.Find_Player)
        move_to_player_node = LeafNode('MoveToPlayer',self.move_to_player)
        attack_to_player_node = LeafNode('AttackToPlayer', self.Attack_to_Player)

        Idle_node = LeafNode('Idle', self.Idle)

        Idle_and_Chase_node.add_children(Check_Dead_node, Chase_and_Attack_node, Idle_node)
        # Idle_and_Chase_node.add_children(Check_Dead_node, Check_Hit_node, Chase_and_Attack_node, Idle_node)
        Check_Dead_node.add_children(Check_Health_node, motion_of_Dead_node, Dead_node)
        Check_Hit_node.add_children(Check_Crash_node, Hit_node)
        Chase_and_Attack_node.add_children(chase_node, attack_to_player_node)
        chase_node.add_children(Find_player_node, move_to_player_node)

        self.bt = BehaviorTree(Idle_and_Chase_node)





    pass