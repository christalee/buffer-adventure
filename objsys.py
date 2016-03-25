# objsys.py
# Christalee Bieber, 2016
# cbieber@alum.mit.edu
#
# A Python implementation of a vampire-themed text adventure game, originally written in Scheme. I extended this game for Project 4, The Object-Oriented Adventure game, during the Spring 2004 term of 6.001, Structure & Interpretation of Computer Programs. The original assignment and project files can be found here: http://sicp.ai.mit.edu/Spring-2004/projects/index.html
#
# This file provides a clock and a screen for objects in a simulation world.  Additional utility procedures are also provided.

# * skipping network-mode, whatever that is

class Screen(object):
    def __init__(self):
        self.deity_mode = True
        self.me = False
        self.name = "the-screen"
    
    def set_me(self, new_me):
        self.me = new_me
    
    def tell_world(self, text):
        print text
    # * right now just print everything.
    def tell_room(self, location, text):
        print location
        print text

screen = Screen()
# --------------------
# Clock
# 
# A Clock is an object with a notion of time, which it imparts to all objects that have asked for it.  It does this by invoking a list of CALLBACKs whenever the TICK method is invoked on the clock.  A CALLBACK is an action to invoke on each tick of the clock, by calling a method on an object
        
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
        self.removed_callbacks = []
        for each in self.callbacks.reverse():
            if each not in self.removed_callbacks:
                each.activate()
        self.time += 1
    
    def print_tick(self):
        screen.tell_world("---" + self.name + " Tick " + self.time + "---")
    
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
        self.installed = False
    
    def install(self):
        self.installed = True
        print self.name + " installed!"
    
    def activate(self):
        self.object.__dict__[self.message]

clock = Clock()

def current_time():
    return clock.time

def run_clock(x):
    while x > 0:
        clock.tick()
        x -= 1

# Utility procedures
def find_all(location, type):
    all = filter(lambda x: isinstance(x, type), location.things)
    return all

# * consider adding remove_duplicates here?
