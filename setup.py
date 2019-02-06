import random
import sys

import data
from objects import *


def create_world():
    """Return a dict holding all installed Places (with Exits), Things, and Mobile_Things."""
    w = {}
    for p in data.places:
        w[p] = Place(p)
        w[p].install()

    for e in data.exits:
        populate_exits(*e)

    for t in data.things:
        Thing(t['name'], w[t['place']]).install()

    for m in data.mobile_things:
        Mobile_Thing(m['name'], w[m['place']]).install()

    return w


def populate_exits(origin: str, direction1: str, direction2: str, destination: str):
    # TODO modify Exit to be more parallel to Weapon and Thing??
    """Install an Exit between two Places."""
    global world
    w = world.places
    Exit(w[origin], direction1, w[destination]).install()
    Exit(w[destination], direction2, w[origin]).install()


def populate_weapons(rooms):
    for w in data.weapons:
        Weapon(w['name'], random.choice(rooms.values()), w['damage']).install()


def populate_players(rooms):
    names = data.names
    vamp = random.choice(names)
    names.remove(vamp)
    k = random.choice(rooms.values())
    Vampire(vamp, rooms[k], False).install()
    for each in names:
        Autonomous_Person(each, rooms[k], random.randint(0, 3), random.randint(0, 3)).install()


def setup():
    global world
    world.places = create_world()

    clock = Clock()
    clock.reset()
    clock.add_callback(Callback("tick-printer", clock, "print_tick"))

    print('The Adventures of Buffer the Vampire Slayer')
    name = input('player name: ')
    player = Avatar(name, random.choice(world.places.values()))
    world.player = player

    # populate_weapons(world.places)
    populate_players(world.places)

    return world, clock


world = World()
world, clock = setup()
while True:
    # global world, clock
    action = input('What would you like to do?')
    if action == 'q':
        break
    if action in ['up', 'down', 'north', 'south', 'east', 'west']:
        world.player.go(action)
    if action == 'look':
        world.player.look()
