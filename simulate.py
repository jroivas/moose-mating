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
    parser.add_argument('--no-deep-food', action='store_false', default=True, help='Disable deep food search algorithm (faster)')
    parser.add_argument('--deep-mate', action='store_true', help='Enable deep mate search algorithm (slower)')
    parser.add_argument('-v', '--verbose', action='store_true', help='Verbose')
    parser.add_argument('--stats', action='store_true', help='Show periodical stats')

    res = parser.parse_args()
    args = vars(res)

    area = (args['width'], args['height'])
    woods = world.World(moose_actions.MooseActions, moose.Moose, area=area, seed=args['seed'], verbose=args['verbose'], deep_search_food=args['no_deep_food'], deep_search_mate=args['deep_mate'], food_spawn_rate=args['food'])
    print woods
    for moo in args['mooses']:
        woods.add_animal(moose.Moose(moo))

    print ('Initial population: %s' % [x.item for x in woods.animals])

    for x in xrange(args['ticks']):
        if args['stats'] and woods.age % 5000 == 0:
            print ('food  : %s' % (len(woods.food)))
            print ('animals: %s' % (len(woods.animals)))
        woods.tick()
    sys.stdout.write('\n')
    sys.stdout.flush()

    print ('Alive: %s' % [x.item for x in woods.animals])
    print ('Dead : %s' % [x.item for x in woods.dead_animals])
