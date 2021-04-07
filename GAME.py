# Copyright (c) Durbich
# Licensed under the MIT License. See LICENSE file for license information.


from configparser import ConfigParser
from threading import Thread
import random
import time
import os

import control
import snake
import field


# before draw a new frame we need to erase old, but comand depends on OS
screen_clear_comand = 'cls' if os.name == 'nt' else 'clear'

config = ConfigParser()
config.read('game_data.cfg')
highscore = int(config['player']['highscore'])
x, y = int(config['field']['x']), int(config['field']['y'])
bounds_around = True if config['field']['bounds_around'] == 'yes' else False

room_size = (x, y)
room = field.Field(room_size, bounds_around)
player = snake.Snake(room_size)
room.snake_draw(player.body)
room.spawn_food()
keypress = control.Control()
key_daemon = Thread(target=keypress.key_wait, daemon=True)
key_daemon.start()


def make_next_frame():
    # Let's update snake and super_food if is
    player.move()
    del_cell = player.check_released_cell()
    if del_cell:
        room.clear_cell(del_cell)
    if room.super_food_x_y:
        room.update_super_food()
    # checking for collision
    head = player.body[0]
    where_is_head = room.head_in_cell_out(head)
    if where_is_head == 'bound':
        player.die('wall bump')
    if where_is_head == 'food':
        player.food_eating()
        need_super_food = (player.length-4) % 5 == 0
        room.spawn_food(super_food=need_super_food)
        if need_super_food:
            room.update_super_food()
    if where_is_head == 'super food':
        player.food_eating(room.super_food_score)
    if player.is_dead:
        room.cells[head[1]][head[0]] = 'FF'
    if room.is_have_emptycell is False:
        player.die('There is no space for me in this world')
    os.system(screen_clear_comand)  # erase old screen
    room.framebuild()


dir_dict = {'w': 'U', 'a': 'L', 's': 'D', 'd': 'R'}
while True:
    time.sleep(0.2)
    if keypress.last_key:
        player.change_direction(dir_dict[keypress.last_key])
        keypress.last_key = None
    make_next_frame()
    if player.is_dead:
        break
    print('Score:', player.score)
    print('Highscore:', highscore)

print('GAME OVER! Reason of death:', player.reason_of_death)
print('You reach:', player.score)
if player.score > highscore:
    config['player']['highscore'] = str(player.score)
    with open('game_data.cfg', 'w') as storefile:
        config.write(storefile)
    print('New highscore! Previous:', highscore)
else:
    print('Highscore:', highscore)
