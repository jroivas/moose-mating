#!/usr/bin/env python

import argparse
import moose
import random
import sys


def gen(m1, m2, maxchild=3, algorithm=''):
    child = []
    print ('Mating: %s and %s' % (m1.name, m2.name))
    for x in range(random.randint(1, maxchild + 1)):
        child.append(m1.combine(m2, algorithm))

    return child

def maters(mooses):
    if len(mooses) <= 1:
        return None

    a = random.choice(mooses)
    while True:
        b = random.choice(mooses)
        if a != b:
            return (a, b)

def mate_two(mooses, maxchild=3, algorithm=''):
    res = maters(mooses)
    if res is None:
        return []
    return gen(res[0], res[1], maxchild=maxchild, algorithm=algorithm)

def orgy(mooses, pairs, maxchild=3, algorithm=''):
    res = []
    for x in range(int(pairs)):
        res += mate_two(mooses, maxchild=maxchild, algorithm=algorithm)
    return mooses + res

def tick(mooses):
    for m in mooses:
        m.tick()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Moose orgy')
    parser.add_argument('mooses', nargs='*', help='Original mooses')
    parser.add_argument('-r', '--rate', default=100, type=int, help='Mutation rate')
    parser.add_argument('-g', '--generations', default=10, type=int, help='Number of iterations (min 1)')
    parser.add_argument('-c', '--max-child', default=3, type=int, help='Maximum number of children')
    parser.add_argument('-p', '--pairs', default=1.5, type=float, help='Orgy pair divide factor, can\'t be 0')
    parser.add_argument('-m', '--mutation', default='default', help='Mutation algorithm')

    res = parser.parse_args()
    args = vars(res)

    if args['pairs'] == 0 or args['generations'] < 1:
        parser.print_help()
        sys.exit(1)

    mooses = []
    for dna in args['mooses']:
        mooses.append(moose.Moose(dna, args['rate']))

    if len(mooses) < 2:
        mooses.append(moose.Moose('0' * 40, args['rate']))
    if len(mooses) < 2:
        mooses.append(moose.Moose('1' * 40, args['rate']))

    tick(mooses)

    cnt = 0
    maxcnt = args['generations']
    while cnt < maxcnt:
        mooses = orgy(mooses, max(1, cnt / args['pairs']), maxchild=args['max_child'], algorithm=args['mutation'])
        print ('gen %s: %s' % (cnt + 1, mooses))
        tick(mooses)
        cnt += 1

    for moo in mooses:
        print '%s parents: %s' % (moo, moo.parents)
