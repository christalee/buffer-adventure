from __future__ import absolute_import
from builtins import object
import unittest, doctest
from .objtypes import *

class TestScreen(object):
    def __init__(self):
        self.buffer = []
    
    def tell_room(self, location, text):
        self.buffer.append([location, text])
    
    def lastsaid(self):
        return self.buffer[0]

#w = create_world()
#s = w["10-250"]
#e = Exit(s, "east", w["building-13"])
#t = Mobile_Thing("Trotsky", s)
#
#print s.name
#print s.installed
#s.install()
#print s.installed
#s.delete()
#print s.installed
#
#print names(s.things)
#t.install()
#print names(s.things)
#t.delete()
#print names(s.things)
#
#print t.creation_site.name
#print t.location.name
#print names(w["34-301"].things)
#t.change_location(w["34-301"])
#print t.location.name
#print names(w["34-301"].things)
#
#t.enter_room()
#t.leave_room()
#t.emit("suddenly, a shot rang out!")
#
#print names(s.exits)
#e.install()
#print names(s.exits)
#e.install()
#print random_exit(s)
#print random_exit(s)
#print s.exit_towards('east').destination.name
#
#print e.origin.name
#print e.direction
#print e.destination.name


class Named_ObjectTest(unittest.TestCase):
    def setUp(self):
        self.named_object = Named_Object("Test object")
        
    def test_object_name(self):
        self.assertEqual(self.named_object.name, "Test object")
    
    def test_object_install_init(self):
        self.assertFalse(self.named_object.isInstalled)
    
    def test_object_installation(self):
        self.named_object.install()
        self.assertTrue(self.named_object.isInstalled)
    
    def test_object_deletion(self):
        self.named_object.install()
        self.named_object.delete()
        self.assertFalse(self.named_object.isInstalled)

class ContainerTest(unittest.TestCase):
    def setUp(self):
        self.container = Container()
        self.location1 = Place("bed")
        self.location2 = Place("floor")
        self.thing1 = Thing("cat", self.location1)
        self.thing2 = Thing("rug", self.location2)
        self.thing3 = Thing("blanket", self.location1)
        self.thing4 = Thing("box", self.location2)
    
    def test_container_things_init(self):
        self.assertEqual(self.container.things, [])
    
    def test_container_have_things(self):
        self.container.things = [self.thing1, self.thing2, self.thing3]
        self.assertTrue(self.container.have_thing(self.thing2))
        self.assertFalse(self.container.have_thing(self.thing4))
    
    def test_container_add_thing(self):
        self.container.add_thing(self.thing1)
        self.assertTrue(self.container.have_thing(self.thing1))
        self.container.add_thing(self.thing1)
        self.assertEqual(self.container.things, [self.thing1])
    
    def test_container_delete_thing(self):
        self.container.add_thing(self.thing1)
        self.container.add_thing(self.thing2)
        self.container.delete_thing(self.thing1)
        self.assertEqual(self.container.things, [self.thing2])
        
class ThingTest(unittest.TestCase):
    def setUp(self):
        self.location = Place("bed")
        self.thing = Thing("cat", self.location)
    
    def test_thing_location_init(self):
        self.assertEqual(self.thing.location, self.location)
    
    def test_thing_installation(self):
        self.thing.install()
        self.assertTrue(self.thing.isInstalled)
        self.assertTrue(self.location.have_thing(self.thing))
        
    def test_thing_deletion(self):
        self.thing.install()
        self.thing.delete()
        self.assertFalse(self.thing.isInstalled)
        self.assertFalse(self.location.have_thing(self.thing))
    
    #def test_thing_emit(self):
        #find something to write here that isn't ridiculous

class Mobile_ThingTest(unittest.TestCase):
    def setUp(self):
        self.location1 = Place("outside")
        self.location2 = Place("inside")
        self.mthing = Mobile_Thing("dog", self.location1)
    
    def test_mthing_creation_site(self):
        self.assertEqual(self.mthing.creation_site, self.location1)
    
    def test_mthing_change_location(self):
        self.mthing.install()
        self.assertEqual(self.mthing.location, self.location1)
        self.assertTrue(self.location1.have_thing(self.mthing))
        
        self.mthing.change_location(self.location2)
        self.assertFalse(self.location1.have_thing(self.mthing))
        self.assertEqual(self.mthing.location, self.location2)
        self.assertTrue(self.location2.have_thing(self.mthing))
        
    def test_mthing_enter_room(self):
        self.assertTrue(self.mthing.enter_room())
    
    def test_mthing_leave_room(self):
        self.assertTrue(self.mthing.leave_room())
    
class PlaceTest(unittest.TestCase):
    def setUp(self):
        self.location1 = Place("outside")
        self.location2 = Place("inside")
        self.exit = Exit(self.location1, "north", self.location2)
    
    def test_place_exits_init(self):
        self.assertEqual(self.location1.exits, [])
    
    def test_place_exit_towards(self):
        self.location1.add_exit(self.exit)
        self.assertEqual(self.location1.exit_towards("north"), self.exit)
    
    def test_place_add_exit(self):
        self.location1.add_exit(self.exit)
        self.assertEqual(self.location1.exits, [self.exit])
        #find some way to test the else case

class ExitTest(unittest.TestCase):
    def setUp(self):
        self.location1 = Place("outside")
        self.location2 = Place("inside")
        self.exit = Exit(self.location1, "north", self.location2)
        self.user = Person("Alice", self.location1)
    
    def test_exit_inits(self):
        self.assertEqual(self.exit.origin, self.location1)
        self.assertEqual(self.exit.direction, "north")
        self.assertEqual(self.exit.destination, self.location2)
    
    def test_exit_install(self):
        self.exit.install()
        self.assertEqual(self.location1.exits, [self.exit])
    
    def test_exit_use(self):
        #this method nearly entirely calls methods from the Person class, so I'm not sure it makes sense to test it here??
        
        self.exit.install()
        self.user.install()
        self.assertEqual(self.user.location, self.location1)
        self.assertTrue(self.location1.have_thing(self.user))
        self.assertFalse(self.location2.have_thing(self.user))
        
        self.exit.use(self.user)
        self.assertEqual(self.user.location, self.location2)
        self.assertFalse(self.location1.have_thing(self.user))
        self.assertTrue(self.location2.have_thing(self.user))
    
class PersonTest(unittest.TestCase):
    def setUp(self):
        global screen
        self.location = Place("New York")
        #self.location2 = Place("Toronto")
        self.person1 = Person("Alice", self.location)
        self.person2 = Person("Bob", self.location)
        self.thing1 = Thing("bed", self.location)
        self.thing2 = Mobile_Thing("Jones", self.location)
        self.thing3 = Mobile_Thing("Marx", self.location)
        self.person1.install()
        self.person2.install()
        self.thing1.install()
        self.thing2.install()
        self.thing3.install()
        screen = TestScreen()
    
    def test_inits(self):
        self.assertEqual(self.person.health, 3)
        self.assertEqual(self.person.strength, 1)
        self.assertEqual(self.person.name, "Alice")
        self.assertEqual(self.person.creation_site, self.location)
    
    def test_say(self):
        self.person.say("This is only a test.")
        self.assertEqual(screen.lastsaid, [self.person.location, "At New York Alice says: This is only a test."])
    
    def test_have_fit(self):
        self.person.have_fit()
        self.assertEqual(screen.lastsaid, [self.person.location, "At New York Alice says: Yaaaah! I am upset!"])
    
    def test_people_around(self):
        self.assertEqual(self.person1.people_around(), [self.person2])
    
    def test_things_around(self):
        self.assertEqual(set(self.person1.things_around()), set([self.thing1, self.thing2, self.thing3]))
    
    def test_peek_around(self):
        self.person1.take(self.thing2)
        self.assertEqual(self.person2.peek_around(), [self.thing2.name])
    
    def test_take(self):
        self.person1.take(self.thing2)
        ###assertEqual(self.thing2.location, self.person1)
    
    

class UtilsTest(unittest.TestCase):
    def setUp(self):
        self.location1 = Place("bed")
        self.location2 = Place("floor")
        self.thing1 = Thing("cat", self.location1)
        self.thing2 = Thing("rug", self.location2)
        self.objectlist = [self.location1, self.location2, self.thing1]
        self.exit1 = Exit(self.location1, "north", self.location2)
        self.exit2 = Exit(self.location2, "south", self.location1)
        self.exitlist = [self.exit1, self.exit2]
        
    def test_names(self):
        self.assertEqual(names(self.objectlist), [self.location1.name, self.location2.name, self.thing1.name])

    def test_objectfind(self):
        self.assertEqual(objectfind("cat", self.objectlist), self.thing1)
        self.assertEqual(objectfind("rug", self.objectlist), None)
    
    def test_find_exit(self):
        self.assertEqual(find_exit(self.exitlist, "south"), self.exit2)
        #find a way to test the else clauses here
    
    def test_random_exit(self):
        self.exit1.install()
        self.exit2.install()
        self.assertTrue(random_exit(location1) in self.exitlist)
        
if __name__ == '__main__':
    unittest.main()
    #doctest.testmod()