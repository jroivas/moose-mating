import random

class Moose(object):
    def __init__(self, dna='', mutation_rate=100):
        self.alive = True
        self.age = 0
        self.dna = dna

        self.mutation_rate = mutation_rate

        self.randomizeName()
        self.randomize()
        self.importdna(dna)

        self.parents = (None, None)

    def tick(self):
        """
        >>> a = Moose()
        >>> a.age
        0
        >>> a.age
        0
        >>> a.tick()
        >>> a.age
        1
        >>> a.tick()
        >>> a.age
        2
        """
        self.age += 1

    def die(self):
        """
        >>> a = Moose()
        >>> a.alive
        True
        >>> a.die()
        >>> a.alive
        False
        """
        self.alive = False

    def parseInt(self, val, base=2):
        """
        >>> a = Moose()
        >>> a.parseInt('0')
        0
        >>> a.parseInt('1')
        1
        >>> a.parseInt('01')
        1
        >>> a.parseInt('10')
        2
        >>> a.parseInt('11')
        3
        >>> a.parseInt('011')
        3
        >>> a.parseInt('100')
        4
        >>> a.parseInt('101')
        5
        >>> a.parseInt('101', 10)
        101
        >>> a.parseInt('af', 16)
        175
        >>> a.parseInt('af', 10) # doctest: +ELLIPSIS
        Traceback (most recent call last):
        ...
        ValueError: invalid literal for int() with base 10: 'af'
        >>> a.parseInt('3', 2) # doctest: +ELLIPSIS
        Traceback (most recent call last):
        ...
        ValueError: invalid literal for int() with base 2: '3'
        """
        return int(val, base)

    def importdna(self, dna):
        """
        Example DNA:
        00|11|000|111|000|1111|000|111|0000|111|000|111|0000|
        sh co viw mov stl dirc men ens enmv mis mas jpf sedu

        Shape: 1 of 4 shapes
        Color: 1 of 4 color variations
        Viewarea: 70 + DNA Value (0-7) * 15
        Movingchange: 1 + DNA Value (0-7)
        Stillchange: 1 + DNA Value (0-7)
        Directionchange: DNA Value (0-15)
        Maxenergy: 4 + DNA Value (0-7)
        Energystill: 0.001 + DNA Value (0-7) / 2000
        Minspeed: 0.5 + DNA Value (0-7) / 2
        Maxspeed: Minspeed + DNA Value (0-7)/1.5
        Energymoving: Energystill * (1 + maxspeed/10) * (1 + DNA Value (0-15)/15)
        Jumpforce: 7 + DNA Value (0-7)
        Searchduration: 300 + DNA Value (0-15)*100

        >>> a = Moose()
        >>> a.importdna('0' * 40)
        >>> a.dna
        '0000000000000000000000000000000000000000'
        >>> a.viewarea
        70
        >>> a.movingchange
        1
        >>> a.minspeed
        0.5
        >>> a.maxspeed
        0.5
        >>> a.importdna('1' * 40)
        >>> a.dna
        '1111111111111111111111111111111111111111'
        >>> a.viewarea
        175
        >>> a.movingchange
        8
        >>> a.minspeed
        3.5
        >>> a.maxspeed # doctest: +ELLIPSIS
        8.1...
        >>> a.importdna('0011000111000111100011100001110001110000')
        >>> a.dna
        '0011000111000111100011100001110001110000'
        """
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
        self.energy = self.maxenergy
        self.energystill = 0.001 + self.parseInt(dna[20:23])/2000
        self.minspeed = 0.5 + self.parseInt(dna[27:30]) / 2
        self.maxspeed = self.minspeed + self.parseInt(dna[30:33]) / 1.5
        self.energymoving = self.energystill * (1 + self.maxspeed / 10) * (1 + self.parseInt(dna[24:28]) / 15)
        self.jumpforce = 7 + self.parseInt(dna[33:36])
        self.searchingduration = 300 + self.parseInt(dna[36:40]) * 100

    def randomBool(self):
        """
        """
        return bool(random.getrandbits(1))

    def combine_default(self, another):
        """
        >>> a = Moose('0' * 40)
        >>> b = Moose('1' * 40)
        >>> bak1 = random.getrandbits
        >>> bak2 = random.randint
        >>> random.getrandbits = lambda x: 0
        >>> random.randint = lambda x, y: (y - x) / 2
        >>> a.combine_default(b)
        '1111111111111111111110000000000000000000'
        >>> random.getrandbits = lambda x: 1
        >>> a.combine_default(b)
        '0000000000000000000001111111111111111111'
        >>> random.getrandbits = bak1
        >>> random.randint = bak2
        """
        point = random.randint(0, 39)

        if self.randomBool():
            part1 = self.dna[point:]
            part2 = another.dna[:point]
        else:
            part1 = another.dna[point:]
            part2 = self.dna[:point]

        rawdna = part1 + part2
        return rawdna

    def combine_range(self, another):
        """
        >>> a = Moose('0' * 40)
        >>> b = Moose('1' * 40)
        >>> bak1 = random.getrandbits
        >>> bak2 = random.randint
        >>> random.getrandbits = lambda x: 0
        >>> random.randint = lambda x, y: (y - x) / 2
        >>> a.combine_range(b)
        '1111111111111111111111111111110000000000'
        >>> random.getrandbits = lambda x: 1
        >>> a.combine_range(b)
        '0000000000000000000000000000001111111111'
        >>> random.getrandbits = bak1
        >>> random.randint = bak2
        """
        point = random.randint(10, 30)

        if self.randomBool():
            part1 = self.dna[point:]
            part2 = another.dna[:point]
        else:
            part1 = another.dna[point:]
            part2 = self.dna[:point]

        rawdna = part1 + part2
        return rawdna

    def combine_half(self, another):
        """
        >>> a = Moose('0' * 40)
        >>> b = Moose('1' * 40)
        >>> bak1 = random.getrandbits
        >>> random.getrandbits = lambda x: 0
        >>> a.combine_half(b)
        '0101010101010101010101010101010101010101'
        >>> random.getrandbits = lambda x: 1
        >>> a.combine_half(b)
        '1010101010101010101010101010101010101010'
        >>> random.getrandbits = bak1
        """
        num = 0
        if self.randomBool():
            num = 1


        rawdna = ''
        for i in range(40):
            if i % 2 == num:
                rawdna += self.dna[i]
            else:
                rawdna += another.dna[i]

        return rawdna

    def combine_random(self, another):
        """
        >>> a = Moose('0' * 40)
        >>> b = Moose('1' * 40)
        >>> bak1 = random.getrandbits
        >>> random.getrandbits = lambda x: 0
        >>> a.combine_random(b)
        '1111111111111111111111111111111111111111'
        >>> random.getrandbits = lambda x: 1
        >>> a.combine_random(b)
        '0000000000000000000000000000000000000000'
        >>> random.getrandbits = bak1
        """
        rawdna = ''
        for i in range(40):
            if self.randomBool():
                rawdna += self.dna[i]
            else:
                rawdna += another.dna[i]

        return rawdna

    def combine_xor(self, another):
        """
        >>> a = Moose('0' * 40)
        >>> b = Moose('1' * 40)
        >>> c = Moose('1010101010101010101010101010101010101010')
        >>> d = Moose('1111111111111111111111101010101010101010')
        >>> a.combine_xor(b)
        '1111111111111111111111111111111111111111'
        >>> c.combine_xor(d)
        '0101010101010101010101000000000000000000'
        """
        rawdna = ''

        for i in range(40):
            a = self.dna[i]
            b = another.dna[i]
            rawdna += '%s' % (int(a) ^ int(b))

        return rawdna

    def combine_and(self, another):
        """
        >>> a = Moose('0' * 40)
        >>> b = Moose('1' * 40)
        >>> c = Moose('1010101010101010101010101010101010101010')
        >>> d = Moose('1111111111111111111111101010101010101010')
        >>> a.combine_and(b)
        '0000000000000000000000000000000000000000'
        >>> c.combine_and(d)
        '1010101010101010101010101010101010101010'
        """
        rawdna = ''

        for i in range(40):
            a = self.dna[i]
            b = another.dna[i]
            rawdna += '%s' % (int(a) & int(b))

        return rawdna

    def combine(self, another, algorithm='default'):
        """
        >>> a = Moose('0' * 40)
        >>> b = Moose('1' * 40)
        >>> bak1 = random.getrandbits
        >>> bak2 = random.randint
        >>> random.getrandbits = lambda x: 0
        >>> random.randint = lambda x, y: (y - x) / 2
        >>> c = a.combine(b)
        >>> c.dna != b.dna
        True
        >>> c.dna != a.dna
        True
        >>> random.getrandbits = lambda x: 1
        >>> d = a.combine(b)
        >>> c.dna != d.dna
        True
        >>> c.dna.count('0') > 1
        True
        >>> c.dna.count('1') > 1
        True
        >>> random.getrandbits = bak1
        >>> random.randint = bak2
        """
        if algorithm == 'half':
            rawdna = self.combine_half(another)
        elif algorithm == 'random':
            rawdna = self.combine_random(another)
        elif algorithm == 'range':
            rawdna = self.combine_range(another)
        elif algorithm == 'xor':
            rawdna = self.combine_xor(another)
        elif algorithm == 'and':
            rawdna = self.combine_and(another)
        else:
            rawdna = self.combine_default(another)

        child = Moose(self.mutate(rawdna), self.mutation_rate)
        child.parents = (self, another)

        return child

    def mutate(self, rawdna):
        """
        >>> a = Moose('0' * 40)
        >>> rnd = random.randint
        >>> random.randint = lambda x, y: 1
        >>> dna = a.mutate(a.dna)
        >>> '1' in dna
        True
        >>> random.randint = lambda x, y: 0
        >>> dna = a.mutate(a.dna)
        >>> '1' in dna
        False
        >>> random.randint = rnd
        """
        dna = ''
        for c in rawdna:
            if random.randint(1, self.mutation_rate) == 1:
                if c == '1':
                    dna += '0'
                else:
                    dna += '1'
            else:
                dna += c

        return dna

    def randomizeName(self):
        """
        >>> Moose().name != Moose().name
        True
        >>> Moose().name != Moose().name
        True
        """
        self.name = 'Moose-%s' % (random.randint(1, 99999))

    def randomize(self):
        """
        >>> a = Moose()
        >>> b = Moose()
        >>> a.randomize()
        >>> b.randomize()
        >>> a.dna != b.dna
        True
        """
        self.importdna(''.join(['%s' % random.getrandbits(1) for x in xrange(40)]))

    def __str__(self):
        return self.dna

    def __repr__(self):
        return '%s %s' % (self.name, self.dna)

    def info(self):
        """
        >>> a = Moose('0' * 40)
        >>> b = Moose('1' * 40)
        >>> print a.info() # doctest: +ELLIPSIS
        Name            : Moose-...
        Age             : 0
        Alive           : True
        Shape           : 00
        Color           : 00
        View area       : 70
        Moving change   : 1
        Still change    : 1
        Direction change: 0
        Jump force      : 7
        Energy          : 4
        Max energy      : 4
        Energy still    : 0.001
        Energy moving   : 0.00105
        Max speed       : 0.5
        Min speed       : 0.5
        Search duration : 300
        DNA             : 0000000000000000000000000000000000000000
        >>> print b.info() # doctest: +ELLIPSIS
        Name            : Moose-...
        Age             : 0
        Alive           : True
        Shape           : 11
        Color           : 11
        View area       : 175
        Moving change   : 8
        Still change    : 8
        Direction change: 15
        Jump force      : 14
        Energy          : 11
        Max energy      : 11
        Energy still    : 0.001
        Energy moving   : 0.0036...
        Max speed       : 8.16...
        Min speed       : 3.5
        Search duration : 1800
        DNA             : 1111111111111111111111111111111111111111
        """
        return """Name            : %s
Age             : %s
Alive           : %s
Shape           : %s
Color           : %s
View area       : %s
Moving change   : %s
Still change    : %s
Direction change: %s
Jump force      : %s
Energy          : %s
Max energy      : %s
Energy still    : %s
Energy moving   : %s
Max speed       : %s
Min speed       : %s
Search duration : %s
DNA             : %s""" % (
            self.name,
            self.age,
            self.alive,
            self.shape,
            self.color,
            self.viewarea,
            self.movingchange,
            self.stillchange,
            self.directionchange,
            self.jumpforce,
            self.energy,
            self.maxenergy,
            self.energystill,
            self.energymoving,
            self.maxspeed,
            self.minspeed,
            self.searchingduration,
            self.dna)
