from objtypes import *

def two_way_exit(origin, direction1, direction2, destination):
    Exit(origin, direction1, destination).install()
    Exit(destination, direction2, origin).install()

def create_world():
    world = {"grendels-den" : Place("grendels-den"),
    "barker-library" : Place("barker-library"),
    "lobby-7" : Place("lobby-7"),
    "10-250" : Place("10-250"),
    "lobby-10" : Place("lobby-10"),
    "eecs-hq" : Place("eecs-hq"),
    "eecs-ug-office" : Place("eecs-ug-office"),
    "edgerton-hall" : Place("edgerton-hall"),
    "stata-center" : Place("stata-center"),
    "6001-lab" : Place("6001-lab"),
    "building-13" : Place("building-13"),
    "great-court" : Place("great-court"),
    "student-center" : Place("student-center"),
    "bexley" : Place("bexley"),
    "baker" : Place("baker"),
    "legal-seafood" : Place("legal-seafood"),
    "graduation-stage" : Place("graduation-stage"),
    "34-301" : Place("34-301")}
    
    for each in world.keys():
        world[each].install()
    
    two_way_exit(world["lobby-10"], "up", "down", world["10-250"])
    two_way_exit(world["grendels-den"], "up", "down", world["lobby-10"])
    two_way_exit(world["10-250"], "up", "down", world["barker-library"])
    two_way_exit(world["lobby-10"], "west", "east", world["lobby-7"])
    two_way_exit(world["lobby-7"], "west", "east", world["student-center"])
    two_way_exit(world["student-center"], "south", "north", world["bexley"])
    two_way_exit(world["bexley"], "west", "east", world["baker"])
    two_way_exit(world["lobby-10"], "north", "south", world["building-13"])
    two_way_exit(world["lobby-10"], "south", "north", world["great-court"])
    two_way_exit(world["building-13"], "north", "south", world["edgerton-hall"])
    two_way_exit(world["edgerton-hall"], "up", "down", world["34-301"])
    two_way_exit(world["34-301"], "up", "down", world["eecs-hq"])
    two_way_exit(world["34-301"], "east", "west", world["stata-center"])
    two_way_exit(world["stata-center"], "north", "south", world["stata-center"])
    two_way_exit(world["stata-center"], "up", "down", world["stata-center"])
    two_way_exit(world["eecs-hq"], "west", "east", world["eecs-ug-office"])
    two_way_exit(world["edgerton-hall"], "north", "south", world["legal-seafood"])
    two_way_exit(world["eecs-hq"], "up", "down", world["6001-lab"])
    two_way_exit(world["legal-seafood"], "east", "west", world["great-court"])
    two_way_exit(world["great-court"], "up", "down", world["graduation-stage"])
    
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
    humans = names.remove(vamp)
    Vampire(vamp, random.choice(rooms), False).install()
    for eacn in humans:
        Autonomous_Person(each, random.choice(rooms), random.randint(0, 3), random.randint(0, 3)).install()
    return "populated-players"

def setup(name):
    clock.reset()
    clock.add_callback(Clock_CB("tick-printer", clock, "print_tick"))
    rooms = create_world()
    #populate_weapons(rooms)
    populate_players(rooms)
    me = Avatar(name, random.choice(rooms))
    screen.set_me(me)
    return "ready"