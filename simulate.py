#!/usr/bin/env python

import moose
import sys
import moose_actions
import world

woods = world.World(moose.Moose, 1)

acts = []
for obj in woods.animals:
    acts.append(moose_actions.MooseActions(obj, woods))

for x in xrange(5000):
    for act in acts:
        act.tick()

print woods.animals

alive = 0
dead = 0
for x in woods.animals:
    if x.alive:
        alive += 1
    else:
        dead += 1

print (alive, dead)
