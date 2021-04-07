# Copyright (c) Durbich
# Licensed under the MIT License. See LICENSE file for license information.


def check_and_fix(max_x_y, new):
    max_x, max_y = max_x_y
    if new[0] == max_x:
        new = (0, new[1])
    if new[0] == -1:
        new = (max_x-1, new[1])
    if new[1] == max_y:
        new = (new[0], 0)
    if new[1] == -1:
        new = (new[0], max_y-1)
    return new


def is_self_eating(snake):
    """input must be list or tuple"""
    head = snake[0]
    for segment in snake[1:]:
        if head == segment:
            return True
    return False
