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
def weapon():
    def _weapon(name, place, damage):
        return o.Weapon(name, place, damage)
    return _weapon


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
def autop():
    def _autop(name, place):
        return o.Autonomous_Person(name, place)

    return _autop


@pytest.fixture
def vampire():
    def _vampire(name, place, sire):
        return o.Vampire(name, place, sire)

    return _vampire


@pytest.fixture
def body():
    def _body(name, place, perp):
        return o.Body(name, place, perp)

    return _body
