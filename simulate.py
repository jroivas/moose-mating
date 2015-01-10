#!/usr/bin/env python

import argparse
import moose
import moose_actions
import sys
import world

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Moose orgy')
    parser.add_argument('mooses', nargs='*', help='Original mooses')
    parser.add_argument('-x', '--width', default=500, type=int, help='World width')
    parser.add_argument('-y', '--height', default=500, type=int, help='World height')
    parser.add_argument('-t', '--ticks', default=10000, type=int, help='Ticks to run simulation')
    parser.add_argument('-s', '--seed', default=0, type=int, help='Seed of the world (default 0 == random)')
    parser.add_argument('-f', '--food', default=0, type=int, help='Food spawn rate')
    parser.add_argument('-v', '--verbose', action='store_true', help='Verbose')

    res = parser.parse_args()
    args = vars(res)

    area = (args['width'], args['height'])
    woods = world.World(moose_actions.MooseActions, moose.Moose, area=area, seed=args['seed'], verbose=args['verbose'])
    for moo in args['mooses']:
        woods.add_animal(moose.Moose(moo))

    print ('Initial population: %s' % [x.item for x in woods.animals])

    for x in xrange(args['ticks']):
        woods.tick()

    print ('Final population  : %s' % [x.item for x in woods.animals])

    alive = []
    dead = []
    for x in woods.animals:
        if x.item.alive:
            alive.append(x.item)
        else:
            dead.append(x.item)

    #print (len(alive), len(dead))
    print ('Alive: %s' % (alive))
    print ('Dead : %s' % (dead))
