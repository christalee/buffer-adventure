import random
from typing import TYPE_CHECKING, List, Optional, Sequence, Union

if TYPE_CHECKING:
    from objects import *


def names(objectlist: Sequence['Named_Object']) -> List[str]:
    """Given a list of objects, return a list of their names."""
    return [x.name for x in objectlist]


def thingfind(name: str, thinglist: Sequence['Thing']) -> Optional['Thing']:
    # renamed this from objectfind to be more specific
    # TODO should this check for duplicates?
    """Given a name and a list of Things, return the first Thing with that name."""
    for t in thinglist:
        if t.name == name:
            return t
    return None


def find_all(location: 'Container', type: type) -> List['Thing']:
    """Given a Place, return a list of all objects of a given type in that Place"""
    return list(filter(lambda x: isinstance(x, type), location.things))


def find_exit(exitlist: List['Exit'], dir: str) -> Optional['Exit']:
    # TODO Add better handling for returning more than one exit here.
    """Given a list of exits, find one in the desired direction."""
    if len(exitlist) > 0:
        exit = [e for e in exitlist if dir in e.direction]
        if len(exit) == 1:
            return exit[0]
        elif len(exit) == 0:
            print("No exits found in that direction.")
            return None
        else:
            print("Exits in that direction lead to: ")
            for e in exit:
                print(e.destination.name)
            index = input("Please enter the index of the exit you want to use: ")
            return exit[int(index)]
    else:
        print("No exit.")
        return None


def random_exit(place: 'Place') -> Optional['Exit']:
    exit = random.choice(place.exits) if place.exits else None
    return exit

# TODO consider adding remove_duplicates here?
