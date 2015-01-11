from __future__ import division
import random

class Actions(object):
    def __init__(self, item, world):
        self.item = item
        self.world = world
        self._moving = False

    def moving(self):
        self._moving = not self._moving
        return self._moving

    def random_direction(self):
        pass

    def moving_direction(self):
        if not self._moving:
            return

        self.random_direction()

    def look_for_food(self):
        return False

    def search_food(self):
        return

    def eat_food(self):
        return

    def move_to_food(self):
        return

    def look_for_partner(self):
        return False

    def others_in_range(self):
        return []

    def potential_partner(self, other):
        if other == self.item:
            return False
        return True

    def mate(self, other):
        return

    def move(self):
        return

    def tick(self):
        if not self.item.alive:
            return

        if self.moving():
            self.moving_direction()

        if self.look_for_food():
            self.search_food()
            self.eat_food()
            self.move_to_food()

        if self.look_for_partner():
            others = self.others_in_range()
            for other in others:
                if self.potential_partner(other):
                    self.mate(other)
                    break

        self.move()
        self.item.tick()
