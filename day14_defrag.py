"""Advent of Code -- Day 14

http://adventofcode.com/2017/day/14"""

from collections import Counter
from typing import Dict

from day10_knothash import knot_hash

assert knot_hash("206,63,255,131,65,80,238,157,254,24,133,2,16,0,1,3") == '20b7b54c92bf73cf3e5631458a715149'  # noqa

TEST_INPUT = 'flqrgnkx'

# from https://joernhees.de/blog/2010/09/21/how-to-convert-hex-strings-to-binary-ascii-strings-in-python-incl-8bit-space/
binary = lambda x: "".join(reversed( [i+j for i,j in zip( *[ ["{0:04b}".format(int(c,16)) for c in reversed("0"+x)][n::2] for n in [1,0] ] ) ] ))  # noqa


def calculate_knot_hash_grid(key):
    row_keys = [f'{key}-{i}' for i in range(128)]

    row_keys_hashed = [knot_hash(row).replace(' ', '0') for row in row_keys]
    row_keys_binary = [binary(row) for row in row_keys_hashed]
    return row_keys_binary


def count1s(input_):
    grid = calculate_knot_hash_grid(input_)
    counts = [Counter(list(row)) for row in grid]
    count1s = [row['1'] for row in counts]
    return sum(count1s)


def grid_to_dict(grid):
    grid_dict = {}

    for row_num, row in enumerate(grid):
        for col_num, value in enumerate(row):
            if value is '1':
                grid_dict[(row_num, col_num)] = int(value)
    return grid_dict


def find_num_groups(grid: Dict) -> int:
    """Find number of clusters in grid"""
    grid_copy = dict(grid)

    clusters = []

    while len(grid_copy) > 0:
        # pop off first element of dict
        curr_item = grid_copy.popitem()
        current_cluster = []
        current_cluster.append(curr_item[0])
        neighbours = list(get_neighbours(curr_item[0][0], curr_item[0][1]))

        while len(neighbours) > 0:
            neighbour_to_check = neighbours.pop()

            if neighbour_to_check in grid_copy:
                grid_copy.pop(neighbour_to_check)
                add_to_cluster = neighbour_to_check
                current_cluster.append(add_to_cluster)
                neighbours_to_add = list(get_neighbours(add_to_cluster[0],
                                                        add_to_cluster[1]))
                neighbours.extend(neighbours_to_add)

        clusters.append(current_cluster)

    return len(clusters)


def get_neighbours(x, y):
    yield (x-1, y)
    yield (x+1, y)
    yield (x, y-1)
    yield (x, y+1)


assert list(get_neighbours(0,0)) == [(-1, 0), (1, 0), (0, -1), (0, 1)]


if __name__ == "__main__":
    # assert count1s(TEST_INPUT) == 8108
    grid = calculate_knot_hash_grid(TEST_INPUT)
    grid_dict = grid_to_dict(grid)
    assert find_num_groups(grid_dict) == 1242

    # puzzle input
    PUZZLE_INPUT = 'jxqlasbh'
    print(count1s(PUZZLE_INPUT))
    grid = calculate_knot_hash_grid(PUZZLE_INPUT)
    grid_dict = grid_to_dict(grid)
    print(find_num_groups(grid_dict))
