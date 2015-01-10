import actions
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

        self.x = 0
        self.y = 0
        self.speed = 0
        self.xspeed = 0
        self.yspeed = 0

        self.jumpindex = 0
        self.yshift = 0
        self.yforce = 0

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

    def search_food(self):
        return

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

    def move(self):
        self.ensure_moving_area()
        self.jumping()
        self.decrease_energy()
