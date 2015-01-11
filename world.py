from __future__ import division
import random
import threading
import time
import uuid

class Food(object):
    def __init__(self, area, margin=0):
        self.area = area
        self.active = True
        self.generate(margin)

    def generate(self, margin):
        self.energy = random.random() * 2

        self.x = random.randint(0, self.area[0] - margin)
        self.y = random.randint(0, self.area[1] - margin)

class World(threading.Thread):
    def __init__(self, action_base, animal_base, area=(400, 400), seed=0, food_spawn_rate=0, verbose=False, deep_search_mate=False, deep_search_food=True):
        threading.Thread.__init__(self)

        self.food = []
        self.animals = []
        self.dead_animals = []

        self.action_base = action_base
        self.animal_base = animal_base

        self.seed = seed
        self.area = area
        self.area_safe_margin = 40

        self.max_mooses = 0
        self.age = 0
        self.sleep = 0
        self.verbose = verbose
        self.food_spawn_rate = food_spawn_rate

        self.deep_search_food = deep_search_food
        self.deep_search_mate = deep_search_mate
        self.running = False
        self.started = False

        self.generate()

    def set_sleep(self, timeout):
        self.sleep = timeout

    def set_max_mooses(self, maxmooses):
        self.max_mooses = maxmooses

    def generate(self):
        self.id = str(uuid.uuid4())
        if self.seed > 0:
            random.seed(self.seed)

        cnt_food = random.randint(10, 200)
        cnt_animals = random.randint(2, 10)
        if self.food_spawn_rate == 0:
            self.food_spawn_rate = random.randint(10, 100)
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
        self.food.append(Food(self.area, self.area_safe_margin))

    def generate_animal(self):
        if self.max_mooses > 2 and len(self.animals) > self.max_mooses:
            return
        self.animals.append(self.action_base(self.animal_base(), self, area=self.area))

    def add_animal(self, animal):
        if self.max_mooses > 2 and len(self.animals) > self.max_mooses:
            del animal
            return
        if self.verbose:
            print ('SPAWNING ANIMAL')
        self.animals.append(self.action_base(animal, self, area=self.area))

    def remove_animal(self, animal):
        if animal not in self.animals:
            return False

        self.animals.remove(animal)
        self.dead_animals.append(animal)
        return True

    def remove_food(self, food):
        if food not in self.food:
            return False

        food.active = False
        self.food.remove(food)

        return True

    def tick(self):
        self.age += 1
        if self.age % self.food_spawn_rate == 0 and bool(random.getrandbits(1)):
            if self.verbose:
                print ('NEW FOOD')
            self.generate_food()

        if len(self.animals) < 2:
            self.generate_animal()
            self.generate_animal()

        for act in self.animals:
            act.tick()

        if self.sleep > 0:
            time.sleep(self.sleep)

    def run(self):
        self.started = True
        self.running = True
        while self.running:
            self.tick()

    def stop(self):
        self.running = False

    def __str__(self):
        return 'World(%s, %s, %s, %s, %s, %s, %s, %s)' % (self.area, self.food_spawn_rate, self.seed, self.deep_search_food, self.deep_search_mate, self.age, len(self.food), len(self.animals))

    def __repr__(self):
        return self.__str__()
