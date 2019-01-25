from .objtypes import *
import data

def create_world():
    """create_world() returns a list holding all installed Places (with Exits), Things, and Mobile_Things."""
    world = {}
    for p in data.places:
      world[p] = Place(p)
      world[p].install()
    
    for e in data.exits:
      populate_exits(*e)
    
    for t in data.things:
      Thing(t['name'], world[t['place']]).install()
    
    for m in data.mobile_things:
      Mobile_Thing(m['name'], world[m['place']]).install()
    
    return world

# TODO modify Exit to be more parallel to Weapon and Thing??
def populate_exits(origin, direction1, direction2, destination):
    """Installs an Exit in """
    Exit(world[origin], direction1, world[destination]).install()
    Exit(world[destination], direction2, world[origin]).install()

def populate_weapons(rooms):
  for w in data.weapons:
    Weapon(w['name'], random.choice(rooms), w['damage']).install()
  return "populated-weapons"

def populate_players(rooms):
    names = data.names
    vamp = random.choice(names)
    names.remove(vamp)
    k = random.choice(list(rooms.keys()))
    Vampire(vamp, rooms[k], False).install()
    for each in names:
        Autonomous_Person(each, rooms[k], random.randint(0, 3), random.randint(0, 3)).install()
    return "populated-players"

# TODO get name from player input
def setup(name):
    clock.reset()
    clock.add_callback(Clock_CB("tick-printer", clock, "print_tick"))
    rooms = create_world()
    populate_weapons(rooms)
    populate_players(rooms)
    me = Avatar(name, rooms[random.choice(list(rooms.keys()))])
    screen.set_me(me)
    return me

screen = Screen()
setup('Talia')