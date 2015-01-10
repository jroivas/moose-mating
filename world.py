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
act.tick()
act.tick()
act.tick()

print ('----')

print (obj.info())
