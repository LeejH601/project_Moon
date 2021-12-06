from modules import *
# import main_state
# import start_state
import home_state

pico2d.open_canvas(Screen_size[0], Screen_size[1])
game_framework.run(home_state)
pico2d.close_canvas()
