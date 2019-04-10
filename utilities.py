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


def find_all(location: 'Place', type: type) -> List['Thing']:
    # TODO rewrite using filter; figure out the type of type
    """Given a Place, return a list of all objects of a given type in that Place"""
    return [x for x in location.things if isinstance(x, type)]


def find_exit(exitlist: List['Exit'], dir: str) -> Union[bool, 'Exit']:
    # TODO Add better handling for returning more than one exit here.
    # Consider changing exits to be named by destination rather than direction??
    """Given a list of exits, find one in the desired direction."""
    if len(exitlist) > 0:
        exit = [e for e in exitlist if e.direction == dir]
        if len(exit) == 1:
            return exit[0]
        elif len(exit) == 0:
            print("No exits found in that direction.")
            return False
        else:
            print("Exits in that direction lead to: ")
            for e in exit:
                print(e.destination.name)
            index = input("Please enter the index of the exit you want to use: ")
            return exit[int(index)]
    else:
        print("No exit.")
        return False


def random_exit(place: 'Place') -> 'Exit':
    return random.choice(place.exits)

# TODO consider adding remove_duplicates here?
