#!/usr/bin/env python

import moose
import sys

if len(sys.argv) > 1:
    obj = moose.Moose(sys.argv[1])
else:
    obj = moose.Moose()

print (obj.info())
