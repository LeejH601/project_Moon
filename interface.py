from pico2d import *
from modules import Screen_size
import Server

class Interface:

    image_Health = None
    image_HealthBack = None
    image_Healthglass = None
    image_Gold = None
    gold_image_frame = 0

    def __init__(self) -> None:
        if Interface.image_Health == None:
            Interface.image_Health = load_image('sprite\\UI\RedBar.png')
        if Interface.image_HealthBack == None:
            Interface.image_HealthBack = load_image('sprite\\UI\BarBackground.png')
        if Interface.image_Healthglass == None:
            Interface.image_Healthglass = load_image('sprite\\UI\BarGlass.png')
        if Interface.image_Gold == None:
            Interface.image_Gold = []
            for i in range(1, 10):
                Interface.image_Gold.append(load_image('sprite\\UI\goldCoin%d.png' % i))
        
    
    def update(self, deltatime):
        Interface.gold_image_frame = (Interface.gold_image_frame + 9 * deltatime) % 9


    def rendering(self):
        Interface.image_HealthBack.clip_draw_to_origin(0, 0, 1024, 734, 20, Screen_size[1] - 71, 150, 50)
        w = Interface.image_Health.w
        dw = 150 / 100.0
        dx = Server.player.health / Server.player.max_health
        width = dx * dw * 100

        Interface.image_Health.clip_draw_to_origin(0,0, 1024, Interface.image_Health.h, 20, Screen_size[1] - 60, width, 50)
        Interface.image_Healthglass.clip_draw_to_origin(0, 0, 1024, 734, 20, Screen_size[1] - 71, 150, 50)


        Interface.image_Gold[int(Interface.gold_image_frame)].draw_to_origin(20, Screen_size[1] - 71)
        gold = Server.inventory.gold
        Server.font.draw(55, Screen_size[1] - 55, str(gold), (255, 255, 255))
        # print(gold)
        pass

    pass