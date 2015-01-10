import random
import time

class Food(object):
    def __init__(self):
        self.generate()

    def generate(self):
        self.size = random.randint(1, 10)
        self.value = random.randint(1, 10)

class World(object):
    def __init__(self, animal_base, seed=0):
        self.food = []
        self.animals = []
        self.animal_base = animal_base
        self.seed = seed
        self.generate()

    def generate(self):
        if self.seed == 0:
            return

        if self.seed > 0:
            random.seed(self.seed)

        cnt_food = random.randint(10, 1000)
        cnt_animals = random.randint(1, 10)

        if self.seed > 0:
            # Prevent animals and food to be same
            random.seed(int(time.time() * 1000000))

        for x in xrange(cnt_food):
            self.generate_food()
        for x in xrange(cnt_animals):
            self.generate_animal()

    def generate_food(self):
        self.food.append(Food())

    def generate_animal(self):
        self.animals.append(self.animal_base())

    def add_animal(self, animal):
        self.animals.append(animal)
