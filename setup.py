from __future__ import absolute_import
from .objtypes import *

def two_way_exit(origin, direction1, direction2, destination):
    """Installs an Exit in """
    Exit(world[origin], direction1, world[destination]).install()
    Exit(world[destination], direction2, world[origin]).install()

places = ["grendels-den", "barker-library", "lobby-7", "10-250", "lobby-10", "eecs-hq", "eecs-ug-office", "edgerton-hall", "stata-center", "6001-lab", "building-13", "great-court", "student-center", "bexley", "baker", "legal-seafood", "graduation-stage", "34-301"]

exits =   [["lobby-10", "up", "down", "10-250"],
              ["grendels-den", "up", "down", "lobby-10"],
              ["10-250", "up", "down", "barker-library"],
              ["lobby-10", "west", "east", "lobby-7"],
              ["lobby-7", "west", "east", "student-center"],
              ["student-center", "south", "north", "bexley"],
              ["bexley", "west", "east", "baker"],
              ["lobby-10", "north", "south", "building-13"],
              ["lobby-10", "south", "north", "great-court"],
              ["building-13", "north", "south", "edgerton-hall"],
              ["edgerton-hall", "up", "down", "34-301"],
              ["34-301", "up", "down", "eecs-hq"],
              ["34-301", "east", "west", "stata-center"],
              ["stata-center", "north", "south", "stata-center"],
              ["stata-center", "up", "down", "stata-center"],
              ["eecs-hq", "west", "east", "eecs-ug-office"],
              ["edgerton-hall", "north", "south", "legal-seafood"],
              ["eecs-hq", "up", "down", "6001-lab"],
              ["legal-seafood", "east", "west", "great-court"],
              ["great-court", "up", "down", "graduation-stage"]
              ]

def create_world():
    """create_world() returns a list holding all installed Places (with Exits), Things, and Mobile_Things."""
    world = {}
    for p in places:
      world[p] = Place(p)
      world[p].install()

    map(two_way_exit, exits)
    # TODO factor out data into its own file and/or use a less clumsy structure to hold & install them
    # map(install, map(Thing, *things))
    
    Thing("blackboard", world["10-250"]).install()
    Thing("lovely-trees", world["great-court"]).install()
    Thing("flag-pole", world["great-court"]).install()
    
    Mobile_Thing("tons-of-code", world["baker"]).install()
    Mobile_Thing("problem-set", world["10-250"]).install()
    Mobile_Thing("recitation-problem", world["10-250"]).install()
    Mobile_Thing("sicp", world["stata-center"]).install()
    Mobile_Thing("engineering-book", world["barker-library"]).install()
    Mobile_Thing("diploma", world["graduation-stage"]).install()
    
    return world

    # TODO also refactor these, yikes
def populate_weapons(rooms):
    Weapon("chair-of-the-faculty", random.choice(rooms), 5).install()
    Weapon("student-riot", random.choice(rooms), 4).install()
    Weapon("sicp-book", random.choice(rooms), 2).install()
    Weapon("inflatable-lambda", random.choice(rooms), 3).install()
    Weapon("6001-quiz", random.choice(rooms), 3).install()
    Weapon("stick-of-chalk", random.choice(rooms), 1).install()
    return "populated-weapons"

def populate_players(rooms):
    names = ["ben-bitdiddle", "alyssa-hacker", "chuck-vest", "course-6-frosh", "lambda-man", "grumpy-grad-student"]
    vamp = random.choice(names)
    names.remove(vamp)
    k = random.choice(rooms.keys())
    Vampire(vamp, rooms[k], False).install()
    for each in names:
        Autonomous_Person(each, rooms[k], random.randint(0, 3), random.randint(0, 3)).install()
    return "populated-players"

def setup(name):
    clock.reset()
    clock.add_callback(Clock_CB("tick-printer", clock, "print_tick"))
    rooms = create_world()
    #populate_weapons(rooms)
    populate_players(rooms)
    me = Avatar(name, rooms[random.choice(rooms.keys())])
    screen.set_me(me)
    return me