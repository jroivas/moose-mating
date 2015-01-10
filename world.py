#!/usr/bin/env python

import moose
import sys
import moose_actions

if len(sys.argv) > 1:
    obj = moose.Moose(sys.argv[1])
else:
    obj = moose.Moose()

print (obj.info())

act = moose_actions.MooseActions(obj)
while obj.alive and obj.age < 10000:
    act.tick()

print ('----')

print (obj.info())

print ('----')

print ('End position, x: %s, y: %s' % (act.path[-1]))
