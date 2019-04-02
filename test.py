import objects as o
# import setup as s
import utilities as u

# class TestWorld():
#     def __init__(self):
#         self.buffer = []
#
#     def tell_room(self, location, text):
#         self.buffer.append([location, text])
#
#     def lastsaid(self):
#         return self.buffer[0]

#w = create_world()
#s = w["10-250"]
#e = Exit(s, "east", w["building-13"])
#t = Mobile_Thing("Trotsky", s)
#
# print s.name
# print s.installed
# s.install()
# print s.installed
# s.delete()
# print s.installed
#
# print names(s.things)
# t.install()
# print names(s.things)
# t.delete()
# print names(s.things)
#
# print t.creation_site.name
# print t.location.name
# print names(w["34-301"].things)
# t.change_location(w["34-301"])
# print t.location.name
# print names(w["34-301"].things)
#
# t.enter_room()
# t.leave_room()
#t.emit("suddenly, a shot rang out!")
#
# print names(s.exits)
# e.install()
# print names(s.exits)
# e.install()
# print random_exit(s)
# print random_exit(s)
# print s.exit_towards('east').destination.name
#
# print e.origin.name
# print e.direction
# print e.destination.name


# Named_Object
def test_object_init(named_object):
    no = named_object("test object")

    assert no.name == "test object"
    assert not no.isInstalled

    no.install()
    assert no.isInstalled


def test_object_delete(named_object):
    no = named_object("test object")

    no.install()
    no.delete()
    assert not no.isInstalled


# Container
def test_container_init(container):
    assert container.things == []


def test_container_have_thing(container, thing, place):
    bed = place("bed")
    floor = place("floor")
    cat = thing("cat", bed)
    rug = thing("rug", floor)
    blanket = thing("blanket", bed)
    box = thing("box", floor)

    assert not container.have_thing(cat)

    container.things = [cat, rug, blanket]
    assert container.have_thing(rug)
    assert not container.have_thing(box)


def test_container_add_thing(container, thing, place):
    bed = place("bed")
    cat = thing("cat", bed)

    assert not container.have_thing(cat)

    container.add_thing(cat)
    assert container.have_thing(cat)
    assert container.things == [cat]

    # If I try to add thing1 again, it shouldn't add a 2nd copy
    container.add_thing(cat)
    assert container.have_thing(cat)
    assert container.things == [cat]

# TODO are there things that shouldn't be in Containers?


def test_container_delete_thing(container, thing, place):
    bed = place("bed")
    floor = place("floor")
    cat = thing("cat", bed)
    rug = thing("rug", floor)
    blanket = thing("blanket", bed)

    assert not container.have_thing(cat)

    container.add_thing(cat)
    container.add_thing(rug)
    container.remove_thing(cat)
    assert container.things == [rug]
    assert not container.have_thing(cat)

    # can't delete something that isn't there
    container.remove_thing(blanket)
    assert container.things == [rug]
    assert not container.have_thing(blanket)


# Clock
def test_clock_init(clock):
    assert clock.time == 0
    assert clock.callbacks == []
    assert clock.removed_callbacks == []
    assert clock.name == 'Clock'


def test_clock_install(clock):
    assert clock.callbacks == []
    clock.install()
    assert clock.callbacks == [clock.print_tick]


def test_clock_reset(clock):
    clock.time = 5
    clock.install()
    assert clock.callbacks == [clock.print_tick]

    clock.reset()
    assert clock.time == 0
    assert clock.callbacks == []


def test_clock_tick(clock):
    pass


def test_clock_add_callback(clock):
    pass


# Thing
def test_thing_init(place, thing):
    bed = place("bed")
    cat = thing("cat", bed)

    assert cat.location == bed


def test_thing_install(place, thing):
    bed = place("bed")
    cat = thing("cat", bed)

    cat.install()
    assert bed.have_thing(cat)


def test_thing_delete(place, thing):
    bed = place("bed")
    cat = thing("cat", bed)

    cat.install()
    cat.delete()
    assert not bed.have_thing(cat)

# def test_thing_say():
    # find something to write here that isn't ridiculous


# Mobile_Thing
def test_mthing_init(place, mthing):
    floor = place("floor")
    dog = mthing("dog", floor)

    assert dog.creation_site == floor


def test_mthing_change_location(place, mthing):
    floor = place("floor")
    bed = place("bed")
    dog = mthing("dog", floor)

    dog.install()
    assert dog.location == floor
    assert floor.have_thing(dog)

    dog.change_location(bed)
    assert not floor.have_thing(dog)
    assert dog.location == bed
    assert bed.have_thing(dog)


# Holy_Object
# TODO this might be entirely superfluous
def test_holy_init(holy, place):
    table = place("table")
    grail = holy('grail', table)

    grail.install()
    assert grail.name == 'grail'
    assert grail.location == table
    assert table.have_thing(grail)


# Weapon


# Place
def test_place_init(place):
    bed = place("bed")

    assert bed.exits == []
    assert bed.name == 'bed'
    # TODO is this the right way to test the inheritance?
    assert isinstance(bed, o.Container)
    assert isinstance(bed, o.Named_Object)


def test_place_exit_towards(place, exit):
    bed = place("bed")
    floor = place("floor")
    exit1 = exit(bed, "down", floor)

    bed.add_exit(exit1)
    assert bed.exit_towards("down") == exit1


def test_place_add_exit(place, exit):
    bed = place("bed")
    floor = place("floor")
    exit1 = exit(bed, "down", floor)

    assert bed.exits == []
    assert bed.add_exit(exit1)
    assert bed.exits == [exit1]
    # TODO find some way to test the else case
    assert not bed.add_exit(exit1)


# Exit
def test_exit_init(place, exit):
    bed = place("bed")
    floor = place("floor")
    exit1 = exit(bed, "down", floor)

    assert exit1.origin == bed
    assert exit1.direction == 'down'
    assert exit1.destination == floor


def test_exit_install(place, exit):
    bed = place("bed")
    floor = place("floor")
    exit1 = exit(bed, "down", floor)

    # TODO is this redundant with test_place_add_exit?
    exit1.install()
    assert bed.exits == [exit1]


def test_exit_use(place, exit, person):
    bed = place("bed")
    floor = place("floor")
    exit1 = exit(bed, "down", floor)
    alice = person("Alice", bed)

    exit1.install()
    alice.install()
    # TODO is this redundant with test_person_install?
    assert alice.location == bed
    assert bed.have_thing(alice)

    exit1.use(alice)
    assert alice.location == floor
    assert floor.have_thing(alice)
    assert not bed.have_thing(alice)


# Person
def test_person_init(person, place):
    floor = place("floor")
    bob = person("Bob", floor)

    assert bob.health == 3
    assert bob.strength == 1
    assert bob.name == "Bob"
    assert bob.creation_site == floor

    assert isinstance(bob, o.Mobile_Thing)
    assert isinstance(bob, o.Container)

# def test_say(self):
#     self.person.say("This is only a test.")
#     self.assertEqual(world.lastsaid, [self.person.location, "At New York Alice says: This is only a test."])

# def test_have_fit(self):
#     self.person.have_fit()
#     self.assertEqual(world.lastsaid, [self.person.location, "At New York Alice says: Yaaaah! I am upset!"])


def test_person_people_around(person, place, exit):
    bed = place("bed")
    floor = place("floor")
    alice = person("Alice", bed)
    bob = person("Bob", floor)
    exit1 = exit(bed, "down", floor)

    alice.install()
    bob.install()
    assert alice.people_around() == []
    assert bob.people_around() == []

    exit1.use(alice)
    assert alice.people_around() == [bob]
    assert bob.people_around() == [alice]


def test_person_room_things(person, place, thing):
    bed = place("bed")
    cat = thing("cat", bed)
    blanket = thing("blanket", bed)
    alice = person("Alice", bed)

    cat.install()
    blanket.install()
    assert alice.room_things() == [cat, blanket]


def test_person_people_things(person, place, mthing):
    floor = place("floor")
    dave = person("Dave", floor)
    bob = person("Bob", floor)
    dog = mthing("dog", floor)

    dog.install()
    dave.take(dog.name)
    assert bob.people_things() == [dog]
    assert dave.people_things() == []


def test_person_take(person, place, thing, mthing):
    bed = place("bed")
    floor = place("floor")
    dave = person("Dave", floor)
    bob = person("Bob", floor)
    rug = thing("rug", floor)
    dog = mthing("dog", floor)
    pillow = mthing("pillow", bed)

    assert dave.things == []

    dog.install()
    dave.take(dog.name)
    assert dave.things == [dog]
    assert dog.location == dave

    # once you have it, you can't take it again
    assert not dave.take(dog.name)
    # if it's not here, you can't take it
    assert not dave.take(pillow.name)
    # if it's not a Mobile_Thing, you can't take it
    assert not dave.take(rug.name)
    # you can't take a Person either
    assert not dave.take(bob.name)

# TODO finish the rest of the methods, classes


# Utils
def test_names(place, thing, person):
    bed = place("bed")
    floor = place("floor")
    blanket = thing("blanket", bed)
    cat = thing("cat", bed)
    bob = person("Bob", floor)

    blanket.install()
    cat.install()
    bob.install()
    objects = [bed, blanket, cat, bob]
    assert u.names(objects) == ['bed', "blanket", "cat", "Bob"]


def test_thingfind(place, thing, person):
    bed = place("bed")
    floor = place("floor")
    blanket = thing("blanket", bed)
    cat = thing("cat", bed)
    bob = person("Bob", floor)

    blanket.install()
    cat.install()
    bob.install()
    objects = [bed, blanket, cat, bob]
    assert u.thingfind("cat", objects) == cat
    assert not u.thingfind("rug", objects)


def test_find_all(place, thing, person, mthing):
    bed = place("bed")
    blanket = thing("blanket", bed)
    cat = thing("cat", bed)
    pillow = mthing("pillow", bed)

    blanket.install()
    cat.install()
    pillow.install()
    assert bed.things == [blanket, cat, pillow]
    assert u.find_all(bed, o.Mobile_Thing) == [pillow]


def test_find_exit(exit, place):
    bed = place("bed")
    floor = place("floor")
    table = place("table")
    exit1 = exit(bed, "down", floor)
    exit2 = exit(bed, "left", table)

    exit1.install()
    exit2.install()
    assert bed.exits == [exit1, exit2]
    assert u.find_exit(bed.exits, "left") == exit2
    # find a way to test the else clauses here


def test_random_exit(exit, place):
    bed = place("bed")
    floor = place("floor")
    table = place("table")
    exit1 = exit(bed, "down", floor)
    exit2 = exit(bed, "left", table)

    exit1.install()
    exit2.install()
    assert u.random_exit(bed) in bed.exits
