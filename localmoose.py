#!/usr/bin/env python

import argparse
#import draw_world
import qworld
import moose
import moose_actions
import sys
import time
import world

from PyQt5 import QtCore
from PyQt5 import QtGui
from PyQt5 import QtWidgets
from PyQt5.Qt import Qt

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Moose orgy')
    parser.add_argument('mooses', nargs='*', help='Original mooses')
    parser.add_argument('-x', '--width', default=500, type=int, help='World width')
    parser.add_argument('-y', '--height', default=500, type=int, help='World height')
    parser.add_argument('-t', '--ticks', default=10000, type=int, help='Ticks to run simulation')
    parser.add_argument('-s', '--seed', default=0, type=int, help='Seed of the world (default 0 == random)')
    parser.add_argument('-m', '--max-mooses', default=0, type=int, help='Maximum number of mooses (0 == unlimited)')
    parser.add_argument('-f', '--food', default=0, type=int, help='Food spawn rate')
    parser.add_argument('--sleep', default=0.2, type=float, help='Sleep timer between ticks')
    parser.add_argument('--no-deep-food', action='store_false', default=True, help='Disable deep food search algorithm (faster)')
    parser.add_argument('--deep-mate', action='store_true', help='Enable deep mate search algorithm (slower)')
    parser.add_argument('-v', '--verbose', action='store_true', help='Verbose')
    parser.add_argument('--statsfile', help='Stats file name')

    res = parser.parse_args()
    args = vars(res)

    area = (args['width'], args['height'])
    woods = world.World(moose_actions.MooseActions, moose.Moose, area=area, seed=args['seed'], verbose=args['verbose'], deep_search_food=args['no_deep_food'], deep_search_mate=args['deep_mate'], food_spawn_rate=args['food'])
    woods.set_max_mooses(args['max_mooses'])
    worlds = [woods]

    for moo in args['mooses']:
        woods.add_animal(moose.Moose(moo))

    woods.set_sleep(args['sleep'])
    woods.start()

    app = QtWidgets.QApplication(sys.argv)
    win = qworld.QWorld(woods)
    win.show()

    app.exec_()

    woods.stop()
    woods.join()
