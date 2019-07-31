# objects.py
# Christalee Bieber, 2016
# cbieber@alum.mit.edu
#
# This file defines a clock and a screen that act as the game world, plus classes for game objects.

# TODO skipping network-mode, whatever that is

import random
from typing import Callable, Dict, List, Optional, Union

import data
import utilities as u

DEBUG: bool = True


class Named_Object:
    """
    Named_Objects are the basic underlying object type in our system. For example, Persons, Places, and Things will all be kinds of (inherit from) Named_Objects.

    Behavior (methods) supported by all Named_Objects:
    - Has a name that it can return
    - Handles an install message
    - Handles a delete message
    """

    def __init__(self, name) -> None:
        self.name: str = name
        self.installed: bool = True
        if DEBUG:
            print(self.name + " installed!")

    def __repr__(self) -> str:
        return self.name

    def delete(self) -> None:
        # TODO should this actually delete the object?
        self.installed = False
        if DEBUG:
            print(self.name + " deleted!")


class Container:
    """
    A Container holds Things.

    This class is not meant for "stand-alone" objects; rather, it is expected that other classes will inherit from the Container class in order to be able to contain Things.
    """

    def __init__(self) -> None:
        self.things: List['Thing'] = []

    def have_thing(self, x: 'Thing') -> bool:
        return x in self.things

    # TODO consider raising exceptions here?
    def add_thing(self, x: 'Thing') -> None:
        # TODO should these also world.tell_world()?
        if not self.have_thing(x) and isinstance(x, Thing):
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

    def __repr__(self) -> str:
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
        x = str(cb).split()
        if cb in self.callbacks:
            self.removed_callbacks.append(cb)
            self.callbacks.remove(cb)
            if DEBUG:
                print(x[-1].replace('>', '.') + x[2] + " removed")
        else:
            if DEBUG:
                print(x[-1].replace('>', '.') + x[2] + " doesn't exist")


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
        print("At " + self.location.name + ", " + self.name + " says: " + text)


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
        normal = random.randrange(1, self.damage)
        chance = random.randrange(1, 10)

        if chance == 1:
            target.suffer(10 * normal, perp)
        else:
            target.suffer(normal, perp)


class Place(Container, Named_Object):
    """
    A Place is a Container (so Things may be in the Place).

    A Place has Exits, which are passages from one place to another. One can retrieve all of the Exits of a Place, or an Exit in a given direction from Place.
    """

    def __init__(self, name: str):
        self.exits: List[Exit] = []

        Named_Object.__init__(self, name)
        super(Place, self).__init__()

    def exit_towards(self, direction: str):
        return u.find_exit(self.exits, direction)

    def add_exit(self, exit: 'Exit'):
        if exit in self.exits:
            if DEBUG:
                print(self.name + " already has an exit to " + exit.name)
            return False
        else:
            self.exits.append(exit)
            if DEBUG:
                print(exit.name + " added at " + self.name)
            return True


class Exit(Named_Object):
    """An Exit leads from one Place to another Place in some direction."""

    def __init__(self, origin: Place, direction: str, destination: Place):
        self.origin = origin
        self.direction = direction
        self.destination = destination

        super(Exit, self).__init__(direction + "->" + destination.name)
        self.origin.add_exit(self)

    def use(self, who: 'Person'):
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
        self.weapon: Optional[Weapon] = None

        Mobile_Thing.__init__(self, name, birthplace)
        super(Person, self).__init__()

    def have_fit(self) -> None:
        self.say("Yaaaah! I am upset!")
        self.say("I feel better now.")

    # TODO combine _around methods?
    def people_around(self) -> List['Person']:
        people: List[Person] = u.find_all(self.location, Person)
        people.remove(self)
        return people

    def room_things(self) -> List[Thing]:
        things: List[Thing] = list(filter(lambda t: not isinstance(t, Person) and not t.owner, self.location.things))
        # [t for t in self.location.things if not t.owner and not isinstance(t, Person)]
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
            if item == self.weapon:
                self.weapon = None
            return True
        else:
            self.say("I don't have that item!")
            return False

    def go(self, direction: str = None) -> bool:
        if direction:
            exit: Exit = self.location.exit_towards(direction)
        else:
            exit: Exit = u.random_exit(self.location)

        if exit:
            exit.use(self)
            return True
        else:
            # TODO tell_room()
            print(self.location, "No exit in " + direction + " direction")
            return False

    def suffer(self, hits: int, perp: 'Person'):
        self.say("Ouch! " + str(hits) + " damage is more than I want!")
        self.health -= hits
        if self.health <= 0:
            self.die(perp)
        if DEBUG:
            print('Health: ' + str(self.health))

    def equip(self, weapon: str):
        w = u.thingfind(weapon, self.things)
        if isinstance(w, Weapon):
            self.weapon = w
            if DEBUG:
                self.say(weapon + " equipped!")
        else:
            self.say("You can only equip weapons, sorry.")

    def attack(self, target: str):
        victim: Optional[Person] = u.thingfind(target, self.people_around())
        if not victim:
            self.say("There's no one here to attack!")
            return False

        # pick a weapon: the strongest item in inventory, or fists if you have no weapons
        if not self.weapon:
            weapons: List[Optional[Weapon]] = u.find_all(self, Weapon)
            if len(weapons) == 0:
                self.say(self.name + " punches " + target + "!")
                victim.suffer(3, self)
                return True
            else:
                self.equip(max(weapons, key=lambda x: x.damage).name)

        self.weapon.hit(self, victim)
        return True

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
    """
    A Person that can change Places and pick up Things.

    activity determines maximum movement
    miserly determines chance of picking stuff up
    """

    def __init__(self, name: str, birthplace: Place):
        self.activity: int = random.randrange(1, 5)
        self.miserly: int = random.randrange(1, 4)

        super(Autonomous_Person, self).__init__(name, birthplace)
        clock.add_callback(self.move_and_take)

    def move_and_take(self) -> None:
        moves: int = random.randrange(self.activity)
        for x in range(moves):
            self.go()
        if random.randrange(self.miserly) == 0:
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
        if itemname == '' and items:
            itemname = random.choice(items).name
        if not items:
            if DEBUG:
                self.say("Whoops, there's nothing here to take.")
            return False

        return super(Autonomous_Person, self).take(itemname)


class Oracle(Autonomous_Person):
    """An Oracle is an Autonomous_Person who walk the halls muttering gloomy predictions of the future."""

    def __init__(self, birthplace: Place):
        self.name: str = "nostradamus"

        super(Oracle, self).__init__(self.name, birthplace)
        clock.add_callback(self.prophecy)

    def prophecy(self) -> None:
        self.say(random.choice(data.sayings))

    def die(self, perp: Person):
        clock.remove_callback(self.prophecy)
        self.say("At last, the stars are right!")
        super(Oracle, self).die(perp)


class Slayer(Autonomous_Person):
    """The Slayer wanders around, hunting Vampires (but no one else!) They only take 1 damage from Vampires and should look for a Holy_Object if they don't have one. If the Slayer is killed, a new one should emerge."""

    def __init__(self, birthplace: Place):
        self.name: str = "bram-stoker"

        super(Slayer, self).__init__(self.name, birthplace)
        self.activity: int = random.randrange(5, 10)
        self.miserly: int = random.randrange(5, 10)

    def go(self):
        self.slay()
        super(Slayer, self).go()

    def slay(self):
        vamps = u.find_all(self.location, Vampire)
        if vamps:
            target = random.choice(vamps)
            self.attack(target)
        else:
            if DEBUG:
                self.say("There's no one here to slay!")
            return False

    def take(self, itemname: str = ''):
        holies = u.find_all(self, Holy_Object)
        if len(holies) > 0:
            itemname = ''
        else:
            holy_items = u.find_all(self.location, Holy_Object)
            itemname = random.choice(holy_items).name

        super(Slayer, self).take(itemname)

    def die(self, perp: Person):
        global world
        self.say("Time for another ride on the wheel of dharma...")
        super(Slayer, self).die(perp)
        Slayer(random.choice(list(world.values())))

    def suffer(self, hits: int, perp: Person):
        if isinstance(perp, Vampire):
            hits = 1
        super(Slayer, self).suffer(hits, perp)


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
        clock.add_callback(self.move_and_attack)

    def die(self, perp: Person):
        if DEBUG:
            self.say(self.name + " turns to dust!")
        clock.remove_callback(self.move_and_attack)
        self.delete()

    def gain_power(self) -> None:
        self.power += 1
        if DEBUG:
            self.say(self.name + " gained power")

    def move_and_attack(self) -> None:
        if random.randrange(2) == 0:
            self.go()
        if random.randrange(3) < 2:
            self.attack()
        if DEBUG:
            self.say("I'm done moving for now.")

    def attack(self, target='') -> None:
        others = list(filter(lambda x: isinstance(x, Person) and not isinstance(x, Vampire), self.people_around()))
        if len(others) > 0:
            victim = random.choice(others)
            self.say(self.name + " bites " + victim.name + "!")
            for t in victim.things:
                if isinstance(t, Holy_Object):
                    self.say('Curses! Foiled again!')
                    break
            else:
                victim.suffer(random.randrange(self.power), self)
                if DEBUG:
                    print(self.name + " is tired")


class Body(Thing):
    """A Thing which has the potential to rise as a Vampire"""

    def __init__(self, name: str, location: Place, perp: Optional[Union[Person, Vampire]]):
        self.age: int = 0
        self.perp = perp
        self.name = "body of " + name

        super(Body, self).__init__(self.name, location)
        if isinstance(self.perp, Vampire):
            clock.add_callback(self.wait)

    def wait(self) -> None:
        self.age += 1
        if self.age > 3:
            self.delete()
            name = self.name.replace("body of ", '')
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
