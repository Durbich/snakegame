# Copyright (c) Durbich
# Licensed under the MIT License. See LICENSE file for license information.


from random import choice as rand_choice


class Field:
    def __init__(self, xysize, bounds_around=False):
        self.xsize, self.ysize = xysize
        self.x_out = [-1, self.xsize]
        self.y_out = [-1, self.ysize]
        self.snakecell = '██'
        self.boundcell = '><'
        self.emptycell = '  '
        self.is_have_emptycell = True
        self.foodcell = '+1'
        self.super_food_cell = '+0'
        self.super_food_score = 0
        self.super_food_start_score = self.xsize//2 + self.ysize//2
        if self.super_food_start_score > 99:
            self.super_food_start_score = 99
        self.super_food_x_y = None  # if have - will be tuple
        self.cells = [            # MATTER: cells[Y][X]
            [self.emptycell for i in range(self.xsize)]
            for i in range(self.ysize)
            ]
        if bounds_around:
            horisontal = [self.boundcell for i in range(self.xsize)]
            self.cells[0] = horisontal.copy()
            self.cells[-1] = horisontal.copy()
            for i in range(self.ysize-2):
                self.cells[i+1][0] = self.boundcell
                self.cells[i+1][-1] = self.boundcell

    def snake_draw(self, snake):
        for segment in snake:
            self.cells[segment[1]][segment[0]] = self.snakecell

    def framebuild(self):
        print('╔'+'══'*self.xsize+'╗')
        for y in self.cells[::-1]:
            print('║', end='')
            for x in y:
                print(x, end='')
            print('║')
        print('╚'+'══'*self.xsize+'╝')

    def head_in_cell_out(self, head):
        head_position = self.cells[head[1]][head[0]]
        self.cells[head[1]][head[0]] = self.snakecell
        if head_position == self.emptycell:
            return 'empty'
        if head_position == self.boundcell:
            return 'bound'
        if head_position == self.foodcell:
            return 'food'
        if head_position == self.super_food_cell:
            self.kill_super_food()
            return 'super food'

    def spawn_food(self, super_food=False):
        availablecells = []
        y = 0
        while y < self.ysize:
            x = 0
            while x < self.xsize:
                if self.cells[y][x] == self.emptycell:
                    availablecells.append((x, y))
                x += 1
            y += 1
        if availablecells:
            foodcell = rand_choice(availablecells)
            self.cells[foodcell[1]][foodcell[0]] = self.foodcell
            if super_food:
                availablecells.remove(foodcell)
                if availablecells:
                    self.super_food_x_y = rand_choice(availablecells)
                    self.super_food_score = self.super_food_start_score
        else:
            self.is_have_emptycell = False

    def update_super_food(self):
        if self.super_food_x_y:
            if self.super_food_score == 0:
                _x, _y = self.super_food_x_y
                self.kill_super_food()
                self.cells[_y][_x] = self.emptycell
            else:
                _x, _y = self.super_food_x_y
                self.super_food_score -= 1
                if self.super_food_score >= 10:
                    self.super_food_cell = f'{self.super_food_score}'
                else:
                    self.super_food_cell = f'+{self.super_food_score}'
                self.cells[_y][_x] = self.super_food_cell

    def kill_super_food(self):
        self.super_food_x_y = None

    def clear_cell(self, cell):
        self.cells[cell[1]][cell[0]] = self.emptycell
