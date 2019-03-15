# objects.py
# Christalee Bieber, 2016
# cbieber@alum.mit.edu
#
# This file defines a clock and a screen that act as the game world, plus classes for game objects.

# * TODO
# * scan & transcribe/OCR printout
# * Resolve all TODO / comments
# * write a test suite
# write methods to list player commands, inventory
# * add type signatures to everything
# * add extension code from printout
# * add text parser??
# TODO get clear on return / print / say/emit/tell values
# TODO Currently everything is printed to global output; eventually it should be restricted to a single location (look for calls to screen and/or 'TELL-ROOM)
# add code to ensure that there's only one World at a time? only one Clock? Avatar? Or at least World / Clock / Avatar go together?
# remove unneeded isinstance checks
# replace Callback with actual callbacks?
# replace for each with better loop variable names
# TODO should Named_Object and/or Container be abstract base classes?
# should Container just be... a list?
# Do I need these install() methods? Should delete() actually del(object)?

# * DONE decide how I want to interact with the game during dev & prod
# * DONE migrate to python 3.6 at least
# * DONE pick a docstring convention and stick with it

# TODO skipping network-mode, whatever that is

import random
from typing import Dict, List, Optional, TypeVar, Union

from utilities import *


class Callback:
    """A Callback stores a target object, method, and arguments. When activated, it executes the method on the target object. It can be thought of as a button that executes an action at every tick of the clock."""

    def __init__(self, name: str, obj: 'Named_Object', msg: str):
        self.name = "Callback " + name
        self.object = obj
        self.message = msg
        self.isInstalled: bool = False

    def __repr__(self):
        return self.name

    def install(self):
        self.isInstalled = True
        print(self.name + " installed!")

    def activate(self):
        getattr(self.object, self.message)()


class Clock:
    """A Clock is an object with a notion of time, which it imparts to all objects that have asked for it. It does this by invoking a list of Callbacks whenever the tick() method is invoked."""

    def __init__(self):
        self.name: str = "the clock"
        self.time: int = 0
        self.callbacks: List[Callback] = []
        self.removed_callbacks: List[Callback] = []

    def __repr__(self):
        return self.name

    def install(self):
        self.add_callback(Callback("tick-printer", self, "print_tick"))

    def reset(self):
        self.time = 0
        self.callbacks = []

    def tick(self):
        for each in reversed(self.callbacks):
            if each not in self.removed_callbacks:
                each.activate()
        self.removed_callbacks = []  # TODO does this do things correctly??
        self.time += 1

    def print_tick(self):
        print("---" + self.name + " Tick " + str(self.time) + "---")

    def add_callback(self, cb: Callback):
        if cb in self.callbacks:
            print(cb.name + "already exists")
        else:
            self.callbacks.append(cb)
            print(cb.name + " added")

    def remove_callback(self, obj: 'Named_Object', cb_name: str):
        def rcb(x: Callback):
            if x.name == cb_name and x.object == obj:
                self.removed_callbacks.append(x)
                return False
            else:
                return True
        self.callbacks = list(filter(rcb, self.callbacks))
        print(cb_name + " removed")


class Named_Object:
    """Named_Objects are the basic underlying object type in our system. For example, Persons, Places, and Things will all be kinds of (inherit from) Named_Objects.

    Behavior (methods) supported by all Named_Objects:
    - Has a name that it can return
    - Handles an install message
    - Handles a delete message"""

    def __init__(self, name):
        self.name: str = name
        self.isInstalled: bool = False

    def __repr__(self):
        return self.name

    def install(self):
        self.isInstalled = True
        print(self.name + " installed!")

    def delete(self):
        # TODO should this actually delete the object?
        self.isInstalled = False
        print(self.name + " deleted!")


class Container:
    """A Container holds Things.

    This class is not meant for "stand-alone" objects; rather, it is expected that other classes will inherit from the Container class in order to be able to contain Things."""

    # TODO is there any point in having this instead of just using a list?
    def __init__(self):
        self.things: List['Thing'] = []

    def have_thing(self, x: 'Thing'):
        if x in self.things:
            return True
        else:
            return False

    def add_thing(self, x: 'Thing'):
        # TODO should these also world.tell_world()?
        if not self.have_thing(x):
            self.things.append(x)

    def delete_thing(self, x: 'Thing'):
        # TODO should these also world.tell_world()?
        if self.have_thing(x):
            self.things.remove(x)


class Thing(Named_Object):
    """A Thing is a Named_Object that has a Place."""

    def __init__(self, name: str, location: 'Place'):
        self.location = location
        super(Thing, self).__init__(name)

    def install(self):
        super(Thing, self).install()
        self.location.add_thing(self)

    def delete(self):
        self.location.delete_thing(self)
        super(Thing, self).delete()

    def emit(self, text: str):
        # TODO should this be renamed say, in parallel to Person.say()?
        # TODO tell_room()
        print(self.location, "At " + self.location.name + " " + text)


class Mobile_Thing(Thing):
    # TODO figure out how to handle locations of Mobile_Things
    # Mobile_Place = TypeVar('Mobile_Place', Place, Person)
    """A Mobile_Thing is a Thing that has a location that can change."""

    def __init__(self, name: str, location: 'Place'):
        self.creation_site = location
        super(Mobile_Thing, self).__init__(name, location)
        # self.location: Union[Person, Place]

    def change_location(self, new_location: Union['Person', 'Place']):
        self.location.delete_thing(self)
        new_location.add_thing(self)
        self.location = new_location

    def enter_room(self):
        # TODO are these methods necessary? cf. Person.enter_room()
        return True

    def leave_room(self):
        # TODO are these methods necessary? cf. Person.leave_room()
        return True


class Place(Container, Named_Object):
    """A Place is a Container (so Things may be in the Place).

    A Place has Exits, which are passages from one place to another. One can retrieve all of the Exits of a Place, or an Exit in a given direction from Place."""

    def __init__(self, name: str):
        self.exits: List[Exit] = []
        Named_Object.__init__(self, name)
        super(Place, self).__init__()

    def exit_towards(self, direction: str):
        return find_exit(self.exits, direction)

    def add_exit(self, exit: 'Exit'):
        if exit not in self.exits:
            self.exits.append(exit)
            print(exit.name + " added at " + self.name)
        else:
            print(self.name + " already has exit to " + exit.name)


class Exit(Named_Object):
    """An Exit leads from one Place to another Place in some direction."""

    def __init__(self, origin: Place, direction: str, destination: Place):
        self.origin = origin
        self.direction = direction
        self.destination = destination
        super(Exit, self).__init__(direction)

    def install(self):
        if hasattr(self, "origin"):
            if self.origin.add_exit(self):
                super(Exit, self).install()

    def use(self, who: 'Person'):
        # TODO Check that the Place stops having the Person when they use the Exit
        who.leave_room()
        # TODO tell_room()
        print(who.location, who.name + " moves from " + who.location.name + " to " + self.destination.name)
        who.change_location(self.destination)
        who.enter_room()


# There are several kinds of Person:
# There are Autonomous_Persons, including Vampires, and there is the Avatar of the user. The foundation is here.


class Person(Container, Mobile_Thing):
    """A Person can move around (is a Mobile_Thing), and can hold Things (is a Container). A Person has a plethora of methods."""

    def __init__(self, name: str, birthplace: Place):
        self.health: int = 3
        self.strength: int = 1
        Mobile_Thing.__init__(self, name, birthplace)
        super(Person, self).__init__()
        # self.things: List[Mobile_Thing]

    def say(self, text: str):
        # TODO tell_room()
        print(self.location, "At " + self.location.name + " " + self.name + " says: " + text)

    def have_fit(self):
        self.say("Yaaaah! I am upset!")
        self.say("I feel better now.")

    def people_around(self):
        people: List[Person] = []
        for each in self.location.things:
            if each != self and isinstance(each, Person):
                people.append(each)
        return people

    def things_around(self):
        things: List[Thing] = []
        for each in self.location.things:
            if not isinstance(each, Person):
                things.append(each)
        return things

    def peek_around(self):
        all_items: List[List[str]] = []
        for each in self.people_around():
            itemlist: List[str] = names(each.things)
            if len(itemlist) > 0:
                self.say(each.name + " has " + ", ".join(itemlist))
            all_items.append(itemlist)
        # TODO tell_room()
        return all_items

    def take(self, itemname: str):
        item = thingfind(itemname, self.location.things)
        if not item:
            self.say("Sorry, that item isn't here.")
            return False
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
            return True

    def lose(self, item: Mobile_Thing, destination):
        self.say("I lose " + item.name)
        self.have_fit()
        item.change_location(destination)

    def drop(self, itemname: str):
        # TODO clarify that self.things only ever contains Mobile_Things
        item = thingfind(itemname, self.things)
        if not item:
            self.say("I don't have that item!")
            return False
        else:
            self.say("I drop " + item.name + " at " + self.location.name)
            item.change_location(self.location)
            return True

    def go_exit(self, exit: Exit):
        exit.use(self)

    def go(self, direction: str):
        exit = self.location.exit_towards(direction)
        if isinstance(exit, Exit):
            self.go_exit(exit)
            return True
        else:
            # TODO tell_room()
            print(self.location, "No exit in " + direction + " direction")
            return False

    def suffer(self, hits: int, perp):
        self.say("Ouch! " + str(hits) + " hits is more than I want!")
        self.health -= hits
        if self.health <= 0:
            self.die(perp)
        print('Health: ' + str(self.health))

    def die(self, perp):
        for each in self.things:
            self.lose(each, self.location)
        print("An earth-shattering, soul-piercing scream is heard...")
        self.create_body(perp)
        self.delete()

    def create_body(self, perp):
        # TODO combine die() with create_body()?
        Body(self.name, self.location, perp).install()

    def enter_room(self):
        # TODO write leave_room? get rid of enter_room? cf. Exit.use()
        others = self.people_around()
        if len(others) > 0:
            self.say("Hi " + ", ".join(names(others)))
        return True


class Autonomous_Person(Person):
    """A Person that can change Places and pick up Things.

    activity determines maximum movement
    miserly determines chance of picking stuff up"""

    def __init__(self, name: str, birthplace: Place, activity: int, miserly: int):
        self.activity = activity
        self.miserly = miserly
        super(Autonomous_Person, self).__init__(name, birthplace)

    def install(self):
        # global clock
        super(Autonomous_Person, self).install()
        clock.add_callback(Callback("move-and-take", self, "move_and_take"))

    def move_and_take(self):
        moves: int = random.randint(0, self.activity)
        while moves > 0:
            self.move()
            moves -= 1
        if random.randint(0, self.miserly) == 0:
            self.take()
        self.say(self.name + " done moving for this tick")

    def die(self, perp):
        # global clock
        clock.remove_callback(self, "move-and-take")
        self.say("SHREEEEK! I, uh, suddenly feel very faint...")
        super(Autonomous_Person, self).die(perp)

    def move(self):
        exit: Exit = random_exit(self.location)
        self.go_exit(exit)

    def take(self):
        items: List[Named_Object] = self.things_around() + self.peek_around()
        if len(items) > 0:
            super(Autonomous_Person, self).take(random.choice(items))
        return True


class Body(Thing):
    """A Thing which has the potential to rise as a Vampire"""

    def __init__(self, name: str, location: Place, perp):
        self.age: int = 0
        self.perp = perp
        super(Body, self).__init__(name, location)
        self.name = "body of " + name

    def install(self):
        # global clock
        super(Body, self).install()
        if isinstance(self.perp, Vampire):
            clock.add_callback(Callback(str(self.name), self, "wait"))

    def wait(self):
        self.age += 1
        if self.age > 3:
            self.delete()
            self.emit(self.name + " rises as a vampire!")
            Vampire(self.name, self.location, self.perp).install()

    def delete(self):
        # global clock
        clock.remove_callback(self, str(self.name))
        super(Body, self).delete()


class Vampire(Person):
    """An undead Person that randomly attacks people."""

    def __init__(self, name: str, birthplace: Place, sire: Optional['Vampire']):
        self.sire = sire
        if self.sire:
            self.power = 2
        else:
            self.power = 10
        super(Vampire, self).__init__(name, birthplace)

    def install(self):
        # global clock
        super(Vampire, self).install()
        if self.sire:
            self.sire.gain_power()
        clock.add_callback(Callback("rove-and-attack", self, "rove_and_attack"))

    def die(self, perp):
        # global clock
        clock.remove_callback(self, "rove-and-attack")
        super(Vampire, self).die(perp)

    def create_body(self, perp):
        self.emit(self.name + " turns to dust!")

    def gain_power(self):
        self.power += 1
        print(self.name + " gained power")

    def rove_and_attack(self):
        if random.randint(0, 2) == 0:
            self.move()
        if random.randint(0, 3) < 2:
            self.attack()

    def move(self):
        exit: Exit = random_exit(self.location)
        self.go_exit(exit)

    def attack(self):
        others = self.people_around()
        if len(others) > 0:
            victim = random.choice(others)
            self.emit(self.name + " bites " + victim.name + "!")
            victim.suffer(random.randint(0, self.power), self)
        print(self.name + " is tired")


class Avatar(Person):
    """The Avatar of the user is also a Person."""

    def __init__(self, name: str, birthplace: Place):
        super(Avatar, self).__init__(name, birthplace)

    def look(self):
        print("You are in " + self.location.name)
        if len(self.things) > 0:
            print("You are holding: " + ", ".join(names(self.things)))
        else:
            print("You are not holding anything.")
        if len(self.things_around()) > 0:
            print("You see stuff in the room: " + ", ".join(names(self.things_around())))
        else:
            print("There is no stuff in the room.")
        if len(self.people_around()) > 0:
            print("You see other people: " + ", ".join(names(self.people_around())))
        else:
            print("There are no other people around you.")
        if len(self.location.exits) > 0:
            print("The exits are in directions: " + ", ".join(names(self.location.exits)))
        else:
            print("There are no exits... you are dead and gone to heaven!")

    def go(self, direction: str):
        success: bool = super(Avatar, self).go(direction)
        if success:
            # global clock
            clock.tick()
        return success

    def die(self, perp):
        self.say("I am slain!")
        super(Avatar, self).die(perp)


clock = Clock()
