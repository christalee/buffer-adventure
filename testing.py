import unittest, doctest
from objtypes import *

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
    
class UtilsTest(unittest.TestCase):
    def setUp(self):
        self.location1 = Place("bed")
        self.location2 = Place("floor")
        self.thing1 = Thing("cat", self.location1)
        self.thing2 = Thing("rug", self.location2)
        self.objectlist = [self.location1, self.location2, self.thing1]
        
    def test_names(self):
        self.assertEqual(names(self.objectlist), [self.location1.name, self.location2.name, self.thing1.name])

    def test_objectfind(self):
        self.assertEqual(objectfind("cat", self.objectlist), self.thing1)
        self.assertEqual(objectfind("rug", self.objectlist), None)
        
if __name__ == '__main__':
    unittest.main()
    doctest.testmod()