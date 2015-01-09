import random

class Moose(object):
    def __init__(self, dna=''):
        self.viewarea = 100
        self.movingchange = 2
        self.stillchange = 2
        self.directionchange = 4
        self.maxenergy = 5
        self.jumpforce = 10
        self.energystill = 0.001
        self.energymoving = 0.002
        self.maxspeed = 4
        self.minspeed = 1
        self.searchingduration = 500
        self.shape = 0
        self.color = 0

        self.age = 0
        self.dna = dna

        self.randomizeName()
        self.randomize()
        self.importdna(dna)

        self.parents = []

    def tick(self):
        self.age += 1

    def die(self):
        self.alive = False

    def parseInt(self, val, base=2):
        return int(val, base)

    def importdna(self, dna):
        if len(dna) < 40:
            return

        self.dna = dna
        self.shape = dna[0:2]
        self.color = dna[2:4]

        self.viewarea = 70 + self.parseInt(dna[4:7]) * 15
        self.movingchange = 1 + self.parseInt(dna[7:10])
        self.stillchange = 1 + self.parseInt(dna[10:13])
        self.directionchange = self.parseInt(dna[13:17])
        self.maxenergy = 4 + self.parseInt(dna[17:20])
        self.energystill = 0.001 + self.parseInt(dna[20:23])/2000
        self.minspeed = 0.5 + self.parseInt(dna[27:30]) / 2
        self.maxspeed = self.minspeed + self.parseInt(dna[30:33]) / 1.5
        self.energymoving = self.energystill * (1 + self.maxspeed / 10) * (1 + self.parseInt(dna[24:28]) / 15)
        self.jumpforce = 7 + self.parseInt(dna[33:36])
        self.searchingduration = 300 + self.parseInt(dna[36:40]) * 100

    def randomBool(self):
        return bool(random.getrandbits(1))

    def combine(self, another):
        point = random.randint(0, 39)

        if self.randomBool():
            part1 = self.dna[point:]
            part2 = another.dna[:point]
        else:
            part1 = another.dna[point:]
            part2 = self.dna[:point]

        rawdna = part1 + part2
        child = Moose(self.mutate(rawdna))
        child.parents = (self, another)

        return child

    def mutate(self, rawdna):
        dna = ''
        for c in rawdna:
            if random.randint(1, 100) == 1:
                if c == '1':
                    dna += '0'
                else:
                    dna += '1'
            else:
                dna += c

        return dna

    def randomizeName(self):
        self.name = 'Moose-%s' % (random.randint(1, 99999))

    def randomize(self):
        self.importdna(''.join(['%s' % random.getrandbits(1) for x in xrange(40)]))

    def __str__(self):
        return self.dna

    def __repr__(self):
        return '%s %s' % (self.name, self.dna)

    def info(self):
        return """Name            : %s
Age             : %s
Shape           : %s
Color           : %s
View area       : %s
Moving change   : %s
Still change    : %s
Direction change: %s
Max energy      : %s
Jump force      : %s
Energy still    : %s
Energy moving   : %s
Max speed       : %s
Min speed       : %s
Search duration : %s
DNA             : %s
        """ % (
            self.name,
            self.age,
            self.shape,
            self.color,
            self.viewarea,
            self.movingchange,
            self.stillchange,
            self.directionchange,
            self.maxenergy,
            self.jumpforce,
            self.energystill,
            self.energymoving,
            self.maxspeed,
            self.minspeed,
            self.searchingduration,
            self.dna)
