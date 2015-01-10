#!/usr/bin/env python

import moose
import sys
import moose_actions
import world

area = (500, 500)
woods = world.World(moose.Moose, area=area, seed=1)

acts = []
for obj in woods.animals:
    acts.append(moose_actions.MooseActions(obj, woods, area=area))

for x in xrange(10000):
    for act in acts:
        act.tick()

print woods.animals

alive = []
dead = []
for x in woods.animals:
    if x.alive:
        alive.append(x)
    else:
        dead.append(x)

print (len(alive), len(dead))
print ('Alive: %s' % (alive))
print ('Dead : %s' % (dead))
