import random
import time

class Food(object):
    def __init__(self, area):
        self.area = area
        self.active = True
        self.generate()

    def generate(self):
        self.energy = random.random() * 2

        self.x = random.randint(0, self.area[0])
        self.y = random.randint(0, self.area[1])

class World(object):
    def __init__(self, animal_base, area=(400, 400), seed=0):
        self.food = []
        self.animals = []
        self.animal_base = animal_base
        self.seed = seed
        self.area = area
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
        self.food.append(Food(self.area))

    def generate_animal(self):
        self.animals.append(self.animal_base())

    def add_animal(self, animal):
        self.animals.append(animal)

    def remove_food(self, food):
        if food not in self.food:
            return False

        food.active = False
        self.food.remove(food)

        return True
