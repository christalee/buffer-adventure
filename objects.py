# objects.py
# Christalee Bieber, 2016
# cbieber@alum.mit.edu
#
# This file defines a clock and a screen that act as the game world, plus classes for game objects.

# TODO skipping network-mode, whatever that is

import random
from typing import Callable, Dict, List, Optional, Union

import utilities as u

DEBUG: bool = True


class Named_Object:
    """Named_Objects are the basic underlying object type in our system. For example, Persons, Places, and Things will all be kinds of (inherit from) Named_Objects.

    Behavior (methods) supported by all Named_Objects:
    - Has a name that it can return
    - Handles an install message
    - Handles a delete message"""

    def __init__(self, name) -> None:
        self.name: str = name
        self.installed: bool = True
        if DEBUG:
            print(self.name + " installed!")

    def __repr__(self):
        return self.name

    def delete(self) -> None:
        # TODO should this actually delete the object?
        self.installed = False
        if DEBUG:
            print(self.name + " deleted!")


class Container:
    """A Container holds Things.

    This class is not meant for "stand-alone" objects; rather, it is expected that other classes will inherit from the Container class in order to be able to contain Things."""

    def __init__(self) -> None:
        self.things: List['Thing'] = []

    def have_thing(self, x: 'Thing') -> bool:
        return x in self.things

    # TODO consider raising exceptions here?
    def add_thing(self, x: 'Thing') -> None:
        # TODO should these also world.tell_world()?
        if not self.have_thing(x):
            self.things.append(x)

    # TODO consider raising exceptions here?
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
        self.add_callback(self.print_tick)

    def __repr__(self):
        return self.name

    def reset(self) -> None:
        self.time = 0
        self.callbacks = []
        self.add_callback(self.print_tick)

    def tick(self) -> None:
        for cb in reversed(self.callbacks):
            if cb not in self.removed_callbacks:
                cb()
        self.removed_callbacks = []  # TODO does this do things correctly??
        self.time += 1

    def print_tick(self) -> None:
        print("---" + self.name + " Tick " + str(self.time) + "---")

    def add_callback(self, cb: Callable):
        x = str(cb).split()
        if cb in self.callbacks:
            print(x[-1].replace('>', '.') + x[2] + " already exists")
        else:
            self.callbacks.append(cb)
            if DEBUG:
                print(x[-1].replace('>', '.') + x[2] + " added")

    def remove_callback(self, cb: Callable):
        if cb in self.callbacks:
            self.removed_callbacks.append(cb)
            self.callbacks.remove(cb)
            if DEBUG:
                x = str(cb).split()
                print(x[-1].replace('>', '.') + x[2] + " removed")


class Thing(Named_Object):
    """A Thing is a Named_Object that has a Place."""

    def __init__(self, name: str, location: 'Place'):
        self.location = location
        self.owner: Optional['Person'] = None

        super(Thing, self).__init__(name)
        self.location.add_thing(self)

    def delete(self) -> None:
        self.location.remove_thing(self)
        super(Thing, self).delete()

    def say(self, text: str):
        # TODO tell_room()
        if DEBUG:
            print("At " + self.location.name + ", " + text)


class Mobile_Thing(Thing):
    """A Mobile_Thing is a Thing that has a location that can change."""

    def __init__(self, name: str, location: 'Place'):
        self.creation_site = location

        super(Mobile_Thing, self).__init__(name, location)

    def change_location(self, new_location: 'Place'):
        self.location.remove_thing(self)
        new_location.add_thing(self)
        self.location = new_location

    def change_owner(self, new_owner: Optional['Person']):
        if self.owner:
            self.owner.remove_thing(self)
            self.owner.say("I lose " + self.name)
            self.owner.have_fit()
        if new_owner:
            new_owner.add_thing(self)
        self.owner = new_owner


class Holy_Object(Mobile_Thing):
    """A Holy_Object is a Mobile_Thing that repels Vampire attacks on the Person holding it."""

    def __init__(self, name: str, location: 'Place'):
        super(Holy_Object, self).__init__(name, location)


class Weapon(Mobile_Thing):
    """A Weapon is a Mobile_Thing that can be used to attack Vampires (and other Persons). Usually it deals a random amount of damage (up to its damage value) but 10% of the time it inflicts 10x normal."""

    def __init__(self, name: str, location: 'Place', damage: int):
        self.damage = damage

        super(Weapon, self).__init__(name, location)

    def hit(self, perp: 'Person', target: 'Person'):
        self.say(perp.name + " lays the smackdown on " + target.name + '!')
        normal = random.randint(1, self.damage)
        chance = random.randint(1, 10)

        if chance == 1:
            target.suffer(10 * normal, perp)
        else:
            target.suffer(normal, perp)


class Place(Container, Named_Object):
    """A Place is a Container (so Things may be in the Place).

    A Place has Exits, which are passages from one place to another. One can retrieve all of the Exits of a Place, or an Exit in a given direction from Place."""

    def __init__(self, name: str):
        self.exits: List[Exit] = []

        Named_Object.__init__(self, name)
        super(Place, self).__init__()

    def exit_towards(self, direction: str):
        return u.find_exit(self.exits, direction)

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

        super(Exit, self).__init__(direction + " - " + destination.name)
        self.origin.add_exit(self)

    def use(self, who: 'Person'):
        # TODO Check that the Place stops having the Person when they use the Exit
        # TODO tell_room()
        if DEBUG:
            print(who.name + " moves from " + who.location.name + " to " + self.destination.name)
        who.change_location(self.destination)
        for t in who.things:
            t.change_location(self.destination)


# There are several kinds of Person:
# There are Autonomous_Persons, including Vampires, and there is the Avatar of the user. The foundation is here.


class Person(Container, Mobile_Thing):
    """A Person can move around (is a Mobile_Thing), and can hold Things (is a Container). A Person has a plethora of methods."""

    def __init__(self, name: str, birthplace: Place):
        self.health: int = 3
        self.strength: int = 1
        self.things: List[Mobile_Thing]

        Mobile_Thing.__init__(self, name, birthplace)
        super(Person, self).__init__()

    def say(self, text: str):
        # TODO tell_room()
        print("At " + self.location.name + " " + self.name + " says: " + text)

    def have_fit(self) -> None:
        self.say("Yaaaah! I am upset!")
        self.say("I feel better now.")

    # TODO combine _around methods?
    def people_around(self) -> List['Person']:
        people: List[Person] = [p for p in self.location.things if p != self and isinstance(p, Person)]
        return people

    def room_things(self) -> List[Thing]:
        things: List[Thing] = [t for t in self.location.things if not t.owner and not isinstance(t, Person)]
        return things

    def people_things(self) -> List[Mobile_Thing]:
        all_items: List[Mobile_Thing] = []
        for p in self.people_around():
            itemlist: List[Mobile_Thing] = p.things
            if len(itemlist) > 0:
                self.say(p.name + " has " + ", ".join(u.names(itemlist)))
            all_items.extend(itemlist)
        # TODO tell_room()
        return all_items

    def take(self, itemname: str) -> bool:
        item: Optional[Mobile_Thing] = u.thingfind(itemname, self.location.things)
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
            if item.owner:
                n = item.owner.name
            else:
                n = item.location.name
            self.say("I take " + item.name + " from " + n)
            item.change_owner(self)
            return True

    def drop(self, itemname: str) -> bool:
        item: Optional[Mobile_Thing] = u.thingfind(itemname, self.things)
        if item:
            self.say("I drop " + item.name + " at " + self.location.name)
            item.change_location(self.location)
            item.change_owner(None)
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
        exit: Exit = u.random_exit(self.location)
        exit.use(self)

    def suffer(self, hits: int, perp: 'Person'):
        self.say("Ouch! " + str(hits) + " damage is more than I want!")
        self.health -= hits
        if self.health <= 0:
            self.die(perp)
        if DEBUG:
            print('Health: ' + str(self.health))

    def attack(self, target: str):
        victim: Optional[Person] = u.thingfind(target, self.people_around())
        if not victim:
            self.say("There's no one here to attack!")
            return False
        # pick a weapon: from player input, or the strongest item in inventory, or fists if you have no weapons
        weapons: List[Optional[Weapon]] = [x for x in self.things if isinstance(x, Weapon)]
        if weapons:
            if len(weapons) == 1:
                w = weapons[0]
            else:
                print("Choose your weapon: " + ', '.join(u.names(weapons)))
                w = u.thingfind(input(), weapons)
                if not w:
                    w = max(weapons, key=lambda x: x.damage)
            w.hit(self, victim)
        else:
            self.say(self.name + " punches " + target + "!")
            victim.suffer(3, self)

    def die(self, perp: 'Person'):
        for n in u.names(self.things):
            self.drop(n)
        print("An earth-shattering, soul-piercing scream is heard...")
        Body(self.name, self.location, perp)
        self.delete()

    def change_location(self, new_location: Place):
        super(Person, self).change_location(new_location)
        others = self.people_around()
        if len(others) > 0:
            self.say("Hi " + ", ".join(u.names(others)))


class Autonomous_Person(Person):
    """A Person that can change Places and pick up Things.

    activity determines maximum movement
    miserly determines chance of picking stuff up"""

    def __init__(self, name: str, birthplace: Place, activity: int, miserly: int):
        self.activity = activity
        self.miserly = miserly

        super(Autonomous_Person, self).__init__(name, birthplace)
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

    def take(self, itemname='') -> bool:
        items: List[Named_Object] = self.people_things() + self.room_things()
        if items:
            return super(Autonomous_Person, self).take(random.choice(items).name)
        else:
            if DEBUG:
                self.say("Whoops, there's nothing here to take.")
            return False


class Vampire(Person):
    """An undead Person that randomly attacks people."""

    def __init__(self, name: str, birthplace: Place, sire: Optional['Vampire']):
        self.sire = sire
        if self.sire:
            self.power = 2
            self.sire.gain_power()
        else:
            self.power = 10

        super(Vampire, self).__init__(name, birthplace)
        clock.add_callback(self.rove_and_attack)

    def die(self, perp: Person):
        if DEBUG:
            self.say(self.name + " turns to dust!")
        clock.remove_callback(self.rove_and_attack)
        super(Vampire, self).die(perp)

    def gain_power(self) -> None:
        self.power += 1
        if DEBUG:
            self.say(self.name + " gained power")

    def rove_and_attack(self) -> None:
        if random.randint(0, 2) == 0:
            self.wander()
        if random.randint(0, 3) < 2:
            self.attack()

    def attack(self, target='') -> None:
        others = [p for p in self.people_around() if not isinstance(p, Vampire)]
        if len(others) > 0:
            victim = random.choice(others)
            self.say(self.name + " bites " + victim.name + "!")
            for t in victim.things:
                if isinstance(t, Holy_Object):
                    if DEBUG:
                        self.say('Curses! Foiled again!')
                    break
            else:
                victim.suffer(random.randint(0, self.power), self)
                if DEBUG:
                    print(self.name + " is tired")


class Body(Thing):
    """A Thing which has the potential to rise as a Vampire"""

    def __init__(self, name: str, location: Place, perp: Optional[Union[Person, Vampire]]):
        self.age: int = 0
        self.perp = perp

        super(Body, self).__init__(name, location)
        self.name = "body of " + name
        if isinstance(self.perp, Vampire):
            clock.add_callback(self.wait)

    def wait(self) -> None:
        self.age += 1
        if self.age > 3:
            self.delete()
            name = self.name.strip("body of ")
            if DEBUG:
                self.say(name + " rises as a vampire!")
            Vampire(name, self.location, self.perp)

    def delete(self) -> None:
        clock.remove_callback(self.wait)
        super(Body, self).delete()


class Avatar(Person):
    """The Avatar of the user is also a Person."""

    def __init__(self, name: str, birthplace: Place):
        super(Avatar, self).__init__(name, birthplace)

    def look(self) -> None:
        print("You are in " + self.location.name)
        if len(self.things) > 0:
            print("You are holding: " + ", ".join(u.names(self.things)))
        else:
            print("You are not holding anything.")
        if len(self.room_things()) > 0:
            print("You see things in the room: " + ", ".join(u.names(self.room_things())))
        else:
            print("There is nothing in the room.")
        if len(self.people_around()) > 0:
            print("You see other people: " + ", ".join(u.names(self.people_around())))
        else:
            print("There are no other people around you.")
        if len(self.location.exits) > 0:
            print("The exits are in directions: " + ", ".join(u.names(self.location.exits)))
        else:
            print("There are no exits... you are dead and gone to heaven!")

    def go(self, direction: str) -> bool:
        success: bool = super(Avatar, self).go(direction)
        if success:
            clock.tick()
            self.look()
        return success

    def die(self, perp: Person):
        self.say("Woe, I am slain!")
        super(Avatar, self).die(perp)


# avoiding circular imports
clock: Clock = Clock()


def current_time():
    return clock.time


def run_clock(x):
    while x > 0:
        clock.tick()
        x -= 1
