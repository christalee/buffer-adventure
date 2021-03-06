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


def test_clock_tick(place, thing, capsys):
    # TODO
    # bed = place("bed")
    # cat = thing("cat", bed)
    # o.clock.reset()
    #
    # o.clock.add_callback(cat.say("Meow!"))
    # o.clock.add_callback(bed.have_thing(cat))
    #
    # o.clock.tick()
    # assert o.clock.time == 1
    #
    # assert "Clock Tick" in c(capsys)
    # assert o.clock.removed_callbacks == []
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
    assert "Dave says: I lose dog" in c(capsys)

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


# Tool
def test_tool_init(tool, place):
    floor = place("floor")
    slide = tool("slide", floor, 3)

    assert slide.magic == 3


# Place
def test_place_init(place):
    bed = place("bed")

    assert bed.exits == []
    assert bed.name == 'bed'
    # TODO is this the right way to test the inheritance?
    assert isinstance(bed, o.Container)
    assert isinstance(bed, o.Named_Object)


def test_place_add_exit(place, exit, capsys):
    bed = place("bed")
    floor = place("floor")
    exit1 = exit(bed, "down", floor)
    exit2 = exit(bed, "down", floor)

    # TODO is this needed, since exit1 calls bed.add_exit?
    assert bed.exits == [exit1]
    assert "down->floor added at bed"

    # can't add_exit twice
    assert not bed.add_exit(exit2)
    assert "bed already has an exit to down->floor" in c(capsys)


# Hideout
# again, is this necessary?
def test_hideout_init(hideout):
    tomb = hideout("tomb")

    assert tomb.name == "tomb"


# Exit
def test_exit_init(place, exit, hideout, capsys):
    bed = place("bed")
    floor = place("floor")
    tomb = hideout("tomb")
    shaft = hideout("shaft")

    # Exit from Place to Place, no magic
    exit1 = exit(bed, "down", floor)
    assert exit1.origin == bed
    assert exit1.direction == 'down'
    assert exit1.destination == floor
    assert exit1.magic == 0
    assert exit1.name == 'down->floor'

    # TODO is this how I want to test success/failure for installation?
    # Exit from Place to Place, magic
    exit2 = exit(floor, "up", bed, 4)
    assert exit2

    # Exit from Hideout to Hideout, magic
    exit3 = exit(shaft, "down", tomb, 2)
    assert exit3

    # Exit from Place to Hideout, no magic - should fail
    exit4 = exit(bed, "down", tomb)
    assert "down->tomb must have some magic" in c(capsys)
    assert not exit4.installed

    # Exit from Place to Hideout, magic
    exit5 = exit(bed, "up", shaft, 4)
    assert exit5

    assert bed.exits == [exit1, exit5]
    assert floor.exits == [exit2]
    assert shaft.exits == [exit3]


# Person
def test_person_init(person, place):
    floor = place("floor")
    bob = person("Bob", floor)

    assert bob.health == 3
    assert bob.strength == 1
    assert bob.magic == 0
    assert not bob.weapon

    assert isinstance(bob, o.Mobile_Thing)
    assert isinstance(bob, o.Container)


def test_person_fit(person, place, capsys):
    floor = place("floor")
    bob = person("Bob", floor)

    bob.have_fit()
    assert "Yaaaah! I am upset!" in c(capsys)


def test_person_shirt(place, person, capsys):
    bed = place("bed")
    chris = person("Chris", bed)

    chris.shirt()
    assert c(capsys).split(": ")[-1].strip() in data.shirts


def test_person_people_around(person, place, exit):
    bed = place("bed")
    floor = place("floor")
    alice = person("Alice", bed)
    bob = person("Bob", floor)
    exit1 = exit(bed, "down", floor)

    assert alice.people_around() == []
    assert bob.people_around() == []

    alice.go('down')
    assert alice.people_around() == [bob]
    assert bob.people_around() == [alice]


def test_person_room_things(person, place, thing, mthing):
    bed = place("bed")
    cat = thing("cat", bed)
    blanket = thing("blanket", bed)
    dog = mthing("dog", bed)
    bob = person("Bob", bed)
    alice = person("Alice", bed)

    assert alice.room_things() == [cat, blanket, dog]

    # once a Thing has an owner, it shouldn't show up in room_things
    bob.take(dog.name)
    assert alice.room_things() == [cat, blanket]


def test_person_people_things(person, place, thing, mthing, capsys):
    floor = place("floor")
    dave = person("Dave", floor)
    bob = person("Bob", floor)
    dog = mthing("dog", floor)
    cat = mthing("cat", floor)
    blanket = thing("blanket", floor)

    # cat and blanket have no owner, so they shouldn't show up in people_things
    assert dave.take(dog.name)
    assert bob.people_things() == [dog]
    assert dave.people_things() == []
    assert "Bob says: Dave has dog" in c(capsys)


def test_person_take(person, place, thing, mthing, tool, capsys):
    bed = place("bed")
    floor = place("floor")
    dave = person("Dave", floor)
    bob = person("Bob", floor)
    rug = thing("rug", floor)
    dog = mthing("dog", floor)
    pillow = mthing("pillow", bed)
    slide = tool("slide", floor, 3)

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

    # if you pick up a Tool, it increases your magic
    assert bob.take(slide.name)
    assert bob.magic == slide.magic


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
    assert floor.have_thing(dog)

    # TODO check location, have_thing of mthings before and after take and drop

    # you can't drop a thing you don't have
    assert not dave.drop(dog.name)
    assert "I don't have that item!" in c(capsys)

    # drop your weapon, rebel scum!
    assert dave.take(relic.name)
    dave.equip(relic.name)
    assert dave.drop(relic.name)
    assert not dave.weapon


def test_person_equip(person, place, weapon, mthing, capsys):
    floor = place("floor")
    dave = person("Dave", floor)
    chair = weapon("chair", floor, 2)
    dog = mthing("dog", floor)

    assert dave.take(chair.name)
    dave.equip(chair.name)
    assert dave.weapon == chair
    assert "chair equipped!" in c(capsys)

    # can't equip Things that aren't Weapons
    assert dave.take(dog.name)
    dave.equip(dog.name)
    assert "You can only equip weapons, sorry." in c(capsys)


def test_person_go(person, place, exit, mthing, capsys):
    bed = place("bed")
    floor = place("floor")
    table = place("table")
    alice = person("Alice", bed)
    dog = mthing("dog", bed)
    exit1 = exit(bed, "down", floor)
    exit2 = exit(bed, "left", table)
    exit3 = exit(table, "right", bed)
    exit4 = exit(floor, "up", bed)

    assert alice.take(dog.name)
    assert alice.go("down")
    assert alice.location == floor
    assert floor.have_thing(alice)
    assert not bed.have_thing(alice)

    # and your little dog, too!
    assert dog.location == floor
    assert floor.have_thing(dog)
    assert not bed.have_thing(dog)

    # without a direction given, wander
    assert alice.go("up")
    assert alice.go()
    assert alice.location in [floor, table]

    # if there isn't an exit, you can't go that way
    assert not alice.go("north")
    assert "No exit in north direction" in c(capsys)


def test_person_go_magic(person, place, exit, capsys):
    bed = place("bed")
    floor = place("floor")
    alice = person("Alice", floor)
    jack = o.Hacker(floor)
    exit = exit(floor, "up", bed, 3)

    # Alice can't use exits that require magic
    alice.go('up')
    assert alice.location == floor
    assert "Alice is insufficiently clueful" in c(capsys)

    # but Jack can
    jack.go('up')
    assert jack.location == bed
    assert "jack-florey moves from floor to bed" in c(capsys)


def test_person_change_location(person, place, capsys):
    bed = place("bed")
    floor = place("floor")
    alice = person("Alice", bed)
    dave = person("Dave", floor)
    bob = person("Bob", floor)

    alice.change_location(floor)
    assert "Hi Dave, Bob" in c(capsys)


def test_person_suffer(person, place, capsys):
    floor = place("floor")
    dave = person("Dave", floor)
    bob = person("Bob", floor)

    d_health = dave.health
    dave.suffer(2, bob)
    assert dave.health == d_health - 2 + dave.strength
    assert "Ouch!" in c(capsys)

    dave.suffer(5, bob)
    assert not dave.installed
    assert "body of Dave" in u.names(floor.things)


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
    d_strength = dave.strength
    dave.attack('Bob')
    assert "Dave punches Bob!" in c(capsys)
    assert bob.health < 3
    assert dave.strength == d_strength + 1

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


# Autonomous_Person
def test_autop_init(autop, place):
    floor = place("floor")
    chris = autop("Chris", floor)

    assert chris.activity in range(1, 4)
    assert chris.miserly in range(1, 4)
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
    jack = o.Hacker(bed)
    liz = o.Hacker(floor)
    jessie = o.Hacker(table)

    chris.miserly = 1
    chris.move_and_take()
    assert len(chris.things) > 0
    assert chris.magic > 0
    assert "I'm done moving for now" in c(capsys)


def test_autop_take(autop, mthing, place, capsys):
    floor = place("floor")
    chris = autop("Chris", floor)
    dog = mthing("dog", floor)

    assert chris.take()
    assert chris.things == [dog]

    # can't take something that isn't there
    assert not chris.take("cat")
    assert "Whoops, there's nothing here to take." in c(capsys)

    # seriously, there's nothing to take
    assert not chris.take()


def test_autop_hack(autop, place, capsys):
    floor = place("floor")
    bed = place("bed")
    chris = autop("Chris", floor)
    alice = autop("Alice", bed)
    jack = o.Hacker(floor)

    chris.hack()
    assert chris.magic > 0
    assert "jack-florey is wearing a shirt" in c(capsys)

    # poor Alice, there's no one to catch a clue from
    alice.hack()
    assert alice.magic == 0


def test_autop_die(autop, place, person, capsys):
    floor = place("floor")
    chris = autop("Chris", floor)
    bob = person("Bob", floor)

    chris.die(bob)
    assert chris.move_and_take not in o.clock.callbacks
    assert "I suddenly feel very faint" in c(capsys)


# Oracle
def test_oracle_init(place):
    floor = place("floor")
    nostradamus = o.Oracle(floor)

    assert nostradamus.name == "nostradamus"


def test_oracle_move_and_take(place, capsys):
    floor = place("floor")
    nostradamus = o.Oracle(floor)

    nostradamus.move_and_take()
    # TODO fix this ugh
    assert not set(data.sayings).isdisjoint(set(c(capsys).splitlines()))


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
    assert slayer.activity in range(5, 11)
    assert slayer.health in range(5, 11)
    assert slayer.magic in range(1, 6)


def test_slayer_slay(place, vampire, capsys):
    floor = place("floor")
    slayer = o.Slayer(floor)
    vlad = vampire("Vlad", floor, None)

    slayer.slay()
    assert vlad.health < 10

    # if there's no Vampires to slay, do nothing
    vlad.die(slayer)
    assert not slayer.slay()
    assert "There's no one here to slay!" in c(capsys)


def test_slayer_take(holy, place, autop, mthing):
    floor = place("floor")
    slayer = o.Slayer(floor)
    chris = autop("Chris", floor)
    grail = holy('grail', floor)
    relic = holy("relic", floor)
    dog = mthing("dog", floor)
    pillow = mthing("pillow", floor)

    chris.take(grail.name)
    # preferentially take a Holy_Object first
    slayer.take()
    assert grail in slayer.things or relic in slayer.things

    # then proceed with usual random take()
    slayer.take()
    # TODO is this the best way?
    assert len(slayer.things) == 2


def test_slayer_suffer(place, vampire, person):
    floor = place("floor")
    slayer = o.Slayer(floor)
    vlad = vampire("Vlad", floor, None)
    chris = person("Chris", floor)

    # Slayers only take 1 damage from Vampires
    s_health = slayer.health
    slayer.suffer(5, vlad)
    assert slayer.health == s_health - 1

    # but they suffer normally from other attacks
    slayer.suffer(3, chris)
    assert slayer.health == s_health - 3


def test_slayer_die(place, vampire, capsys):
    floor = place("floor")
    slayer = o.Slayer(floor)
    vlad = vampire("Vlad", floor, None)

    slayer.die(vlad)
    assert "Time for another ride on the wheel of dharma..." in c(capsys)
    # TODO check that Slayer has respawned


# Hacker
def test_hacker_init(place):
    floor = place("floor")
    jack = o.Hacker(floor)

    assert jack.name == 'jack-florey'
    assert jack.magic == 10


def test_hacker_hack(place, hideout, capsys):
    floor = place("floor")
    tomb = hideout("tomb")
    jack = o.Hacker(floor)
    liz = o.Hacker(tomb)

    jack.hack()
    assert "sign-in: jack-florey" not in u.names(floor.things)

    liz.hack()
    assert "sign-in: jack-florey" in u.names(tomb.things)
    assert "I'm going to sign in" in c(capsys)


# Vampire
def test_vampire_init(vampire, place, capsys):
    floor = place("floor")
    vlad = vampire("Vlad", floor, None)

    assert vlad.strength == 10
    assert not vlad.sire
    assert vlad.move_and_take in o.clock.callbacks

    lestat = vampire("Lestat", floor, vlad)
    assert lestat.strength == 2
    assert vlad.strength == 11
    assert lestat.sire == vlad
    assert lestat.move_and_take in o.clock.callbacks
    assert "Vlad got stronger" in c(capsys)


def test_vampire_move_and_take(vampire):
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


def test_vampire_die(vampire, place, person, capsys):
    floor = place("floor")
    vlad = vampire("Vlad", floor, None)
    chris = person("Chris", floor)

    vlad.die(chris)
    assert vlad.move_and_take not in o.clock.callbacks
    assert "Vlad turns to dust!" in c(capsys)
    assert not vlad.installed


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


# Utilities
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
    cat = mthing("cat", bed)
    pillow = thing("pillow", bed)

    assert u.find_all(bed, o.Mobile_Thing) == [cat]


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
