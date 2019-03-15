import random
import sys

import data
from objects import *


def create_world():
    """Return a dict holding all installed Places."""
    w: Dict[str, Place] = {}
    for p in data.places:
        w[p] = Place(p)
        w[p].install()

    return w


def create_things(world):
    for t in data.things:
        Thing(t['name'], world[t['place']]).install()

    for m in data.mobile_things:
        Mobile_Thing(m['name'], world[m['place']]).install()


def create_exits(world):
    # TODO modify Exit to be more parallel to Weapon and Thing??
    """Install an Exit between two Places."""
    for e in data.exits:
        Exit(world[e['origin']], e['direction1'], world[e['destination']]).install()
        Exit(world[e['destination']], e['direction2'], world[e['origin']]).install()


def create_weapons(world):
    for w in data.weapons:
        Weapon(w['name'], random.choice(list(world.values())), w['damage']).install()


def create_people(world):
    names = data.names
    vamp = random.choice(names)
    names.remove(vamp)
    Vampire(vamp, random.choice(list(world.values())), False).install()
    for n in names:
        Autonomous_Person(n, random.choice(list(world.values())), random.randint(0, 3), random.randint(0, 3)).install()


def setup():
    clock.reset()
    clock.add_callback(Callback("tick-printer", clock, "print_tick"))

    world = create_world()
    create_things(world)
    create_exits(world)
    # create_weapons(world)
    create_people(world)

    print('The Adventures of Buffer the Vampire Slayer')
    name = input('player name: ')
    player = Avatar(name, random.choice(list(world.values())))
    player.install()

    return world, player


world, player = setup()
while True:
    action = input('What would you like to do? ')
    if action in ['q', 'quit', 'exit']:
        break
    if action in ['up', 'down', 'north', 'south', 'east', 'west']:
        player.go(action)
    if action in ['i', 'inventory']:
        print(player.things)
    if action in ['?', 'h', 'help']:
        print(dir(player))
    if ' ' in action:
        verb, object = action.split(' ')
        if hasattr(player, verb):
            getattr(player, verb)(object)
    if hasattr(player, action):
        getattr(player, action)()
    else:
        pass
