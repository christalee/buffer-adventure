from setup import *

w = create_world()
s = w["10-250"]
e = Exit(s, "east", w["building-13"])
t = Mobile_Thing("Trotsky", s)

print s.name
print s.installed
s.install()
print s.installed
s.delete()
print s.installed

print names(s.things)
t.install()
print names(s.things)
t.delete()
print names(s.things)

print t.creation_site.name
print t.location.name
print names(w["34-301"].things)
t.change_location(w["34-301"])
print t.location.name
print names(w["34-301"].things)

t.enter_room()
t.leave_room()
t.emit("suddenly, a shot rang out!")

print names(s.exits)
e.install()
print names(s.exits)
e.install()
print random_exit(s)
print random_exit(s)
print s.exit_towards('east').destination.name

print e.origin.name
print e.direction
print e.destination.name
