from modules import *
import main_state

name = "TitleState"
image = None


def enter():
    global image, logoimage
    image = load_image('title.png')
    logoimage = load_image('GameLogo.png')


def exit():
    global image
    del(image)


def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        else:
            if (event.type, event.key) == (SDL_KEYDOWN, SDLK_ESCAPE):
                game_framework.quit()
            elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_SPACE):
                game_framework.change_state(main_state)


def draw():
    clear_canvas()
    draw_size = Screen_size[0]/image.w, Screen_size[1]/image.h
    image.draw(Screen_size[0]/2,Screen_size[1]/2, draw_size[0]*image.w, draw_size[1]*image.h)
    logoimage.draw(Screen_size[0]/4,Screen_size[1]/2, logoimage.w*2, logoimage.h*2)
    update_canvas()







def update(deletatime):
    pass


def pause():
    pass


def resume():
    pass






