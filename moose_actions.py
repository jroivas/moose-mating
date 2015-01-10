import actions
import math
import random

class MooseActions(actions.Actions):
    def __init__(self, item, world, area=(400, 400)):
        super(MooseActions, self).__init__(item, world)
        self.area = area

        self._still = False
        self._still_timer = 0
        self._mate_timer = 0
        self._can_mate = True
        self._searching = False

        self.x = random.randint(0, self.area[0])
        self.y = random.randint(0, self.area[1])

        self.speed = 0
        self.xspeed = 0
        self.yspeed = 0

        self.jumpindex = 0
        self.yshift = 0
        self.yforce = 0

        self.grownup_age = 20
        self.year_in_ticks = 200

        self.eatarea = 20
        self.potential_food = None
        self.potential_food_dist = 0

        self.path = []

    def handle_timers(self):
        if self._still_timer == 0:
            self._still = False
        else:
            self._still_timer -= 1

        if self._mate_timer == 0:
            self._can_mate = True
        else:
            self._mate_timer -= 1

    def moving(self):
        self.handle_timers()

        if not self._moving and not self._still and random.randint(0, 100) < self.item.stillchange:
            self._moving = not self._moving
            self.random_direction()
        elif self._moving and random.randint(0, 100) < self.item.movingchange:
            self._moving = not self._moving

        return self._moving

    def random_direction(self):
        self.speed = self.item.minspeed
        self.speed += random.random() * (self.item.maxspeed - self.item.minspeed)

        # TODO: Old animals slow down

        absx = random.random() * self.speed
        absy = self.speed - absx

        # Adjust for negative values as well
        if self.item.randomBool():
            self.xspeed = -absx
        else:
            self.xspeed = absx

        if self.item.randomBool():
            self.yspeed = -absy
        else:
            self.yspeed = absy

    def look_for_food(self):
        return (self._searching or random.randint(0, 20) == 10) and (
            (self.item.energy / self.item.maxenergy * 100) < 91)

    def head_to(self, hx, hy):
        dx = self.x - hx
        dy = self.y - hy

        while abs(dx) + abs(dy) > self.item.maxspeed:
            dx *= 0.7
            dy *= 0.7

        xspeed = -dx
        yspeed = -dy

    def search_food(self):
        self.potential_food = None
        self.potential_food_dist = 9999999
        for food in self.world.food:
            if not food.active:
                continue
            dx = self.x - food.x
            dy = self.y - food.y

            dist = math.sqrt(dx * dx + dy * dy)
            if dist < self.item.viewarea and dist < self.potential_food_dist:
                self.potential_food = food
                self.potential_food_dist = dist
                if not self.world.deep_search:
                    break

        if self.potential_food is not None:
            self.head_to(self.potential_food.x, self.potential_food.y)

    def eat_food(self):
        if self.potential_food is None:
            return

        if self.potential_food_dist >= 0 and self.potential_food_dist <= self.eatarea:
            self._moving = False
            self._searching = False
            if self.world.remove_food(self.potential_food):
                self.item.energy += self.potential_food.energy
                if self.item.energy > self.item.maxenergy:
                    self.item.energy = self.item.maxenergy

    def move_to_food(self):
        if self.potential_food is None:
            return

        if self.potential_food_dist >= 0 and self.potential_food_dist <= self.item.viewarea:
            self._moving = True
            self._searching = True

    def ensure_moving_area(self):
        if not self._moving:
            return

        self.path.append((self.x, self.y))
        self.y = self.y + self.yspeed
        self.x = self.x + self.xspeed

        if self.x < 0:
            self.x = 0
            self.random_direction()
        if self.x > self.area[0]:
            self.x = self.area[0]
            self.random_direction()

        if self.y < 0:
            self.y = 0
            self.random_direction()
        if self.y > self.area[1]:
            self.y = self.area[1]
            self.random_direction()

    def jumping(self):
        if self._moving or self.yshift > 3:
            self.jumpindex = self.jumpindex % self.item.jumpforce
            if self.jumpindex < (self.item.jumpforce / 2):
                self.yshift = self.jumpindex
            else:
                self.yshift = self.item.jumpforce - self.jumpindex
            self.jumpindex += 1
        else:
            self.yshift = 0

    def decrease_energy(self):
        if self._moving:
            self.item.energy -= self.item.energymoving
        else:
            self.item.energy -= self.item.energystill

        if self.item.energy < 0:
            self.item.die()

    def look_for_partner(self):
        return random.randint(0, 20) == 5

    def mateable(self):
        return self._can_mate and (self.item.age > self.grownup_age * self.year_in_ticks)

    def others_in_range(self):
        res = []
        for animal in self.world.animals:
            if not animal.item.alive:
                continue
            if animal == self:
                continue
            if animal.item == self.item:
                continue

            # FIXME?
            dx = self.x - (animal.x + 50)
            dy = self.y - animal.y

            dist = math.sqrt(dx * dx + dy * dy)
            if not (dist > 0 and dist < self.item.viewarea):
                continue

            if dist < 30:
                res.append(animal)
                if not self.world.deep_search:
                    break
            else:
                self.head_to(animal.x + 50, animal.y)
        return res

    def potential_partner(self, animal):
        self._moving = False
        animal._moving = False
        energya = self.item.energy / self.item.maxenergy
        energyb = animal.item.energy / animal.item.maxenergy
        multipl = (1.0 / energya * 1.0 / energyb) * 5

        if not (self.mateable() and animal.mateable()):
            return False

        if self._still or animal._still:
            return False

        if int(math.floor(random.random() * multipl)) != 1:
            return False

        return True

    def mate(self, animal):
        self._still = True
        animal._still = True
        self._still_timer = 10
        self._mate_timer = 20

        new_animal = self.item.combine(animal.item)
        self.world.add_animal(new_animal)

    def move(self):
        self.ensure_moving_area()
        self.jumping()
        self.decrease_energy()
