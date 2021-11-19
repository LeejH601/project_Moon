
# layer 0: Background Objects
# layer 1: Foreground Objects
objects = [[],[]]


def add_object(o, layer):
    objects[layer].append(o)


def add_objects(l, layer):
    objects[layer] += l


def remove_object(o):
    for i in range(len(objects)):
        if o in objects[i]:
            objects[i].remove(o)
            del o
            break


def get_player_instacne():
    for i in range(len(objects)):
        _name = objects[1][i].get_name()
        # print(_name)
        try :
            if _name == 'player':
                return objects[1][i]
        except:
            print(objects[1][i])
    return None


def clear():
    for o in all_objects():
        del o
    for l in objects:
        l.clear()

def destroy():
    clear()
    objects.clear()


def all_objects():
    for i in range(len(objects)):
        for o in objects[i]:
            yield o

