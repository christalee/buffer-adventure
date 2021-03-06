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
        # TODO is there an actual need for self.removed_callbacks?
        self.time: int = 0
        self.callbacks: List[Callable] = []
        self.removed_callbacks: List[Callable] = []

        super(Clock, self).__init__('Clock')
        self.add_callback(self.print_tick)

    def __repr__(self) -> str:
        return self.name

    def reset(self) -> None:
        # should this just... create a new Clock?
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
        normal = random.randint(1, self.damage)

        chance = random.randint(1, 10)
        if chance == 1:
            normal *= 10

        hits = normal + perp.strength
        target.suffer(hits, perp)


class Tool(Mobile_Thing):
    """A Tool is a Mobile_Thing that contributes to its owner's magic."""

    def __init__(self, name: str, location: 'Place', magic: int):
        self.magic = magic
        super(Tool, self).__init__(name, location)


class Place(Container, Named_Object):
    """
    A Place is a Container (so Things may be in the Place).

    A Place has Exits, which are passages from one place to another. One can retrieve all of the Exits of a Place, or an Exit in a given direction from Place.
    """

    def __init__(self, name: str):
        self.exits: List[Exit] = []

        Named_Object.__init__(self, name)
        super(Place, self).__init__()

    def add_exit(self, exit: 'Exit') -> bool:
        if exit.name in u.names(self.exits):
            if DEBUG:
                print(self.name + " already has an exit to " + exit.name)
            return False
        else:
            self.exits.append(exit)
            if DEBUG:
                print(exit.name + " added at " + self.name)
            return True


class Hideout(Place):
    """A Hideout is a Place only reachable through an Exit with a non-zero magic level. When a Hacker finds themself in one, they sign in."""

    def __init__(self, name: str):
        super(Hideout, self).__init__(name)


class Exit(Named_Object):
    """An Exit leads from one Place to another Place in some direction."""

    def __init__(self, origin: Place, direction: str, destination: Place, magic: int = 0):
        self.origin = origin
        self.direction = direction
        self.destination = destination
        self.magic = magic

        super(Exit, self).__init__(direction + "->" + destination.name)

        if isinstance(self.destination, Hideout) and self.magic == 0:
            if DEBUG:
                print(self.name + " must have some magic to reach this destination")
            self.delete()
        else:
            self.origin.add_exit(self)


# There are several kinds of Person:
# There are Autonomous_Persons, including Vampires, and there is the Avatar of the user. The foundation is here.
class Person(Container, Mobile_Thing):
    """A Person can move around (is a Mobile_Thing), and can hold Things (is a Container). A Person has a plethora of methods."""

    def __init__(self, name: str, birthplace: Place):
        self.health: int = 3
        self.strength: int = 1
        self.magic: int = 0
        self.things: List[Mobile_Thing]
        self.weapon: Optional[Weapon] = None

        Mobile_Thing.__init__(self, name, birthplace)
        super(Person, self).__init__()

    def have_fit(self) -> None:
        self.say("Yaaaah! I am upset!")
        self.say("I feel better now.")

    def shirt(self):
        self.say(self.name + ' is wearing a shirt that says: ' + random.choice(data.shirts))

    # TODO combine _around methods?
    def people_around(self) -> List['Person']:
        people: List[Person] = u.find_all(self.location, Person)
        people.remove(self)
        return people

    def room_things(self) -> List[Thing]:
        things: List[Thing] = list(filter(lambda t: not isinstance(t, Person) and not t.owner, self.location.things))
        return things

    def people_things(self) -> List[Mobile_Thing]:
        all_items: List[Mobile_Thing] = []
        for p in self.people_around():
            itemlist: List[Mobile_Thing] = p.things
            if itemlist:
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
            n = item.owner.name if item.owner else item.location.name
            self.say("I take " + item.name + " from " + n)
            item.change_owner(self)

            if isinstance(item, Tool):
                self.magic += item.magic

            return True

    def drop(self, itemname: str) -> bool:
        item: Optional[Mobile_Thing] = u.thingfind(itemname, self.things)
        if item:
            self.say("I drop " + item.name + " at " + self.location.name)
            item.change_owner(None)
            if item == self.weapon:
                self.weapon = None
            return True
        else:
            self.say("I don't have that item!")
            return False

    def equip(self, weapon: str):
        w = u.thingfind(weapon, self.things)
        if isinstance(w, Weapon):
            self.weapon = w
            if DEBUG:
                self.say(weapon + " equipped!")
        else:
            self.say("You can only equip weapons, sorry.")

    def go(self, direction: Optional[str] = None) -> bool:
        exit: Optional[Exit] = u.find_exit(self.location.exits, direction) if direction else u.random_exit(self.location)

        if exit:
            if self.magic >= exit.magic:
                if DEBUG:
                    print(self.name + " moves from " + self.location.name + " to " + exit.destination.name)
                self.change_location(exit.destination)
                return True
            else:
                print(self.name + " is insufficiently clueful to use this route")
                return False
        else:
            # TODO tell_room()
            print(self.location, "No exit in " + str(direction) + " direction")
            return False

    def change_location(self, new_location: Place):
        super(Person, self).change_location(new_location)
        for t in self.things:
            t.change_location(new_location)

        others = self.people_around()
        if others:
            self.say("Hi " + ", ".join(u.names(others)))

    def suffer(self, hits: int, perp: 'Person'):
        # negative hits aren't ok
        hits = max(hits - self.strength, 0)
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

        # pick a weapon: the strongest item in inventory, or fists if you have no weapons
        if not self.weapon:
            weapons: List[Weapon] = u.find_all(self, Weapon)
            if not weapons:
                self.say(self.name + " punches " + target + "!")
                victim.suffer(3, self)
                # punching makes you stronger
                self.strength += 1
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


class Autonomous_Person(Person):
    """
    A Person that can change Places and pick up Things.

    activity determines maximum movement
    miserly determines chance of picking stuff up
    """

    def __init__(self, name: str, birthplace: Place):
        self.activity: int = random.randint(1, 3)
        self.miserly: int = random.randint(1, 3)

        super(Autonomous_Person, self).__init__(name, birthplace)
        clock.add_callback(self.move_and_take)

    def move_and_take(self) -> None:
        moves: int = random.randrange(self.activity)
        for x in range(moves):
            self.go()
        if random.randrange(self.miserly) == 0:
            self.take()
        if self.people_around():
            self.hack()
        if DEBUG:
            self.say("I'm done moving for now.")

    def take(self, itemname='') -> bool:
        items: List[Thing] = self.people_things() + self.room_things()
        if not items:
            if DEBUG:
                self.say("Whoops, there's nothing here to take.")
            return False

        if items and not itemname:
            itemname = random.choice(items).name
        return super(Autonomous_Person, self).take(itemname)

    def hack(self):
        jacks: List[Autonomous_Person] = list(filter(lambda x: x.magic > 5, self.people_around()))
        if jacks:
            self.magic += random.randint(1, 3)
            random.choice(jacks).shirt()

    def die(self, perp: Person) -> None:
        # should this remove all callbacks for self??
        # no, some callbacks might persist after death
        clock.remove_callback(self.move_and_take)
        if DEBUG:
            self.say("Aaaaahhhh! I suddenly feel very faint...")
        super(Autonomous_Person, self).die(perp)


class Oracle(Autonomous_Person):
    """An Oracle is an Autonomous_Person who walk the halls muttering gloomy predictions of the future."""

    def __init__(self, birthplace: Place):
        self.name: str = "nostradamus"
        super(Oracle, self).__init__(self.name, birthplace)

    def move_and_take(self) -> None:
        self.say(random.choice(data.sayings))
        super(Oracle, self).move_and_take()

    def die(self, perp: Person):
        self.say("At last, the stars are right!")
        super(Oracle, self).die(perp)


class Slayer(Autonomous_Person):
    """The Slayer wanders around, hunting Vampires (but no one else!) They only take 1 damage from Vampires and should look for a Holy_Object if they don't have one. If the Slayer is killed, a new one should emerge."""

    def __init__(self, birthplace: Place):
        self.name: str = "bram-stoker"
        super(Slayer, self).__init__(self.name, birthplace)

        self.activity: int = random.randint(5, 10)
        self.health: int = random.randint(5, 10)
        self.magic: int = random.randint(1, 5)

    def go(self):
        self.slay()
        super(Slayer, self).go()

    def slay(self) -> bool:
        vamps = u.find_all(self.location, Vampire)
        if vamps:
            target = random.choice(vamps)
            self.attack(target)
            return True
        else:
            if DEBUG:
                self.say("There's no one here to slay!")
            return False

    def take(self, itemname: str = ''):
        holies = u.find_all(self, Holy_Object)
        holy_items = list(filter(lambda t: isinstance(t, Holy_Object), self.room_things() + self.people_things()))

        itemname = '' if holies or not holy_items else random.choice(holy_items).name
        super(Slayer, self).take(itemname)

    def suffer(self, hits: int, perp: Person):
        if isinstance(perp, Vampire):
            # TODO this is a clumsy way of reducing Vampire damage to 1
            hits = 1 + self.strength
        super(Slayer, self).suffer(hits, perp)

    def die(self, perp: Person):
        # TODO figure out how to respawn
        self.say("Time for another ride on the wheel of dharma...")
        super(Slayer, self).die(perp)
        Slayer(random.choice(rooms))


class Hacker(Autonomous_Person):
    """The Hacker is available to learn magic from.  When a Hacker finds themself in a Hideout, they sign in."""

    def __init__(self, birthplace: Place):
        self.name: str = 'jack-florey'
        super(Hacker, self).__init__(self.name, birthplace)
        self.magic: int = 10

    def hack(self):
        if isinstance(self.location, Hideout):
            self.say("I'm going to sign in at " + self.location.name)
            Thing("sign-in: " + self.name, self.location)
        super(Hacker, self).hack()


class Vampire(Autonomous_Person):
    """An undead Person that randomly attacks people."""

    def __init__(self, name: str, birthplace: Place, sire: Optional['Vampire']):
        self.sire = sire
        super(Vampire, self).__init__(name, birthplace)

        if self.sire:
            self.strength = 2
            self.sire.strength += 1
            if DEBUG:
                self.sire.say(self.sire.name + " got stronger")
        else:
            self.strength = 10

    def move_and_take(self) -> None:
        # Note: this does not call super.move_and_take()!!
        if random.randrange(2) == 0:
            self.go()
        if random.randrange(3) < 2:
            self.attack()
        if DEBUG:
            self.say("I'm done moving for now.")

    def attack(self, target='') -> None:
        others = list(filter(lambda x: isinstance(x, Person) and not isinstance(x, Vampire), self.people_around()))
        if others:
            victim = random.choice(others)
            self.say(self.name + " bites " + victim.name + "!")
            for t in victim.things:
                if isinstance(t, Holy_Object):
                    self.say('Curses! Foiled again!')
                    break
            else:
                victim.suffer(random.randrange(self.strength), self)
                if DEBUG:
                    print(self.name + " is tired")

    def die(self, perp: Person):
        if DEBUG:
            self.say(self.name + " turns to dust!")
        clock.remove_callback(self.move_and_take)
        self.delete()


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

        if self.things:
            print("You are holding: " + ", ".join(u.names(self.things)))
        else:
            print("You are not holding anything.")

        if self.room_things():
            print("You see things in the room: " + ", ".join(u.names(self.room_things())))
        else:
            print("There is nothing in the room.")

        if self.people_around():
            print("You see other people: " + ", ".join(u.names(self.people_around())))
        else:
            print("There are no other people around you.")

        if self.location.exits:
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
    for i in range(x):
        clock.tick()
