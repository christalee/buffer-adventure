import pytest

import objects as o


@pytest.fixture
def named_object():
    def _named_object(name):
        return o.Named_Object(name)

    return _named_object


@pytest.fixture
def container():
    return o.Container()


@pytest.fixture
def clock():
    return o.Clock()


@pytest.fixture
def thing():
    def _thing(name, place):
        return o.Thing(name, place)

    return _thing


@pytest.fixture
def mthing():
    def _mthing(name, place):
        return o.Mobile_Thing(name, place)

    return _mthing


@pytest.fixture
def holy():
    def _holy(name, place):
        return o.Holy_Object(name, place)

    return _holy


@pytest.fixture
def place():
    def _place(name):
        return o.Place(name)

    return _place


@pytest.fixture
def exit():
    def _exit(origin, name, destination):
        return o.Exit(origin, name, destination)

    return _exit


@pytest.fixture
def person():
    def _person(name, place):
        return o.Person(name, place)

    return _person


@pytest.fixture
def objects(place, thing, mthing, holy, person, exit):
    no = named_object("test object")
    bed = place("bed")
    floor = place("floor")
    table = place("table")
    cat = thing("cat", bed)
    rug = thing("rug", floor)
    blanket = thing("blanket", bed)
    box = thing("box", floor)
    dog = mthing("dog", floor)
    grail = holy('grail', table)
    alice = person("Alice", bed)
    bob = person("Bob", floor)
    exit1 = exit(bed, "down", floor)
    exit2 = exit(bed, "left", table)

    return no, bed, floor, table, cat, dog, rug, blanket, box, grail, alice, bob, exit1, exit2
