# objsys.py
# Christalee Bieber, 2016
# cbieber@alum.mit.edu
#
# A Python implementation of a vampire-themed text adventure game, originally written in Scheme. I extended this game for Project 4, the Object-Oriented Adventure Game, during the Spring 2004 term of 6.001, Structure & Interpretation of Computer Programs. The original assignment and project files can be found here: http://sicp.ai.mit.edu/Spring-2004/projects/index.html
#
# This file provides a clock and a screen for objects in a simulation world.  Additional utility procedures are also provided.

# TODO skipping network-mode, whatever that is

class Screen(object):
    def __init__(self):
        self.deity_mode = True
        self.me = False
        self.name = "the-screen"
    
    def set_me(self, new_me):
        self.me = new_me
    
    def tell_world(self, text):
        print text
    # TODO right now just print everything / later do what??
    def tell_room(self, location, text):
        print location
        print text

screen = Screen()
# --------------------
# Clock
# 
# A Clock is an object with a notion of time, which it imparts to all objects that have asked for it.  It does this by invoking a list of CALLBACKs whenever the TICK method is invoked on the clock.  A CALLBACK is an action to invoke on each tick of the clock, by calling a method on an object

# TODO is this the most elegant way to handle callbacks?
        
class Clock(object):
    def __init__(self):
        self.name = "the-clock"
        self.time = 0
        self.callbacks = []
        self.removed_callbacks = []
    
    def install(self):
        self.add_callback(Clock_CB("tick-printer", self, "print_tick"))

    def reset(self):
        self.time = 0
        self.callbacks = []

    def tick(self):
        for each in reversed(self.callbacks):
            if each not in self.removed_callbacks:
                each.activate()
        self.removed_callbacks = [] # TODO does this do things corrrectly??
        self.time += 1
    
    def print_tick(self):
        screen.tell_world("---" + self.name + " Tick " + str(self.time) + "---")
    
    def add_callback(self, cb):
        if isinstance(cb, Clock_CB):
            if cb in self.callbacks:
                return "already-present"
            else:
                self.callbacks.append(cb)
        else:
            print "That is not a callback."

    def remove_callback(self, obj, cb_name):
        def rcb(x):
            if x.name == cb_name and x.object == obj:
                self.removed_callbacks.append(x)
                return False
            else:
                return True
        self.callbacks = filter(rcb, self.callbacks)
        return "removed"

# Clock callbacks
# 
# A Clock_CB is an object that stores a target object, method, and arguments.  When activated, it executes the method on the target object.  It can be thought of as a button that executes an action at every tick of the clock.

class Clock_CB(object):
    def __init__(self, name, obj, msg):
        self.name = name
        self.object = obj
        self.message = msg
        self.isInstalled = False
    
    def install(self):
        self.isInstalled = True
        print self.name + " installed!"
    
    def activate(self):
        getattr(self.object, self.message)()

clock = Clock()

def current_time():
    return clock.time

def run_clock(x):
    while x > 0:
        clock.tick()
        x -= 1

# Utilities

# Given a list of objects, returns a list of their names.
def names(objectlist):
    namelist = [x.name for x in objectlist]
    return namelist

# Given a name and a list of objects, returns the object with that name.
def objectfind(objectname, objectlist):
    for each in objectlist:
        if each.name == objectname:
            return each
    return None
    
def find_all(location, type):
    all = filter(lambda x: isinstance(x, type), location.things)
    return all

# Given a list of exits, find one in the desired direction.
# TODO Add better handling for returning more than one exit here. Consider changing exits to be named by destination rather than direction??
def find_exit(exitlist, dir):
    if len(exitlist) > 0:
        exit = filter(lambda each: each.direction == dir, exitlist)
        if len(exit) == 1:
            return exit[0]
        elif len(exit) == 0:
            print "No exits found in that direction."
        else:
            print "Exits in that direction lead to: "
            for each in exit:
                print each.destination.name
            print "Please enter the index of the exit you want to use."
            index = input()
            return exit[index]
    else:
        print "No exit."

def random_exit(place):
    return random.choice(place.exits)

# TODO consider adding remove_duplicates here?
