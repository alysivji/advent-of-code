"""Advent of Code 2017 -- Day 11

http://adventofcode.com/2017/day/11"""

from collections import deque
from typing import Tuple

DIRECTION = {
    'n': 0,
    'ne': 1,
    'se': 2,
    's': 3,
    'sw': 4,
    'nw': 5
}


class Hexagon:

    def __init__(self, level):
        self.level = level

        # n ne se s sw nw
        self.neighbours = [None, None, None, None, None, None]


def create_hexagon_mosaic(num_nodes):
    # create patient-zero hexagon (middle hexagon)
    stack = deque()
    center = Hexagon(level=0)
    stack.append(center)

    for _ in range(num_nodes):
        # pop off element
        curr_hexagon = stack.popleft()
        level = curr_hexagon.level

        # loop thru edges and if one is empty, add a hexago
        for idx, side in enumerate(curr_hexagon.neighbours):
            if side is None:
                new_hexagon = Hexagon(level=level+1)
                connection_edge = (idx + 3) % 6

                # connect to main
                curr_hexagon.neighbours[idx] = new_hexagon
                new_hexagon.neighbours[connection_edge] = curr_hexagon

                # connect to neighbors (if they exist)
                left_neighbour = curr_hexagon.neighbours[idx - 1]
                if left_neighbour:
                    new_hexagon.neighbours[(connection_edge + 1) % 6] = left_neighbour
                    left_neighbour.neighbours[(connection_edge + 1 + 3) % 6] = new_hexagon
                    stack.append(left_neighbour)

                right_neighbour = curr_hexagon.neighbours[(idx + 1) % 6]
                if right_neighbour:
                    new_hexagon.neighbours[connection_edge - 1] = right_neighbour
                    right_neighbour.neighbours[(connection_edge - 1 + 3) % 6] = new_hexagon
                    stack.append(right_neighbour)

    return center


def get_ending_level(center: Hexagon, moves: str) -> Tuple[int, int]:
    moves_list = moves.split(',')
    current_location = center
    max_distance = 0

    for move in moves_list:
        max_distance = max(max_distance, current_location.level)
        current_location = current_location.neighbours[DIRECTION[move]]

    return current_location.level, max_distance


if __name__ == '__main__':
    center = create_hexagon_mosaic(15_000_000)

    assert get_ending_level(center, "ne,ne,ne") == 3
    assert get_ending_level(center, 'ne,ne,sw,sw') == 0
    assert get_ending_level(center, 'ne,ne,s,s') == 2
    assert get_ending_level(center, 'se,sw,se,sw,sw') == 3

    with open('11_input.txt', 'r') as f:
        moves = f.readline().strip()

    print(get_ending_level(center, moves))
