#!/usr/bin/env python

import moose
import sys
import moose_actions
import world

if __name__ == '__main__':
    area = (500, 500)
    woods = world.World(moose_actions.MooseActions, moose.Moose, area=area, seed=1, verbose=True)

    print [x.item for x in woods.animals]

    for x in xrange(20000):
        woods.tick()

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
