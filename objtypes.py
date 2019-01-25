from __future__ import print_function
from __future__ import absolute_import
# objtypes.py
# Christalee Bieber, 2016
# cbieber@alum.mit.edu
#
# A Python implementation of a vampire-themed text adventure game, originally written in Scheme. I extended this game for Project 4, the Object-Oriented Adventure Game, during the Spring 2004 term of 6.001, Structure & Interpretation of Computer Programs. The original assignment and project files can be found here: http://sicp.ai.mit.edu/Spring-2004/projects/index.html
#
# This file defines object classes and a few helper functions for the game world defined in setup.py

# * TODO
# * decide how I want to interact with the game during dev & prod
# * migrate to python 3.6 at least
# * pick a docstring convention and stick with it
# * scan & transcribe/OCR printout
# * Check all return values
# * Resolve all TODO / comments
# * write a test suite
# * add type signatures to everything
# * add extension code from printout
# * add text parser??

import random
from .objsys import *

# --------------------
# Named_Object
# 
# Named_Objects are the basic underlying object type in our system. For example, Persons, Places, and Things will all be kinds of (inherit from) Named_Objects.
# 
# Behavior (methods) supported by all Named_Objects:
# - Has a name that it can return
# - Handles an install message
# - Handles a delete message

class Named_Object(object):
    def __init__(self, name):
        self.name = name
        self.isInstalled = False
    
    def install(self):
        self.isInstalled = True
        print(self.name + " installed!")
    
    def delete(self):
        self.isInstalled = False
        print(self.name + " deleted!")

# --------------------
# Container
# 
# A Container holds Things.  
# 
# This class is not meant for "stand-alone" objects; rather, it is expected that other classes will inherit from the Container class in order to be able to contain Things.

class Container(object):
    def __init__(self):
        self.things = []

    def have_thing(self, x):
        if x in self.things:
            return True
        else:
            return False
    
    def add_thing(self, x):
        if not self.have_thing(x):
            self.things.append(x)
    
    def delete_thing(self, x):
        if self.have_thing(x):
            self.things.remove(x)

# --------------------
# Thing
# 
# A Thing is a Named_Object that has a Place.

class Thing(Named_Object):
    def __init__(self, name, location):
        self.location = location
        super(Thing, self).__init__(name)
    
    def install(self):
        super(Thing, self).install()
        self.location.add_thing(self)
    
    def delete(self):
        self.location.delete_thing(self)
        super(Thing, self).delete()
    
    def emit(self, text):
        screen.tell_room(self.location, "At " + self.location.name + " " + text)

# --------------------
# Mobile_Thing
# 
# A Mobile_Thing is a Thing that has a location that can change.

class Mobile_Thing(Thing):
    def __init__(self, name, location):
        self.creation_site = location
        super(Mobile_Thing, self).__init__(name, location)
        
    def change_location(self, new_location):
        self.location.delete_thing(self)
        new_location.add_thing(self)
        self.location = new_location
    
    def enter_room(self):
        return True
    
    def leave_room(self):
        return True

# --------------------
# Place
# 
# A Place is a Container (so Things may be in the Place).
# 
# A Place has Exits, which are passages from one place to another.  One can retrieve all of the Exits of a Place, or an Exit in a given direction from Place.

class Place(Container, Named_Object):
    def __init__(self, name):
        self.exits = []
        Named_Object.__init__(self, name)
        super(Place, self).__init__()
    
    def exit_towards(self, direction):
        return find_exit(self.exits, direction)
    
    def add_exit(self, exit):
        if not exit in self.exits:
            self.exits.append(exit)
            return "done"
        else:
            print(self.name + " already has exit to " + exit.name)

# ------------------------------------------------------------
# Exit
# 
# An Exit leads from one Place to another Place in some direction.

class Exit(Named_Object):
    def __init__(self, origin, direction, destination):
        self.origin = origin
        self.direction = direction
        self.destination = destination
        super(Exit, self).__init__(direction)
    
    def install(self):
        if hasattr(self, "origin"):
            if self.origin.add_exit(self):
                super(Exit, self).install()
    
    # TODO what does leave_room even do?? is it meant to be superseded in Person? 
    # TODO Check that the Place stops having the Person when they use the Exit??
    def use(self, whom): 
        whom.leave_room()
        screen.tell_room(whom.location, whom.name + " moves from " + whom.location.name + " to " + self.destination.name)
        whom.change_location(self.destination)
        whom.enter_room()

# --------------------
# Person
# 
# There are several kinds of Person:  
# There are Autonomous_Persons, including Vampires, and there is the Avatar of the user.  The foundation is here.
# 
# A Person can move around (is a Mobile_Thing), and can hold Things (is a Container). A Person has a plethora of methods.

# TODO Currently everything is printed to global output; eventually it should be restricted to a single location (look for calls to screen and/or 'TELL-ROOM)

class Person(Container, Mobile_Thing):
    def __init__(self, name, birthplace):
        self.health = 3
        self.strength = 1
        Mobile_Thing.__init__(self, name, birthplace)
        super(Person, self).__init__()
    
    def say(self, stuff):
        screen.tell_room(self.location, "At " + self.location.name + " " + self.name + " says: " + stuff)
    
    def have_fit(self):
        self.say("Yaaaah! I am upset!")
        return "I-feel-better-now"
    
    def people_around(self):
        people = []
        for each in self.location.things:
            if isinstance(each, Person) and each != self:
                people.append(each)
        return people
    
    def things_around(self): 
        things = []
        for each in self.location.things:
            if not isinstance(each, Person):
                things.append(each)
        return things

    def peek_around(self):
        all_items = []
        for each in self.people_around():
            itemlist = []
            for item in names(each.things):
                itemlist.append(item)
            all_items.append(itemlist)
            print(each.name + " has " + ", ".join(itemlist))
        return all_items
    
    def take(self, itemname):
        item = objectfind(itemname, self.location.things)
        if self.have_thing(item):
            self.say("I am already carrying " + item.name)
            return False
        if isinstance(item, Person) or not isinstance(item, Mobile_Thing):
            self.say("I try but cannot take " + item.name)
            return False
        else:
            owner = item.location
            self.say("I take " + item.name + " from " + owner.name)
            if isinstance(owner, Person):
                owner.lose(item, self)
            else:
                item.change_location(self)
            return item
    
    def lose(self, item, destination):
        self.say("I lose " + item.name)
        self.have_fit()
        item.change_location(destination)
    
    def drop(self, itemname):
        item = objectfind(itemname, self.location.things)
        self.say("I drop " + item.name + " at " + self.location.name)
        item.change_location(self.location)
    
    def go_exit(self, exit):
        exit.use(self)
    
    def go(self, direction):
        exit = self.location.exit_towards(direction)
        if isinstance(exit, Exit):
            self.go_exit(exit)
        else:
            screen.tell_room(self.location, "No exit in " + direction + " direction")
            return False
    
    def suffer(self, hits, perp):
        self.say("Ouch! " + str(hits) + " hits is more than I want!")
        self.health -= hits
        if self.health <= 0:
            self.die(perp)
        return self.health
    
    def die(self, perp):
        for each in self.things:
            self.lose(each, self.location)
        screen.tell_world("An earth-shattering, soul-piercing scream is heard...")
        self.create_body(perp)
        self.delete()
    # * Probably need to change this to create an instance of Body too
    def create_body(self, perp):
        Body(self.name, self.location, perp).install()
    
    def enter_room(self):
        others = self.people_around()
        if len(others) > 0:
            self.say("Hi " + ", ".join(names(others)))
        return True

# --------------------
# Autonomous_Person
# 
# activity determines maximum movement
# miserly determines chance of picking stuff up

# TODO At some point, check all return values in original and decide if they are meaningful

class Autonomous_Person(Person):
    def __init__(self, name, birthplace, activity, miserly):
        self.activity = activity
        self.miserly = miserly
        super(Autonomous_Person, self).__init__(name, birthplace)
    
    # TODO revisit this when clock is invented
    def install(self):
        super(Autonomous_Person, self).install()
        clock.add_callback(Clock_CB("move-and-take", self, "move_and_take")) 
    
    def move_and_take(self):
        moves = random.randint(0, self.activity)
        while moves > 0:
            self.move()
            moves -= 1
        if random.randint(0, self.miserly) == 0:
            self.take()
        return "done-for-this-tick"
    
    def die(self, perp):
        clock.remove_callback(self, "move-and-take")
        self.say("SHREEEEK! I, uh, suddenly feel very faint...")
        super(Autonomous_Person, self).die(perp)
    
    def move(self):
        exit = random_exit(self.location)
        if isinstance(exit, Exit):
            self.go_exit(exit)
    
    def take(self):
        items = self.things_around() + self.peek_around()
        if len(items) > 0:
            super(Autonomous_Person, self).take(random.choice(items))
        return False

# --------------------
# Body
# 
# A Thing which has the potential to rise as a vampire

class Body(Thing):
    def __init__(self, name, location, perp):
        self.age = 0
        self.perp = perp
        super(Body, self).__init__(name, location)
        self.name = "body-of-" + super(Body, self).name
    
    def install(self):
        super(Body, self).install()
        if isinstance(self.perp, Vampire):
            clock.add_callback(Clock_CB(str(self.age), self, "wait"))
    
    def wait(self):
        self.age += 1
        if self.age > 3:
            self.delete()
            self.emit(self.name + " rises as a vampire!")
            Vampire(self.name, self.location, self.perp).install()
    
    def delete(self):
        clock.remove_callback(self, str(self.age))
        super(Body, self).delete()

# --------------------
# Vampire
# 
# An undead Person that randomly attacks people.

class Vampire(Person):
    def __init__(self, name, birthplace, sire):
        self.sire = sire
        if self.sire:
            self.power = 2
        else:
            self.power = 10
        super(Vampire, self).__init__(name, birthplace)
    
    def install(self):
        super(Vampire, self).install()
        if self.sire:
            sire.gain_power()
        clock.add_callback(Clock_CB("rove-and-attack", self, "rove_and_attack"))
    
    def die(self, perp):
        clock.remove_callback(self, "rove-and-attack")
        super(Vampire, self).die(perp)
    
    def create_body(self, perp):
        self.emit(self.name + " turns to dust!")
        return "no-body-necessary"
    
    def gain_power(self):
        self.power += 1
        return "gained-power"
    
    def rove_and_attack(self):
        if random.randint(0, 2) == 0:
            self.move()
        if random.randint(0, 3) < 2:
            self.attack()
    
    def move(self):
        exit = random_exit(self.location)
        if isinstance(exit, Exit):
            self.go_exit(exit)
        
    def attack(self):
        if len(others) > 0:
            victim = random.choice(self.people_around())
            self.emit(self.name + " bites " + victim.name + "!")
            victim.suffer(random.randint(0, self.power), self)
        return "vampire-is-tired"

# --------------------
# Avatar
# 
# The Avatar of the user is also a Person.

class Avatar(Person):
    def __init__(self, name, birthplace):
        super(Avatar, self).__init__(name, birthplace)
    
    def look(self):
        screen.tell_world("You are in " + self.location.name)
        if len(self.things) > 0:
            screen.tell_world("You are holding: " + ", ".join(names(self.things)))
        else:
            screen.tell_world("You are not holding anything.")
        if len(self.things_around()) > 0:
            screen.tell_world("You see stuff in the room: " + ", ".join(names(self.things_around())))
        else:
            screen.tell_world("There is no stuff in the room.")
        if len(self.people_around()) > 0:
            screen.tell_world("You see other people: " + ", ".join(names(self.people_around())))
        else:
            screen.tell_world("There are no other people around you.")
        if len(self.location.exits) > 0:
            screen.tell_world("The exits are in directions: " + ", ".join(names(self.location.exits)))
        else:
            screen.tell_world("There are no exits... you are dead and gone to heaven!")
        return "ok"
    
    def go(self, direction):
        success = super(Avatar, self).go(direction)
        if success:
            clock.tick()
        return success
    
    def die(self, perp):
        self.say("I am slain!")
        super(Avatar, self).die(perp)