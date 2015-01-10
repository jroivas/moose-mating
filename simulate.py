#!/usr/bin/env python

import moose
import sys
import moose_actions
import world

area = (500, 500)
woods = world.World(moose_actions.MooseActions, moose.Moose, area=area, seed=1)

for x in xrange(100000):
    for act in woods.animals:
        act.tick()

print [x.item for x in woods.animals]

alive = []
dead = []
for x in woods.animals:
    if x.item.alive:
        alive.append(x.item)
    else:
        dead.append(x.item)

print (len(alive), len(dead))
print ('Alive: %s' % (alive))
print ('Dead : %s' % (dead))
