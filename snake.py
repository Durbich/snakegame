# Copyright (c) Durbich
# Licensed under the MIT License. See LICENSE file for license information.


import headcollision


class Snake:
    def __init__(self, max_x_y):
        self.length = 4
        self.is_dead = False
        self.reason_of_death = "I'm not dead you fool"
        self.direction = (1, 0)  # MATTER: body[X][Y]
        _y = max_x_y[1]//2
        self.body = [(4, _y), (3, _y), (2, _y), (1, _y)]
        self.score = 0
        self.released_cell_value = ()
        self.max_x_y = max_x_y

    def move(self):
        """1 call = 1 step forward"""

        newpoint = (self.body[0][0] + self.direction[0],
                    self.body[0][1] + self.direction[1])
        newpoint = headcollision.check_and_fix(self.max_x_y, newpoint)
        self.body.insert(0, newpoint)

        if len(self.body) > self.length:
            self.released_cell_value = self.body[-1]
            del self.body[-1]
        if headcollision.is_self_eating(self.body):
            self.is_dead = True
            self.reason_of_death = 'mazohism'

    def check_released_cell(self):
        out = self.released_cell_value
        self.released_cell_value = ()
        return out

    def change_direction(self, new):
        if self.direction[1]:
            if new == 'R':
                self.direction = (1, 0)
            if new == 'L':
                self.direction = (-1, 0)
        if self.direction[0]:
            if new == 'U':
                self.direction = (0, 1)
            if new == 'D':
                self.direction = (0, -1)

    def food_eating(self, points=1):
        self.length += 1
        self.score += points

    def die(self, reason=None):
        self.is_dead = True
        if reason:
            self.reason_of_death = reason
