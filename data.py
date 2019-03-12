from typing import Dict, List, Union

names: List[str] = ["ben-bitdiddle", "alyssa-hacker", "chuck-vest", "course-6-frosh", "lambda-man", "grumpy-grad-student"]

places: List[str] = ["grendels-den", "barker-library", "lobby-7", "10-250", "lobby-10", "eecs-hq", "eecs-ug-office", "edgerton-hall", "stata-center", "6001-lab", "building-13", "great-court", "student-center", "bexley", "baker", "legal-seafood", "graduation-stage", "34-301"]

# TODO consider reformatting these as dicts
# {'origin': , 'direction1': , 'direction2': , 'destination': },
exits: List[Dict[str, str]] = [
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
    {'origin': "great-court", 'direction1': "up", 'direction2': "down", 'destination': "graduation-stage"}
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

# {'name': , 'damage': },
weapons: List[Dict[str, Union[str, int]]] = [{'name': "chair-of-the-faculty", 'damage': 5},
                                             {'name': "student-riot", 'damage': 4},
                                             {'name': "sicp-book", 'damage': 2},
                                             {'name': "inflatable-lambda", 'damage': 3},
                                             {'name': "6001-quiz", 'damage': 3},
                                             {'name': "stick-of-chalk", 'damage': 1}, ]
