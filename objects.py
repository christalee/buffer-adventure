# objects.py
# Christalee Bieber, 2016
# cbieber@alum.mit.edu
#
# This file defines a clock and a screen that act as the game world, plus classes for game objects.

# TODO skipping network-mode, whatever that is

import random
from typing import Callable, Dict, List, Optional, Union

from utilities import *

DEBUG: bool = True


class Named_Object:
    """Named_Objects are the basic underlying object type in our system. For example, Persons, Places, and Things will all be kinds of (inherit from) Named_Objects.

    Behavior (methods) supported by all Named_Objects:
    - Has a name that it can return
    - Handles an install message
    - Handles a delete message"""

    def __init__(self, name) -> None:
        self.name: str = name
        self.isInstalled: bool = False

    def __repr__(self):
        return self.name

    def install(self) -> None:
        self.isInstalled = True
        if DEBUG:
            print(self.name + " installed!")

    def delete(self) -> None:
        # TODO should this actually delete the object?
        self.isInstalled = False
        if DEBUG:
            print(self.name + " deleted!")


class Container:
    """A Container holds Things.

    This class is not meant for "stand-alone" objects; rather, it is expected that other classes will inherit from the Container class in order to be able to contain Things."""

    # TODO is there any point in having this instead of just using a list?
    def __init__(self) -> None:
        self.things: List['Thing'] = []

    def have_thing(self, x: 'Thing') -> bool:
        if x in self.things:
            return True
        else:
            return False

    def add_thing(self, x: 'Thing') -> None:
        # TODO should these also world.tell_world()?
        if not self.have_thing(x):
            self.things.append(x)

    def remove_thing(self, x: 'Thing') -> None:
        # TODO should these also world.tell_world()?
        if self.have_thing(x):
            self.things.remove(x)


class Clock(Named_Object):
    """A Clock is an object with a notion of time, which it imparts to all objects that have asked for it. It does this by invoking a list of callbacks whenever the tick() method is invoked."""

    def __init__(self) -> None:
        self.time: int = 0
        self.callbacks: List[Callable] = []
        self.removed_callbacks: List[Callable] = []
        super(Clock, self).__init__('Clock')

    def __repr__(self):
        return self.name

    def install(self) -> None:
        self.add_callback(self.print_tick)

    def reset(self) -> None:
        self.time = 0
        self.callbacks = []

    def tick(self) -> None:
        for cb in reversed(self.callbacks):
            if cb not in self.removed_callbacks:
                cb()
        self.removed_callbacks = []  # TODO does this do things correctly??
        self.time += 1

    def print_tick(self) -> None:
        print("---" + self.name + " Tick " + str(self.time) + "---")

    def add_callback(self, cb: Callable):
        if cb in self.callbacks:
            print(str(cb.__func__) + " already exists")
        else:
            self.callbacks.append(cb)
            if DEBUG:
                x = str(cb).split()
                print(x[-1].replace('>', '.') + x[2] + " added")

    def remove_callback(self, cb: Callable):
        if cb in self.callbacks:
            self.removed_callbacks.append(cb)
            self.callbacks.remove(cb)
            if DEBUG:
                print(str(cb.__func__) + " removed")


class Thing(Named_Object):
    """A Thing is a Named_Object that has a Place."""

    def __init__(self, name: str, location: 'Place'):
        self.location = location
        super(Thing, self).__init__(name)

    def install(self) -> None:
        super(Thing, self).install()
        self.location.add_thing(self)

    def delete(self) -> None:
        self.location.remove_thing(self)
        super(Thing, self).delete()

    def say(self, text: str):
        # TODO tell_room()
        if DEBUG:
            print("At " + self.location.name + " " + text)


class Mobile_Thing(Thing):
    # TODO figure out how to handle locations of Mobile_Things
    # Mobile_Place = TypeVar('Mobile_Place', Place, Person)
    """A Mobile_Thing is a Thing that has a location that can change."""

    def __init__(self, name: str, location: 'Place'):
        self.creation_site = location
        super(Mobile_Thing, self).__init__(name, location)
        self.location: Union['Person', 'Place']

    def change_location(self, new_location: Union['Person', 'Place']):
        owner = self.location
        owner.remove_thing(self)
        if isinstance(owner, Person):
            owner.say("I lose " + self.name)
            owner.have_fit()
        new_location.add_thing(self)
        self.location = new_location


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
            if DEBUG:
                print(exit.name + " added at " + self.name)
            return True
        else:
            if DEBUG:
                print(self.name + " already has an exit to " + exit.name)
            return False


class Exit(Named_Object):
    """An Exit leads from one Place to another Place in some direction."""

    def __init__(self, origin: Place, direction: str, destination: Place):
        self.origin = origin
        self.direction = direction
        self.destination = destination
        super(Exit, self).__init__(direction)

    # TODO is this hasattr really necessary
    def install(self):
        if hasattr(self, "origin"):
            if self.origin.add_exit(self):
                super(Exit, self).install()

    def use(self, who: 'Person'):
        # TODO Check that the Place stops having the Person when they use the Exit
        # TODO tell_room()
        if DEBUG:
            print(who.name + " moves from " + who.location.name + " to " + self.destination.name)
        who.change_location(self.destination)


# There are several kinds of Person:
# There are Autonomous_Persons, including Vampires, and there is the Avatar of the user. The foundation is here.


class Person(Container, Mobile_Thing):
    """A Person can move around (is a Mobile_Thing), and can hold Things (is a Container). A Person has a plethora of methods."""

    def __init__(self, name: str, birthplace: Place):
        self.health: int = 3
        self.strength: int = 1
        Mobile_Thing.__init__(self, name, birthplace)
        self.things: List[Mobile_Thing]
        super(Person, self).__init__()

    def say(self, text: str):
        # TODO tell_room()
        if DEBUG:
            print("At " + self.location.name + " " + self.name + " says: " + text)

    def have_fit(self) -> None:
        self.say("Yaaaah! I am upset!")
        self.say("I feel better now.")

    # TODO combine _around methods?
    def people_around(self) -> List['Person']:
        people: List[Person] = []
        for t in self.location.things:
            if t != self and isinstance(t, Person):
                people.append(t)
        return people

    def room_things(self) -> List[Thing]:
        things: List[Thing] = []
        for t in self.location.things:
            if not isinstance(t, Person):
                things.append(t)
        return things

    def people_things(self) -> List[List[Thing]]:
        all_items: List[List[Thing]] = []
        for p in self.people_around():
            itemlist: List[str] = p.things
            if len(itemlist) > 0:
                self.say(p.name + " has " + ", ".join(names(itemlist)))
            all_items.append(itemlist)
        # TODO tell_room()
        return all_items

    def take(self, itemname: str) -> bool:
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
            item.change_location(self)
            return True

    def drop(self, itemname: str) -> bool:
        item: Optional[Mobile_Thing] = thingfind(itemname, self.things)
        if item:
            self.say("I drop " + item.name + " at " + self.location.name)
            item.change_location(self.location)
            return True

        else:
            self.say("I don't have that item!")
            return False

    def go(self, direction: str) -> bool:
        exit = self.location.exit_towards(direction)
        if exit:
            exit.use(self)
            return True
        else:
            # TODO tell_room()
            print(self.location, "No exit in " + direction + " direction")
            return False

    def wander(self) -> None:
        exit: Exit = random_exit(self.location)
        exit.use(self)

    def suffer(self, hits: int, perp: 'Person'):
        self.say("Ouch! " + str(hits) + " damage is more than I want!")
        self.health -= hits
        if self.health <= 0:
            self.die(perp)
        print('Health: ' + str(self.health))

    def die(self, perp: 'Person'):
        for n in names(self.things):
            self.drop(n)
        print("An earth-shattering, soul-piercing scream is heard...")
        Body(self.name, self.location, perp).install()
        self.delete()

    def change_location(self, new_location: Union['Person', 'Place']):
        super(Person, self).change_location(new_location)
        others = self.people_around()
        if len(others) > 0:
            self.say("Hi " + ", ".join(names(others)))


class Autonomous_Person(Person):
    """A Person that can change Places and pick up Things.

    activity determines maximum movement
    miserly determines chance of picking stuff up"""

    def __init__(self, name: str, birthplace: Place, activity: int, miserly: int):
        self.activity = activity
        self.miserly = miserly
        super(Autonomous_Person, self).__init__(name, birthplace)

    def install(self) -> None:
        super(Autonomous_Person, self).install()
        clock.add_callback(self.move_and_take)

    def move_and_take(self) -> None:
        moves: int = random.randint(0, self.activity)
        while moves > 0:
            self.wander()
            moves -= 1
        if random.randint(0, self.miserly) == 0:
            self.take()
        if DEBUG:
            self.say("I'm done moving for now.")

    def die(self, perp: Person) -> None:
        clock.remove_callback(self.move_and_take)
        if DEBUG:
            self.say("Aaaaahhhh! I suddenly feel very faint...")
        super(Autonomous_Person, self).die(perp)

    def take(self) -> bool:
        items: List[Named_Object] = self.room_things() + self.people_things()
        if len(items) > 0:
            super(Autonomous_Person, self).take(random.choice(items))
            return True
        else:
            if DEBUG:
                self.say("Whoops, there's nothing here to take.")
            return False


class Body(Thing):
    """A Thing which has the potential to rise as a Vampire"""

    def __init__(self, name: str, location: Place, perp: Person):
        self.age: int = 0
        self.perp = perp
        super(Body, self).__init__(name, location)
        self.name = "body of " + name

    def install(self) -> None:
        super(Body, self).install()
        if isinstance(self.perp, Vampire):
            clock.add_callback(self.wait)

    def wait(self) -> None:
        self.age += 1
        if self.age > 3:
            self.delete()
            if DEBUG:
                self.say(self.name + " rises as a vampire!")
            Vampire(self.name, self.location, self.perp).install()

    def delete(self) -> None:
        clock.remove_callback(self.wait)
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

    def install(self) -> None:
        super(Vampire, self).install()
        if self.sire:
            self.sire.gain_power()
        clock.add_callback(self.rove_and_attack)

    def die(self, perp: Person):
        clock.remove_callback(self.rove_and_attack)
        super(Vampire, self).die(perp)

    def create_body(self, perp: Person):
        if DEBUG:
            self.say(self.name + " turns to dust!")

    def gain_power(self) -> None:
        self.power += 1
        if DEBUG:
            self.say(self.name + " gained power")

    def rove_and_attack(self) -> None:
        if random.randint(0, 2) == 0:
            self.wander()
        if random.randint(0, 3) < 2:
            self.attack()

    def attack(self) -> None:
        others = self.people_around()
        if len(others) > 0:
            victim = random.choice(others)
            victim.suffer(random.randint(0, self.power), self)
            if DEBUG:
                self.say(self.name + " bites " + victim.name + "!")
                print(self.name + " is tired")


class Avatar(Person):
    """The Avatar of the user is also a Person."""

    def __init__(self, name: str, birthplace: Place):
        super(Avatar, self).__init__(name, birthplace)

    def look(self) -> None:
        print("You are in " + self.location.name)
        if len(self.things) > 0:
            print("You are holding: " + ", ".join(names(self.things)))
        else:
            print("You are not holding anything.")
        if len(self.room_things()) > 0:
            print("You see things in the room: " + ", ".join(names(self.room_things())))
        else:
            print("There is nothing in the room.")
        if len(self.people_around()) > 0:
            print("You see other people: " + ", ".join(names(self.people_around())))
        else:
            print("There are no other people around you.")
        if len(self.location.exits) > 0:
            print("The exits are in directions: " + ", ".join(names(self.location.exits)))
        else:
            print("There are no exits... you are dead and gone to heaven!")

    def go(self, direction: str) -> bool:
        success: bool = super(Avatar, self).go(direction)
        if success:
            clock.tick()
            self.look()
        return success

    def die(self, perp: Person):
        self.say("I am slain!")
        super(Avatar, self).die(perp)


clock: Clock = Clock()
