import random
from typing import List, Optional, Union

from objects import *


def names(objectlist: List[Named_Object]) -> List[str]:
    """Given a list of objects, return a list of their names."""
    namelist = [x.name for x in objectlist]
    return namelist


# renamed this from objectfind to be more specific
def thingfind(thingname: str, thinglist: List[Thing]) -> Optional[Thing]:
    """Given a name and a list of Things, return the Thing with that name."""
    for each in thinglist:
        if each.name == thingname:
            return each
    return None


# TODO rewrite using filter; figure out the type of type
def find_all(location: Place, type: type) -> List[Thing]:
    all = [x for x in location.things if isinstance(x, type)]
    return all


def find_exit(exitlist: List[Exit], dir: str) -> Union[bool, Exit]:
    # TODO Add better handling for returning more than one exit here.
    # Consider changing exits to be named by destination rather than direction??
    """Given a list of exits, find one in the desired direction."""
    if len(exitlist) > 0:
        exit = [each for each in exitlist if each.direction == dir]
        if len(exit) == 1:
            return exit[0]
        elif len(exit) == 0:
            print("No exits found in that direction.")
            return True
        else:
            print("Exits in that direction lead to: ")
            for each in exit:
                print(each.destination.name)
            print("Please enter the index of the exit you want to use.")
            index = eval(input())
            return exit[index]
    else:
        print("No exit.")
        return True


def random_exit(place: Place) -> Exit:
    return random.choice(place.exits)


# TODO get clock object from world?
def current_time():
    global clock
    return clock.time


def run_clock(x):
    global clock
    while x > 0:
        clock.tick()
        x -= 1
# TODO consider adding remove_duplicates here?
