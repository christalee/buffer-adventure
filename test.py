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


# Named_Object
def test_object_init(named_object):
    no = named_object("test object")

    assert no.name == "test object"
    assert no.installed


def test_object_delete(named_object):
    no = named_object("test object")

    assert no.installed
    no.delete()
    assert not no.installed


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

    # TODO should this use container.add_thing instead of setting it directly?
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

    # If I try to add cat again, it shouldn't add a 2nd cat
    container.add_thing(cat)
    assert container.have_thing(cat)
    assert container.things == [cat]

# TODO are there things that shouldn't be in Containers?


def test_container_remove_thing(container, thing, place):
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
    assert clock.removed_callbacks == []
    assert clock.name == 'Clock'
    assert clock.callbacks == [clock.print_tick]


def test_clock_reset(clock):
    clock.time = 5
    clock.reset()
    assert clock.time == 0
    assert clock.callbacks == [clock.print_tick]


def test_clock_tick(clock):
    pass


def test_clock_add_callback(clock):
    assert clock.callbacks == [clock.print_tick]

    clock.add_callback(clock.reset)
    assert clock.callbacks == [clock.print_tick, clock.reset]
    # you can't add the same callback twice
    clock.add_callback(clock.reset)
    assert clock.callbacks == [clock.print_tick, clock.reset]


def test_clock_remove_callback(clock):
    assert clock.removed_callbacks == []
    assert clock.callbacks == [clock.print_tick]

    clock.remove_callback(clock.print_tick)
    assert clock.callbacks == []
    assert clock.removed_callbacks == [clock.print_tick]

    # you can't remove the same callback twice
    clock.remove_callback(clock.print_tick)
    assert clock.callbacks == []
    assert clock.removed_callbacks == [clock.print_tick]


# Thing
def test_thing_init(place, thing):
    bed = place("bed")
    cat = thing("cat", bed)

    assert cat.location == bed
    assert bed.have_thing(cat)


def test_thing_delete(place, thing):
    bed = place("bed")
    cat = thing("cat", bed)

    assert bed.have_thing(cat)
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

    assert grail.name == 'grail'
    assert grail.location == table
    assert table.have_thing(grail)


# Weapon
def test_weapon_init(weapon, place):
    floor = place("floor")
    relic = weapon("relic", floor, 5)

    assert relic.damage == 5


def test_weapon_hit(weapon, place, person):
    # TODO test this more thoroughly
    floor = place("floor")
    relic = weapon("relic", floor, 5)
    dave = person("Dave", floor)
    bob = person("Bob", floor)

    assert dave.health == 3
    relic.hit(bob, dave)
    assert dave.health < 3


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

    assert bed.exit_towards("down") == exit1


def test_place_add_exit(place, exit):
    bed = place("bed")
    floor = place("floor")
    exit1 = exit(bed, "down", floor)

    # TODO is this needed, since exit1 calls bed.add_exit?
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
    assert bed.exits == [exit1]


def test_exit_use(place, exit, person):
    bed = place("bed")
    floor = place("floor")
    exit1 = exit(bed, "down", floor)
    alice = person("Alice", bed)

    # TODO is this redundant with test_person_init?
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

    assert alice.room_things() == [cat, blanket]


def test_person_people_things(person, place, mthing):
    floor = place("floor")
    dave = person("Dave", floor)
    bob = person("Bob", floor)
    dog = mthing("dog", floor)

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


def test_person_drop(person, place, mthing):
    floor = place("floor")
    dave = person("Dave", floor)
    dog = mthing("dog", floor)

    dave.take(dog.name)
    assert dave.things == [dog]
    assert dog.location == dave

    dave.drop(dog.name)
    assert dave.things == []
    assert dog.location == dave.location
    assert dog.location == floor
    assert floor.have_thing(dog)

    # you can't drop a thing you don't have
    assert not dave.drop(dog.name)


def test_person_go(person, place, exit):
    bed = place("bed")
    floor = place("floor")
    alice = person("Alice", bed)
    exit1 = exit(bed, "down", floor)

    assert alice.location == bed
    assert alice.go("down")
    assert alice.location == floor
    # if there isn't an exit, you can't go that way
    assert not alice.go("down")


def test_person_wander(person, place, exit):
    bed = place("bed")
    floor = place("floor")
    table = place("table")
    alice = person("Alice", bed)
    exit1 = exit(bed, "down", floor)
    exit2 = exit(bed, "left", table)

    assert alice.location == bed
    alice.wander()
    assert alice.location in [floor, table]


def test_person_suffer(person, place):
    floor = place("floor")
    dave = person("Dave", floor)
    bob = person("Bob", floor)

    assert dave.health == 3
    dave.suffer(2, bob)
    assert dave.health == 1


def test_person_attack(person, place, weapon):
    floor = place("floor")
    dave = person("Dave", floor)
    bob = person("Bob", floor)
    chair = weapon("chair", floor, 2)

    # you can't attack someone who's not there
    assert not dave.attack("Alice")
    # without a weapon, you can punch someone
    assert bob.health == 3
    dave.attack('Bob')
    assert bob.health < 3
    # with a weapon, you can hit someone
    assert dave.health == 3
    bob.take(chair)
    bob.attack("Dave")
    assert dave.health < 3
    # TODO attack with multiple weapons


def test_person_die(person, place, mthing, weapon):
    floor = place("floor")
    dave = person("Dave", floor)
    bob = person("Bob", floor)
    dog = mthing("dog", floor)
    chair = weapon("chair", floor, 2)

    dave.take(dog.name)
    dave.take(chair.name)
    assert dave.things == [dog, chair]
    assert dave.installed

    dave.die(bob)
    assert not dave.installed
    assert dave.things == []
    assert dog in floor.things
    assert chair in floor.things
    # TODO this is clunky
    b = u.find_all(floor, o.Body)[0]
    assert b.name == "body of Dave"


def test_person_change_location(person, place):
    bed = place("bed")
    floor = place("floor")
    alice = person("Alice", bed)

    assert alice.location == bed
    alice.change_location(floor)
    assert alice.location == floor


# Autonomous_Person
def test_autop_init(autop, place, clock):
    floor = place("floor")
    chris = autop("Chris", floor, 3, 2)

    assert chris.activity == 3
    assert chris.miserly == 2
    assert chris.move_and_take in clock.callbacks


def test_autop_move_and_take(autop, place, exit, mthing, holy):
    bed = place("bed")
    floor = place("floor")
    table = place("table")
    chris = autop("Chris", bed, 1, 0)
    exit1 = exit(bed, "down", floor)
    exit2 = exit(bed, "left", table)
    dog = mthing("dog", floor)
    pillow = mthing("pillow", bed)
    grail = holy('grail', table)

    assert chris.location == bed
    assert chris.things == []

    chris.move_and_take()
    assert chris.location in [floor, table]
    assert len(chris.things) > 0


def test_autop_die(autop, place, person, clock):
    floor = place("floor")
    chris = autop("Chris", floor, 3, 2)
    bob = person("Bob", floor)

    chris.die(bob)
    assert chris.move_and_take not in clock.callbacks
    assert not chris.installed


def test_autop_take(autop, mthing, holy, place):
    floor = place("floor")
    chris = autop("Chris", floor, 3, 2)
    dog = mthing("dog", floor)

    assert chris.things == []
    assert chris.take()
    assert chris.things == [dog]
    # can't take something that isn't there
    assert not chris.take()


# Vampire
def test_vampire_init(vampire, place, clock):
    floor = place("floor")
    vlad = vampire("Vlad", floor, None)

    assert vlad.power == 10
    assert not vlad.sire
    assert vlad.rove_and_attack in clock.callbacks

    lestat = vampire("Lestat", floor, vlad)
    assert lestat.power == 2
    assert vlad.power == 11
    assert lestat.sire == vlad
    assert lestat.rove_and_attack in clock.callbacks


def test_vampire_die(vampire, place, person, clock):
    floor = place("floor")
    vlad = vampire("Vlad", floor, None)
    chris = person("Chris", floor)

    vlad.die(chris)
    assert vlad.rove_and_attack in clock.removed_callbacks


def test_vampire_gain_power(vampire, place):
    floor = place("floor")
    vlad = vampire("Vlad", floor, None)

    vlad.gain_power()
    assert vlad.power == 11


def test_vampire_rove_and_attack(vampire):
    pass


def test_vampire_attack(vampire, place, person, holy, mthing):
    floor = place("floor")
    vlad = vampire("Vlad", floor, None)
    lestat = vampire("Lestat", floor, vlad)
    chris = person("Chris", floor)
    ark = holy("covenant-ark", floor)
    dog = mthing("dog", floor)

    # have lestat attack because he's less powerful
    lestat.attack()
    assert chris.health <= 3
    # he shouldn't attack vlad
    assert vlad.health == 3

    # having a Holy_Object should keep him safe
    # TODO be more thorough / consider a separate test case
    chris.take(dog.name)
    chris.take(ark.name)
    lestat.attack()
    assert chris.health > 0


# Body
def test_body_init(body, place, vampire, person, clock):
    floor = place("floor")
    vlad = vampire("Vlad", floor, None)
    mal = body("Mal", floor, vlad)

    assert mal.age == 0
    assert mal.perp == vlad
    assert mal.name == "body of Mal"
    assert mal.wait in clock.callbacks

    chris = person("Chris", floor)
    eve = body("Eve", floor, chris)

    assert eve.age == 0
    assert eve.perp == chris
    assert eve.name == "body of Eve"


def test_body_wait(body, place, vampire):
    floor = place("floor")
    vlad = vampire("Vlad", floor, None)
    mal = body("Mal", floor, vlad)

    mal.wait()
    assert mal.age == 1
    mal.wait()
    mal.wait()
    assert mal.age == 3
    assert mal.installed

    mal.wait()
    assert not mal.installed
    vmal = u.find_all(floor, o.Vampire)[1]
    assert vmal.name == "Mal"
    assert vmal.sire == vlad
    assert vmal.creation_site == floor


def test_body_delete(body, place, vampire, clock):
    floor = place("floor")
    vlad = vampire("Vlad", floor, None)
    mal = body("Mal", floor, vlad)

    mal.delete()
    assert not mal.installed
    assert mal.wait in clock.removed_callbacks


# Avatar
def test_avatar_init(place):
    bed = place("bed")
    talia = o.Avatar("Talia", bed)

    assert talia.name == "Talia"
    assert talia.location == bed
    assert bed.have_thing(talia)


def test_avatar_look():
    pass


def test_avatar_go(place, exit, clock):
    bed = place("bed")
    floor = place("floor")
    table = place("table")
    exit1 = exit(bed, "down", floor)
    exit2 = exit(bed, "left", table)
    talia = o.Avatar("Talia", bed)

    assert talia.go("left")
    assert talia.location == table
    assert clock.time == 1

    # you can't go in a direction without an exit
    assert not talia.go("right")


def test_avatar_die(place, vampire):
    bed = place("bed")
    talia = o.Avatar("Talia", bed)
    vlad = vampire("Vlad", bed, None)

    talia.die(vlad)
    assert not talia.installed


# Utils
def test_names(place, thing, person):
    bed = place("bed")
    floor = place("floor")
    blanket = thing("blanket", bed)
    cat = thing("cat", bed)
    bob = person("Bob", floor)

    objects = [bed, blanket, cat, bob]
    assert u.names(objects) == ['bed', "blanket", "cat", "Bob"]


def test_thingfind(place, thing, person):
    bed = place("bed")
    floor = place("floor")
    blanket = thing("blanket", bed)
    cat = thing("cat", bed)
    bob = person("Bob", floor)

    objects = [bed, blanket, cat, bob]
    assert u.thingfind("cat", objects) == cat
    assert not u.thingfind("rug", objects)


def test_find_all(place, thing, person, mthing):
    bed = place("bed")
    blanket = thing("blanket", bed)
    cat = thing("cat", bed)
    pillow = mthing("pillow", bed)

    assert bed.things == [blanket, cat, pillow]
    assert u.find_all(bed, o.Mobile_Thing) == [pillow]


def test_find_exit(exit, place):
    bed = place("bed")
    floor = place("floor")
    table = place("table")
    exit1 = exit(bed, "down", floor)
    exit2 = exit(bed, "left", table)

    assert bed.exits == [exit1, exit2]
    assert u.find_exit(bed.exits, "left") == exit2
    # find a way to test the else clauses here


def test_random_exit(exit, place):
    bed = place("bed")
    floor = place("floor")
    table = place("table")
    exit1 = exit(bed, "down", floor)
    exit2 = exit(bed, "left", table)

    # TODO are these redundant or prudent?
    assert u.random_exit(bed) in bed.exits
    assert u.random_exit(bed) in [exit1, exit2]


def test_current_time():
    pass


def test_run_clock():
    pass
