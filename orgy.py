#!/usr/bin/env python

import moose
import random
import time


def gen(m1, m2, maxchild=3):
    child = []
    print ('Mating: %s and %s' % (m1.name, m2.name))
    for x in range(random.randint(1, maxchild + 1)):
        child.append(m1.combine(m2))

    return child

def maters(mooses):
    if len(mooses) <= 1:
        return None

    a = random.choice(mooses)
    while True:
        b = random.choice(mooses)
        if a != b:
            return (a, b)

def mate_two(mooses):
    res = maters(mooses)
    if res is None:
        return []
    return gen(res[0], res[1])

def orgy(mooses, pairs):
    res = []
    for x in range(int(pairs)):
        res += mate_two(mooses)
    return mooses + res

def tick(mooses):
    for m in mooses:
        m.tick()

if __name__ == '__main__':
    zero = moose.Moose('0' * 40)
    one  = moose.Moose('1' * 40)

    # Parent mooses
    mooses = [zero, one]
    tick(mooses)

    # First generation of moose
    mooses += gen(zero, one)
    tick(mooses)

    cnt = 0
    maxcnt = 10
    while cnt < maxcnt:
        mooses = orgy(mooses, max(1, cnt/1.5))
        print ('gen %s: %s' % (cnt + 1, mooses))
        tick(mooses)
        cnt += 1
