import data
import objects as o
import utilities as u


def c(captured):
    return captured.readouterr().out


# Named_Object
def test_object_init(named_object, capsys):
    n = named_object("test object")

    assert n.name == "test object"
    assert n.installed
    assert "test object installed!" in c(capsys)


def test_object_delete(named_object, capsys):
    n = named_object("test object")

    assert n.installed
    n.delete()
    assert not n.installed
    assert "test object deleted!" in c(capsys)


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

    # If I add a Place, it shouldn't work
    container.add_thing(bed)
    assert not container.have_thing(bed)
    assert container.things == [cat]
# TODO are there Things that shouldn't be in Containers?


def test_container_remove_thing(container, thing, place):
    bed = place("bed")
    cat = thing("cat", bed)
    rug = thing("rug", bed)
    blanket = thing("blanket", bed)

    container.things = [cat, rug]
    container.remove_thing(cat)
    assert container.things == [rug]
    assert not container.have_thing(cat)

    # can't delete something that isn't there
    container.remove_thing(blanket)
    assert container.things == [rug]
    assert not container.have_thing(blanket)


# Clock
def test_clock_init():
    assert o.clock.time == 0
    assert o.clock.removed_callbacks == []
    assert o.clock.name == 'Clock'
    assert o.clock.callbacks == [o.clock.print_tick]


def test_clock_reset():
    o.clock.time = 5
    o.clock.add_callback(o.clock.reset)
    assert o.clock.time == 5
    assert o.clock.callbacks == [o.clock.print_tick, o.clock.reset]

    o.clock.reset()
    assert o.clock.time == 0
    assert o.clock.callbacks == [o.clock.print_tick]


def test_clock_tick(capsys):
    # TODO
    # o.clock.reset()
    #
    # o.clock.tick()
    # assert o.clock.time == 1
    # assert "Clock Tick" in c(capsys)
    pass


def test_clock_print_tick(capsys):
    o.clock.print_tick()
    assert "Clock Tick" in c(capsys)


def test_clock_add_callback(capsys):
    o.clock.reset()

    o.clock.add_callback(o.clock.reset)
    assert o.clock.callbacks == [o.clock.print_tick, o.clock.reset]
    assert "Clock.Clock.reset added" in c(capsys)

    # you can't add the same callback twice
    o.clock.add_callback(o.clock.reset)
    assert o.clock.callbacks == [o.clock.print_tick, o.clock.reset]
    assert "Clock.Clock.reset already exists" in c(capsys)


def test_clock_remove_callback(capsys):
    o.clock.reset()
    assert o.clock.removed_callbacks == []

    o.clock.remove_callback(o.clock.print_tick)
    assert o.clock.callbacks == []
    assert o.clock.removed_callbacks == [o.clock.print_tick]
    assert "Clock.Clock.print_tick removed" in c(capsys)

    # you can't remove the same callback twice
    o.clock.remove_callback(o.clock.print_tick)
    assert o.clock.callbacks == []
    assert o.clock.removed_callbacks == [o.clock.print_tick]
    assert "Clock.Clock.print_tick doesn't exist" in c(capsys)


# Thing
def test_thing_init(place, thing):
    bed = place("bed")
    cat = thing("cat", bed)

    assert cat.location == bed
    assert bed.have_thing(cat)
    assert not cat.owner


def test_thing_delete(place, thing):
    bed = place("bed")
    cat = thing("cat", bed)

    assert bed.have_thing(cat)
    cat.delete()
    assert not bed.have_thing(cat)


def test_thing_say(place, thing, capsys):
    bed = place("bed")
    cat = thing("cat", bed)

    cat.say("Meow!")
    assert "At bed, cat says: Meow!" in c(capsys)


# Mobile_Thing
def test_mthing_init(place, mthing):
    floor = place("floor")
    dog = mthing("dog", floor)

    assert dog.creation_site == floor


def test_mthing_change_location(place, mthing):
    floor = place("floor")
    bed = place("bed")
    dog = mthing("dog", floor)

    dog.change_location(bed)
    assert not floor.have_thing(dog)
    assert dog.location == bed
    assert bed.have_thing(dog)


def test_mthing_change_owner(person, place, mthing, capsys):
    floor = place("floor")
    dog = mthing("dog", floor)
    dave = person("Dave", floor)
    bob = person("Bob", floor)

    dog.change_owner(dave)
    assert dog.owner == dave
    assert dave.have_thing(dog)

    dog.change_owner(bob)
    assert dog.owner == bob
    assert not dave.have_thing(dog)
    assert bob.have_thing(dog)
    assert "At floor, Dave says: I lose dog" in c(capsys)

    dog.change_owner(None)
    assert not dog.owner
    assert not bob.have_thing(dog)


# Holy_Object
# TODO is this needed at all?
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


def test_weapon_hit(weapon, place, person, capsys):
    # TODO test this more thoroughly
    floor = place("floor")
    relic = weapon("relic", floor, 5)
    dave = person("Dave", floor)
    bob = person("Bob", floor)

    assert dave.health == 3
    relic.hit(bob, dave)
    assert dave.health < 3
    assert "Bob lays the smackdown on Dave!" in c(capsys)


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


def test_place_add_exit(place, exit, capsys):
    bed = place("bed")
    floor = place("floor")
    exit1 = exit(bed, "down", floor)

    # TODO is this needed, since exit1 calls bed.add_exit?
    assert bed.exits == [exit1]
    assert "down->floor added at bed"

    # can't add_exit twice
    assert not bed.add_exit(exit1)
    assert "bed already has an exit to down->floor" in c(capsys)


# Exit
def test_exit_init(place, exit):
    bed = place("bed")
    floor = place("floor")
    exit1 = exit(bed, "down", floor)

    assert exit1.origin == bed
    assert exit1.direction == 'down'
    assert exit1.destination == floor
    assert bed.exits == [exit1]
    assert exit1.name == 'down->floor'


def test_exit_use(place, exit, person):
    bed = place("bed")
    floor = place("floor")
    exit1 = exit(bed, "down", floor)
    alice = person("Alice", bed)

    exit1.use(alice)
    assert alice.location == floor
    assert floor.have_thing(alice)
    assert not bed.have_thing(alice)
    # TODO check that Alice's things go with her


# Person
def test_person_init(person, place):
    floor = place("floor")
    bob = person("Bob", floor)

    assert bob.health == 3
    assert bob.strength == 1
    assert not bob.weapon

    assert isinstance(bob, o.Mobile_Thing)
    assert isinstance(bob, o.Container)


def test_person_fit(person, place, capsys):
    floor = place("floor")
    bob = person("Bob", floor)

    bob.have_fit()
    assert "Yaaaah! I am upset!" in c(capsys)


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


def test_person_people_things(person, place, mthing, capsys):
    floor = place("floor")
    dave = person("Dave", floor)
    bob = person("Bob", floor)
    dog = mthing("dog", floor)

    assert dave.take(dog.name)
    assert bob.people_things() == [dog]
    assert dave.people_things() == []
    assert "At floor, Bob says: Dave has dog" in c(capsys)


def test_person_take(person, place, thing, mthing, capsys):
    bed = place("bed")
    floor = place("floor")
    dave = person("Dave", floor)
    bob = person("Bob", floor)
    rug = thing("rug", floor)
    dog = mthing("dog", floor)
    pillow = mthing("pillow", bed)

    assert dave.take(dog.name)
    assert dave.things == [dog]
    assert dog.owner == dave
    assert "I take dog from floor" in c(capsys)

    # once you have it, you can't take it again
    assert not dave.take(dog.name)
    assert "I am already carrying dog" in c(capsys)

    # if it's not here, you can't take it
    assert not dave.take(pillow.name)
    assert "Sorry, that item isn't here." in c(capsys)

    # if it's not a Mobile_Thing, you can't take it
    assert not dave.take(rug.name)
    assert "I try but cannot take rug" in c(capsys)

    # you can't take a Person either
    assert not dave.take(bob.name)
    assert "I try but cannot take Bob" in c(capsys)

    # if you take some Thing from another Person
    assert bob.take(dog.name)
    assert bob.things == [dog]
    assert dog.owner == bob
    assert 'I take dog from Dave' in c(capsys)


def test_person_drop(person, place, mthing, weapon, capsys):
    floor = place("floor")
    dave = person("Dave", floor)
    dog = mthing("dog", floor)
    relic = weapon("relic", floor, 5)

    assert dave.take(dog.name)
    assert dave.drop(dog.name)
    assert "I drop dog at floor" in c(capsys)
    assert dave.things == []
    assert not dog.owner
    assert dog.location == floor
    assert floor.have_thing(dog)

    # you can't drop a thing you don't have
    assert not dave.drop(dog.name)
    assert "I don't have that item!" in c(capsys)

    # drop your weapon, rebel scum!
    assert dave.take(relic.name)
    assert dave.drop(relic.name)
    assert not dave.weapon


def test_person_go(person, place, exit, capsys):
    bed = place("bed")
    floor = place("floor")
    table = place("table")
    alice = person("Alice", bed)
    exit1 = exit(bed, "down", floor)
    exit2 = exit(bed, "left", table)
    exit3 = exit(table, "right", bed)
    exit4 = exit(floor, "up", bed)

    assert alice.go("down")
    assert alice.location == floor

    # without a direction given, wander
    assert alice.go("up")
    assert alice.go()
    assert alice.location in [floor, table]

    # if there isn't an exit, you can't go that way
    assert not alice.go("down")
    assert "No exit in down direction" in c(capsys)


def test_person_suffer(person, place, capsys):
    floor = place("floor")
    dave = person("Dave", floor)
    bob = person("Bob", floor)

    dave.suffer(2, bob)
    assert dave.health == 1
    assert "Ouch!" in c(capsys)

    dave.suffer(2, bob)
    assert not dave.installed
    assert "body of Dave" in u.names(floor.things)


def test_person_equip(person, place, weapon, mthing, capsys):
    floor = place("floor")
    dave = person("Dave", floor)
    chair = weapon("chair", floor, 2)
    dog = mthing("dog", floor)

    dave.take(chair.name)
    dave.equip(chair.name)
    assert dave.weapon == chair
    assert "chair equipped!" in c(capsys)

    # can't equip Things that aren't Weapons
    dave.take(dog)
    dave.equip(dog)
    assert "You can only equip weapons, sorry." in c(capsys)


def test_person_attack(person, place, weapon, capsys):
    floor = place("floor")
    dave = person("Dave", floor)
    bob = person("Bob", floor)
    carol = person("Carol", floor)
    chair = weapon("chair", floor, 2)
    relic = weapon("relic", floor, 5)

    # you can't attack someone who's not there
    assert not dave.attack("Alice")
    assert "There's no one here to attack!" in c(capsys)

    # without a weapon, you can punch someone
    dave.attack('Bob')
    assert "Dave punches Bob!" in c(capsys)
    assert bob.health < 3

    # with a weapon, you can hit someone
    dave.take(chair.name)
    dave.take(relic.name)
    dave.attack("Carol")
    assert carol.health < 3
    assert "Dave lays the smackdown on Carol!" in c(capsys)

    # attacking without a Weapon equipped picks the strongest in inventory
    assert dave.weapon == relic


def test_person_die(person, place, mthing, weapon, capsys):
    floor = place("floor")
    dave = person("Dave", floor)
    bob = person("Bob", floor)
    dog = mthing("dog", floor)
    chair = weapon("chair", floor, 2)

    dave.take(dog.name)
    dave.take(chair.name)
    dave.die(bob)
    assert "An earth-shattering, soul-piercing scream is heard..." in c(capsys)
    assert not dave.installed
    assert dave.things == []
    assert set([dog, chair]) <= set(floor.things)
    assert "body of Dave" in u.names(floor.things)


def test_person_change_location(person, place, capsys):
    bed = place("bed")
    floor = place("floor")
    alice = person("Alice", bed)
    dave = person("Dave", floor)
    bob = person("Bob", floor)

    alice.change_location(floor)
    assert alice.location == floor
    assert "Hi Dave, Bob" in c(capsys)


# Autonomous_Person
def test_autop_init(autop, place):
    floor = place("floor")
    chris = autop("Chris", floor)

    assert chris.activity <= 5
    assert chris.miserly <= 4
    assert chris.move_and_take in o.clock.callbacks


def test_autop_move_and_take(autop, place, exit, mthing, holy, capsys):
    bed = place("bed")
    floor = place("floor")
    table = place("table")
    chris = autop("Chris", bed)
    exit1 = exit(bed, "down", floor)
    exit2 = exit(bed, "left", table)
    exit3 = exit(table, "right", bed)
    exit4 = exit(floor, "up", bed)
    dog = mthing("dog", floor)
    pillow = mthing("pillow", bed)
    grail = holy('grail', table)

    chris.miserly = 1
    chris.move_and_take()
    assert len(chris.things) > 0
    assert "I'm done moving for now" in c(capsys)


def test_autop_die(autop, place, person, capsys):
    floor = place("floor")
    chris = autop("Chris", floor)
    bob = person("Bob", floor)

    chris.die(bob)
    assert chris.move_and_take not in o.clock.callbacks
    assert "I suddenly feel very faint" in c(capsys)
    assert not chris.installed


def test_autop_take(autop, mthing, place, capsys):
    floor = place("floor")
    chris = autop("Chris", floor)
    dog = mthing("dog", floor)

    assert chris.take()
    assert chris.things == [dog]

    # can't take something that isn't there
    assert not chris.take()
    assert "Whoops, there's nothing here to take." in c(capsys)


# Oracle
def test_oracle_init(place):
    floor = place("floor")
    nostradamus = o.Oracle(floor)

    assert nostradamus.name == "nostradamus"
    assert nostradamus.prophecy in o.clock.callbacks


def test_oracle_prophecy(place, capsys):
    floor = place("floor")
    nostradamus = o.Oracle(floor)

    nostradamus.prophecy()
    assert c(capsys).split(": ")[-1].strip() in data.sayings


def test_oracle_die(place, vampire, capsys):
    floor = place("floor")
    nostradamus = o.Oracle(floor)
    vlad = vampire("Vlad", floor, None)

    nostradamus.die(vlad)
    assert "At last, the stars are right!" in c(capsys)


# Slayer
def test_slayer_init(place):
    floor = place("floor")
    slayer = o.Slayer(floor)

    assert slayer.name == "bram-stoker"
    assert slayer.activity >= 5
    assert slayer.health >= 5


def test_slayer_slay(place, vampire, capsys):
    floor = place("floor")
    slayer = o.Slayer(floor)
    vlad = vampire("Vlad", floor, None)

    slayer.slay()
    assert vlad.health < 10

    # if there's no Vampires to slay, do nothing
    vlad.die(slayer)
    slayer.slay()
    assert "There's no one here to slay!" in c(capsys)


def test_slayer_take(holy, place, mthing):
    floor = place("floor")
    slayer = o.Slayer(floor)
    grail = holy('grail', floor)
    relic = holy("relic", floor)
    dog = mthing("dog", floor)
    pillow = mthing("pillow", floor)

    # preferentially take a Holy_Object first
    slayer.take()
    assert grail in slayer.things or relic in slayer.things

    # then proceed with usual random take()
    slayer.take()
    # TODO is this the best way?
    assert len(slayer.things) == 2


def test_slayer_die(place, vampire, capsys):
    floor = place("floor")
    slayer = o.Slayer(floor)
    vlad = vampire("Vlad", floor, None)

    slayer.die(vlad)
    assert "Time for another ride on the wheel of dharma..." in c(capsys)
    assert not slayer.installed
    # TODO check that Slayer has respawned?


def test_slayer_suffer(place, vampire, person):
    floor = place("floor")
    slayer = o.Slayer(floor)
    vlad = vampire("Vlad", floor, None)
    chris = person("Chris", floor)

    s_health = slayer.health
    slayer.suffer(2, chris)
    assert slayer.health == s_health - 2

    slayer.suffer(3, vlad)
    assert slayer.health == s_health - 3


# Vampire
def test_vampire_init(vampire, place):
    floor = place("floor")
    vlad = vampire("Vlad", floor, None)

    assert vlad.power == 10
    assert not vlad.sire
    assert vlad.move_and_attack in o.clock.callbacks

    lestat = vampire("Lestat", floor, vlad)
    assert lestat.power == 2
    assert vlad.power == 11
    assert lestat.sire == vlad
    assert lestat.move_and_attack in o.clock.callbacks


def test_vampire_die(vampire, place, person, capsys):
    floor = place("floor")
    vlad = vampire("Vlad", floor, None)
    chris = person("Chris", floor)

    vlad.die(chris)
    assert vlad.move_and_attack in o.clock.removed_callbacks
    assert vlad.move_and_attack not in o.clock.callbacks
    assert "Vlad turns to dust!" in c(capsys)
    assert not vlad.installed


def test_vampire_gain_power(vampire, place, capsys):
    floor = place("floor")
    vlad = vampire("Vlad", floor, None)

    vlad.gain_power()
    assert vlad.power == 11
    assert "Vlad gained power" in c(capsys)


def test_vampire_move_and_attack(vampire):
    # TODO
    pass


def test_vampire_attack(vampire, place, person, holy, mthing, capsys):
    floor = place("floor")
    vlad = vampire("Vlad", floor, None)
    lestat = vampire("Lestat", floor, vlad)
    chris = person("Chris", floor)
    ark = holy("covenant-ark", floor)
    dog = mthing("dog", floor)

    # have lestat attack because he's less powerful
    lestat.attack()
    assert chris.health <= 3
    assert "Lestat bites Chris!" in c(capsys)

    # he shouldn't attack vlad
    assert vlad.health == 3

    # having a Holy_Object should keep him safe
    # TODO be more thorough / consider a separate test case
    chris.take(dog.name)
    chris.take(ark.name)
    lestat.attack()
    assert chris.health > 0
    assert 'Curses! Foiled again!' in c(capsys)


# Body
def test_body_init(body, place, vampire, person):
    floor = place("floor")
    vlad = vampire("Vlad", floor, None)
    mal = body("Mal", floor, vlad)

    assert mal.age == 0
    assert mal.perp == vlad
    assert mal.name == "body of Mal"
    assert mal.wait in o.clock.callbacks

    # if the perp isn't a Vampire, the body won't rise again
    chris = person("Chris", floor)
    eve = body("Eve", floor, chris)

    assert eve.wait not in o.clock.callbacks


def test_body_wait(body, place, vampire, capsys):
    floor = place("floor")
    vlad = vampire("Vlad", floor, None)
    mal = body("Mal", floor, vlad)

    mal.wait()
    mal.wait()
    mal.wait()
    assert mal.age == 3
    assert mal.installed

    mal.wait()
    assert not mal.installed
    vmal = u.thingfind("Mal", floor.things)
    assert vmal.name == "Mal"
    assert vmal.sire == vlad
    assert vmal.creation_site == floor
    assert "Mal rises as a vampire!" in c(capsys)


def test_body_delete(body, place, vampire):
    floor = place("floor")
    vlad = vampire("Vlad", floor, None)
    mal = body("Mal", floor, vlad)

    mal.delete()
    assert not mal.installed
    assert mal.wait in o.clock.removed_callbacks
    assert mal.wait not in o.clock.callbacks


# Avatar
def test_avatar_init(place):
    bed = place("bed")
    talia = o.Avatar("Talia", bed)

    assert talia.name == "Talia"
    assert talia.location == bed
    assert bed.have_thing(talia)


def test_avatar_look():
    # TODO
    pass


def test_avatar_go(place, exit):
    o.clock.reset()

    bed = place("bed")
    floor = place("floor")
    table = place("table")
    exit1 = exit(bed, "down", floor)
    exit2 = exit(bed, "left", table)
    talia = o.Avatar("Talia", bed)

    t = o.current_time()
    assert talia.go("left")
    assert talia.location == table
    assert o.clock.time == t + 1

    # you can't go in a direction without an exit
    assert not talia.go("right")


def test_avatar_die(place, vampire, capsys):
    bed = place("bed")
    talia = o.Avatar("Talia", bed)
    vlad = vampire("Vlad", bed, None)

    talia.die(vlad)
    assert not talia.installed
    assert "Woe, I am slain!" in c(capsys)


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
    # TODO find a way to test the else clauses here


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
    # TODO
    pass


def test_run_clock():
    # TODO
    pass
