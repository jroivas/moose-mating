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
    def __init__(self, action_base, animal_base, area=(400, 400), seed=0, food_spawn_rate=0, verbose=False):
        self.food = []
        self.animals = []
        self.action_base = action_base
        self.animal_base = animal_base
        self.seed = seed
        self.area = area
        self.age = 0
        self.verbose = verbose
        self.food_spawn_rate = food_spawn_rate
        self.generate()

    def generate(self):
        if self.seed > 0:
            random.seed(self.seed)

        cnt_food = random.randint(10, 1000)
        cnt_animals = random.randint(2, 10)
        if self.food_spawn_rate == 0:
            self.food_spawn_rate = random.randint(500, 10000)
            if self.verbose:
                print ('Food spawn rate: %s' % self.food_spawn_rate)

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
        self.animals.append(self.action_base(self.animal_base(), self, area=self.area))

    def add_animal(self, animal):
        if self.verbose:
            print ('SPAWNING ANIMAL')
        self.animals.append(self.action_base(animal, self, area=self.area))

    def remove_food(self, food):
        if food not in self.food:
            return False

        food.active = False
        self.food.remove(food)

        return True

    def tick(self):
        for act in self.animals:
            act.tick()
            self.age += 1
            if self.age % self.food_spawn_rate == 0 and bool(random.getrandbits(1)):
                if self.verbose:
                    print ('NEW FOOD')
                self.generate_food()
