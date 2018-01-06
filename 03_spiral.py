"""Advent of Code 2017 -- Day 3

http://adventofcode.com/2017/day/3"""

from collections import OrderedDict
import itertools
from typing import Dict, List

PUZZLE_INPUT = 312_051


class MemorySquare:
    def __init__(self, value, x, y):
        self.value = value
        self.x = x
        self.y = y

    def __repr__(self):
        return f'{self.value} @ ({self.x}, {self.y})'


def create_memory_table(top_limit: int) -> List:
    # add first node
    memory_table = {}
    value = 1
    memory_table[value] = MemorySquare(value, 0, 0)

    step_size = 1
    while value < top_limit:
        if step_size % 2 == 1:
            # x direction
            last_added = memory_table[list(memory_table.keys())[-1]]
            for new_x in range(last_added.x, last_added.x + step_size):
                value += 1
                new_memory_square = MemorySquare(value, new_x + 1, last_added.y)
                memory_table[value] = new_memory_square

            # y direction
            last_added = memory_table[list(memory_table.keys())[-1]]
            for new_y in range(last_added.y, last_added.y + step_size):
                value += 1
                new_memory_square = MemorySquare(value, last_added.x, new_y + 1)
                memory_table[value] = new_memory_square
        else:
            last_added = memory_table[list(memory_table.keys())[-1]]
            for new_x in range(last_added.x, last_added.x - step_size, -1):
                value += 1
                new_memory_square = MemorySquare(value, new_x - 1, last_added.y)
                memory_table[value] = new_memory_square

            # y direction
            last_added = memory_table[list(memory_table.keys())[-1]]
            for new_y in range(last_added.y, last_added.y - step_size, -1):
                value += 1
                new_memory_square = MemorySquare(value, last_added.x, new_y - 1)
                memory_table[value] = new_memory_square

        step_size += 1

    return memory_table


def manhattan_distance(square: MemorySquare) -> int:
    x_value = square.x
    y_value = square.y

    return abs(x_value) + abs(y_value)


def score_adjacent_blocks(memory: Dict, pos: tuple) -> int:
    """Add up diagonal if they exist"""
    x_offsets = [-1, 0, 1]
    y_offsets = [-1, 0, 1]

    value = 0
    for (x, y) in itertools.product(x_offsets, y_offsets):
        check_pos = (pos[0] + x, pos[1] + y)

        if check_pos in memory:
            value += memory[check_pos]

    return value


def create_cummulative_memory_table(top_limit: int) -> List:
    # add first node
    memory_table = OrderedDict()
    value = 1
    memory_table[(0, 0)] = value

    step_size = 1
    while value < top_limit:

        if step_size % 2 == 1:
            # x direction
            last_added = list(memory_table.keys())[-1]
            for new_x in range(last_added[0], last_added[0] + step_size):
                new_block_x = new_x + 1
                new_block_y = last_added[1]
                new_pos = (new_block_x, new_block_y)
                value = score_adjacent_blocks(memory_table, new_pos)
                memory_table[new_pos] = value

            # y direction
            last_added = list(memory_table.keys())[-1]
            for new_y in range(last_added[1], last_added[1] + step_size):
                new_block_x = last_added[0]
                new_block_y = new_y + 1
                new_pos = (new_block_x, new_block_y)
                value = score_adjacent_blocks(memory_table, new_pos)
                memory_table[new_pos] = value

        else:
            last_added = list(memory_table.keys())[-1]
            for new_x in range(last_added[0], last_added[0] - step_size, -1):
                new_block_x = new_x - 1
                new_block_y = last_added[1]
                new_pos = (new_block_x, new_block_y)
                value = score_adjacent_blocks(memory_table, new_pos)
                memory_table[new_pos] = value

            # y direction
            last_added = list(memory_table.keys())[-1]
            for new_y in range(last_added[1], last_added[1] - step_size, -1):
                new_block_x = last_added[0]
                new_block_y = new_y - 1
                new_pos = (new_block_x, new_block_y)
                value = score_adjacent_blocks(memory_table, new_pos)
                memory_table[new_pos] = value

        step_size += 1

    return memory_table


if __name__ == '__main__':
    # memory = create_memory_table(312_051)

    # assert manhattan_distance(memory[1]) == 0
    # assert manhattan_distance(memory[12]) == 3
    # assert manhattan_distance(memory[23]) == 2
    # assert manhattan_distance(memory[1024]) == 31

    pass
