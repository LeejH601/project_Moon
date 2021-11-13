from modules import *
import main_state

pico2d.open_canvas(Screen_size[0], Screen_size[1])
game_framework.run(main_state)
pico2d.close_canvas()
