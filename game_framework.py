from time import time

deltatime = 0
t = 0.0
dt = 1 / 150.0
current_time = 0
frame_time = 0
accumulator = 0.0

class GameState:
    def __init__(self, state):
        self.enter = state.enter
        self.exit = state.exit
        self.pause = state.pause
        self.resume = state.resume
        self.handle_events = state.handle_events
        self.update = state.update
        self.draw = state.draw



class TestGameState:

    def __init__(self, name):
        self.name = name

    def enter(self):
        print("State [%s] Entered" % self.name)

    def exit(self):
        print("State [%s] Exited" % self.name)

    def pause(self):
        print("State [%s] Paused" % self.name)

    def resume(self):
        print("State [%s] Resumed" % self.name)

    def handle_events(self):
        print("State [%s] handle_events" % self.name)

    def update(self):
        print("State [%s] update" % self.name)

    def draw(self):
        print("State [%s] draw" % self.name)



running = None
stack = None


def change_state(state):
    global stack
    if (len(stack) > 0):
        stack[-1].exit()
        stack.pop()
    stack.append(state)
    state.enter()



def push_state(state):
    global stack
    if (len(stack) > 0):
        stack[-1].pause()
    stack.append(state)
    state.enter()



def pop_state():
    global stack
    if (len(stack) > 0):
        stack[-1].exit()
        stack.pop()

    if (len(stack) > 0):
        stack[-1].resume()



def quit():
    global running
    running = False


def run(start_state):
    global running, stack, t, deltatime, frame_time, dt, accumulator
    running = True
    stack = [start_state]
    start_state.enter()
    
    current_time = time()
    frame_time = time() - current_time

    while (running):
        stack[-1].handle_events()
        accumulator += frame_time
        while accumulator >= dt:
            # deltatime = min(frame_time, dt)
            # deltatime = min(frame_time, dt)
            stack[-1].update(dt)
            accumulator -= dt
            t += dt
        stack[-1].update(accumulator)
        stack[-1].draw()

        accumulator = 0
        # print(frame_time)

        # parameter = accumulator / dt
        
        # stack[-1].update(parameter)
        
        frame_time = time() - current_time
        current_time += frame_time

        

    while (len(stack) > 0):
        stack[-1].exit()
        stack.pop()


def test_game_framework():
    start_state = TestGameState('StartState')
    run(start_state)



if __name__ == '__main__':
    test_game_framework()