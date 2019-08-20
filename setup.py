import random

import data
import utilities as u
from objects import *


def create_world():
    """Return a dict holding all installed Places."""
    w: Dict[str, Place] = {}
    for p in data.places:
        w[p] = Place(p)

    return w


def create_things(world):
    rooms = list(world.values())

    for t in data.things:
        Thing(t['name'], world[t['place']])

    for m in data.mobile_things:
        Mobile_Thing(m['name'], world[m['place']])

    for h in data.holy_objects:
        Holy_Object(h, random.choice(rooms))

    for w in data.weapons:
        Weapon(w['name'], random.choice(rooms), w['damage'])

    for t in data.tools:
        Tool(t['name'], random.choice(rooms), t['magic'])


def create_exits(world):
    # TODO modify Exit to be more parallel to Weapon and Thing??
    """Install an Exit between two Places."""
    for e in data.exits:
        Exit(world[e['origin']], e['direction1'], world[e['destination']], e['magic'])
        Exit(world[e['destination']], e['direction2'], world[e['origin']], e['magic'])


def create_people(world):
    rooms = list(world.values())
    names = data.names
    vamp = random.choice(names)
    names.remove(vamp)
    Vampire(vamp, random.choice(rooms), None)
    for n in names:
        Autonomous_Person(n, random.choice(rooms))
    Oracle(random.choice(rooms))
    Slayer(random.choice(rooms))
    Hacker(random.choice(rooms))


def create_specials(w):
    for s in data.special_places:
        w[s] = Special_Location(s)


def setup():
    clock.reset()
    clock.add_callback(clock.print_tick)

    world = create_world()
    create_things(world)
    create_people(world)

    print('The Adventures of Buffer the Vampire Slayer')
    name = input('player name: ')
    player = Avatar(name, random.choice(list(world.values())))

    create_specials(world)
    create_exits(world)
    player.look()

    return world, player


world, player = setup()
everything: List[Thing] = list(world.values())
for p in world.values():
    everything.extend(p.things)

while True:
    action = input('What would you like to do? ')
    if action in ['q', 'quit', 'exit'] or player.health <= 0:
        break
    if action in data.directions.values():
        player.go(action)
    if action in data.directions.keys():
        player.go(data.directions[action])
    if action in ['i', 'inventory']:
        print('Inventory: ' + ', '.join(u.names(player.things)))
    if action in ['?', 'h', 'help']:
        print(dir(player))
    if action == "callbacks":
        print(clock.callbacks)
    if ' ' in action:
        verb, object = action.split(' ')
        if hasattr(player, verb):
            getattr(player, verb)(object)
        if verb == 'tick':
            run_clock(int(object))
        if verb == 'inspect':
            o = u.thingfind(object, everything)
            if o:
                print(vars(o))
    if hasattr(player, action):
        getattr(player, action)()
    else:
        pass
