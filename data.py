from typing import Dict, List, Union

directions: Dict[str, str] = {'n': 'north', 's': 'south', 'e': 'east', 'w': 'west', 'u': 'up', 'd': 'down'}

# directions: List[str] = ['up', 'down', 'north', 'south', 'east', 'west']

names: List[str] = ["ben-bitdiddle", "alyssa-hacker", "chuck-vest", "course-6-frosh", "lambda-man", "grumpy-grad-student", "jack-florey"]

places: List[str] = ["grendels-den", "barker-library", "lobby-7", "10-250", "lobby-10", "eecs-hq", "eecs-ug-office", "edgerton-hall", "stata-center", "6001-lab", "building-13", "great-court", "student-center", "bexley", "baker", "legal-seafood", "graduation-stage", "34-301", "senior-haus", "east-campus", "random-hall", "coffeehouse", "54-100", "roofdeck", 'pika']

special_places: List[str] = ["54-and-a-half", "the-point", "great-dome", "little-dome", "grad-student-office", "green-roof", "hell"]

# {'origin': , 'direction1': , 'direction2': , 'destination': },
# TODO implement logic so direction2 is the opposite of direction1
# here or in the install or init or create method?
exits: List[Dict[str, Union[str, int]]] = [
    {'origin': "lobby-10", 'direction1': "up", 'direction2': "down", 'destination': "10-250"},
    {'origin': "grendels-den", 'direction1': "up", 'direction2': "down", 'destination': "lobby-10"},
    {'origin': "10-250", 'direction1': "up", 'direction2': "down", 'destination': "barker-library"},
    {'origin': "lobby-10", 'direction1': "west", 'direction2': "east", 'destination': "lobby-7"},
    {'origin': "lobby-7", 'direction1': "west", 'direction2': "east", 'destination': "student-center"},
    {'origin': "student-center", 'direction1': "south", 'direction2': "north", 'destination': "bexley"},
    {'origin': "bexley", 'direction1': "west", 'direction2': "east", 'destination': "baker"},
    {'origin': "lobby-10", 'direction1': "north", 'direction2': "south", 'destination': "building-13"},
    {'origin': "lobby-10", 'direction1': "south", 'direction2': "north", 'destination': "great-court"},
    {'origin': "building-13", 'direction1': "north", 'direction2': "south", 'destination': "edgerton-hall"},
    {'origin': "edgerton-hall", 'direction1': "up", 'direction2': "down", 'destination': "34-301"},
    {'origin': "34-301", 'direction1': "up", 'direction2': "down", 'destination': "eecs-hq"},
    {'origin': "34-301", 'direction1': "east", 'direction2': "west", 'destination': "stata-center"},
    {'origin': "stata-center", 'direction1': "north", 'direction2': "south", 'destination': "stata-center"},
    {'origin': "stata-center", 'direction1': "up", 'direction2': "down", 'destination': "stata-center"},
    {'origin': "eecs-hq", 'direction1': "west", 'direction2': "east", 'destination': "eecs-ug-office"},
    {'origin': "edgerton-hall", 'direction1': "north", 'direction2': "south", 'destination': "legal-seafood"},
    {'origin': "eecs-hq", 'direction1': "up", 'direction2': "down", 'destination': "6001-lab"},
    {'origin': "legal-seafood", 'direction1': "east", 'direction2': "west", 'destination': "great-court"},
    {'origin': "great-court", 'direction1': "up", 'direction2': "down", 'destination': "graduation-stage"},
    {'origin': 'lobby-10', 'direction1': 'east', 'direction2': 'west', 'destination': '54-100'},
    {'origin': '54-100', 'direction1': 'east', 'direction2': 'west', 'destination': 'east-campus'},
    {'origin': 'east-campus', 'direction1': 'east', 'direction2': 'west', 'destination': 'senior-haus'},
    {'origin': 'student-center', 'direction1': 'up', 'direction2': 'down', 'destination': 'coffeehouse'},
    {'origin': 'student-center', 'direction1': 'north', 'direction2': 'south', 'destination': 'random-hall'},
    {'origin': 'random-hall', 'direction1': 'up', 'direction2': 'down', 'destination': 'roofdeck'},
    {'origin': 'student-center', 'direction1': 'west', 'direction2': 'east', 'destination': 'pika'},
    {'origin': 'random-hall', 'direction1': 'west', 'direction2': 'east', 'destination': 'pika'},
    {'origin': 'senior-haus', 'direction1': 'east', 'direction2': 'west', 'destination': 'grad-student-office', 'magic': 4},
    {'origin': 'east-campus', 'direction1': 'north', 'direction2': 'south', 'destination': 'the-point', 'magic': 3},
    {'origin': '54-100', 'direction1': 'up', 'direction2': 'down', 'destination': 'green-roof', 'magic': 8},
    {'origin': '54-100', 'direction1': 'down', 'direction2': 'up', 'destination': '54-and-a-half', 'magic': 4},
    {'origin': 'lobby-7', 'direction1': 'up', 'direction2': 'down', 'destination': 'little-dome', 'magic': 3},
    {'origin': 'barker-library', 'direction1': 'up', 'direction2': 'down', 'destination': 'great-dome', 'magic': 8},
    {'origin': 'building-13', 'direction1': 'down', 'direction2': 'up', 'destination': 'hell', 'magic': 3},
    # {'origin': , 'direction1': , 'direction2': , 'destination': , 'magic': },
]

# {'name': , 'place': },
things: List[Dict[str, str]] = [{'name': "blackboard", 'place': "10-250"},
                                {'name': "lovely-trees", 'place': "great-court"},
                                {'name': "flag-pole", 'place': "great-court"}, ]

# {'name': , 'place': },
mobile_things: List[Dict[str, str]] = [{'name': "tons-of-code", 'place': "baker"},
                                       {'name': "problem-set", 'place': "10-250"},
                                       {'name': "recitation-problem", 'place': "10-250"},
                                       {'name': "sicp", 'place': "stata-center"},
                                       {'name': "engineering-book", 'place': "barker-library"},
                                       {'name': "diploma", 'place': "graduation-stage"}, ]

holy_objects: List[str] = ['crown-of-thorns', 'relic', 'holy-water', 'grail', 'holy-hand-grenade', 'rosary', 'shroud-of-turin', 'covenant-ark', 'cross']

# {'name': , 'damage': },
weapons: List[Dict[str, Union[str, int]]] = [{'name': "chair-of-the-faculty", 'damage': 5},
                                             {'name': "student-riot", 'damage': 4},
                                             {'name': "sicp-book", 'damage': 2},
                                             {'name': "inflatable-lambda", 'damage': 3},
                                             {'name': "6001-quiz", 'damage': 3},
                                             {'name': "stick-of-chalk", 'damage': 1}, ]

# for the gloomy-oracle, nostradamus
sayings: List[str] = ["The end is near!", "Someone set us up the bomb!", "Make your time. For great justice!", "Bah! Back in my day, we were REALLY hardcore!", "You will find love on Flag Day!", "Aaaahh! The fnords, they're everywhere!", "Moore's law will end soon", "Microsoft will destroy life as we know it", "I'll never finish my thesis"]

# for the hacker, jack-florey
shirts: List[str] = ['FVCKED BY THE INSTITVTE', 'Hackito Ergo Sum', "Jack Florey's Old No. 5 Roof and Tunnel Hacking", "James Tetazoo's Third East Travelling Animal Zoo", "I'm not here", "Sport Death: Only Life Can Kill You", "Follow Me to Baker House", "An MIT Education Opens Doors"]

# {'name': , 'magic': },
tools: List[Dict[str, Union[str, int]]] = [{'name': 'card', 'magic': 1},
                                           {'name': 'slide', 'magic': 3},
                                           {'name': 'lockpicks', 'magic': 5},
                                           {'name': 'maglight', 'magic': 2},
                                           {'name': 'leatherman', 'magic': 3},
                                           {'name': 'duct-tape', 'magic': 3},
                                           {'name': 'rope', 'magic': 6},
                                           {'name': 'carabiner', 'magic': 7}]
