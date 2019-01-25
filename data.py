names = ["ben-bitdiddle", "alyssa-hacker", "chuck-vest", "course-6-frosh", "lambda-man", "grumpy-grad-student"]

places = ["grendels-den", "barker-library", "lobby-7", "10-250", "lobby-10", "eecs-hq", "eecs-ug-office", "edgerton-hall", "stata-center", "6001-lab", "building-13", "great-court", "student-center", "bexley", "baker", "legal-seafood", "graduation-stage", "34-301"]

# TODO consider reformatting these as dicts
# [origin, direction1, direction2, destination],
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

# {'name': , 'place': },
things = [{'name': "blackboard", 'place': "10-250"}, 
  {'name': "lovely-trees", 'place': "great-court"}, 
  {'name': "flag-pole", 'place': "great-court"},]

# {'name': , 'place': },
mobile_things = [{'name': "tons-of-code", 'place': "baker"},
{'name': "problem-set", 'place': "10-250"},
{'name': "recitation-problem", 'place': "10-250"},
{'name': "sicp", 'place': "stata-center"},
{'name': "engineering-book", 'place': "barker-library"},
{'name': "diploma", 'place': "graduation-stage"},]

# {'name':, 'damage': },
weapons = [{'name': "chair-of-the-faculty", 'damage': 5}, 
  {'name': "student-riot", 'damage': 4}, 
  {'name': "sicp-book", 'damage': 2}, 
  {'name': "inflatable-lambda", 'damage': 3}, 
  {'name': "6001-quiz", 'damage': 3}, 
  {'name': "stick-of-chalk", 'damage': 1},]