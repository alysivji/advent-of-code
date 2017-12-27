"""Advent of Code 2017 -- Day 5

http://adventofcode.com/2017/day/5
"""

from typing import List


def count_steps_to_escape(maze: List[int]) -> int:
    maze = maze[:]
    total_steps = 0
    current_index = 0
    while current_index < len(maze):
        total_steps += 1
        previous_index = current_index
        current_index += maze[current_index]
        maze[previous_index] += 1

    return total_steps


assert count_steps_to_escape([0, 3, 0, 1, -3]) == 5


def offset_escape_steps(maze: List[int]) -> int:
    maze = maze[:]
    total_steps = 0
    current_index = 0
    while current_index < len(maze):
        total_steps += 1
        previous_index = current_index
        current_index += maze[current_index]

        if maze[previous_index] >= 3:
            maze[previous_index] -= 1
        else:
            maze[previous_index] += 1

    return total_steps


print(offset_escape_steps([0, 3, 0, 1, -3]))

if __name__ == '__main__':
    with open('05_input.txt', 'r') as f:
        maze = [int(line.strip()) for line in f.readlines()]

    print(count_steps_to_escape(maze))
    print(offset_escape_steps(maze))
    print('fin.')
