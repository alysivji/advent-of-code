"""Advent of Code 2017 -- Day 6

http://adventofcode.com/2017/day/6
"""

from typing import Tuple

PROBLEM_INPUT = "14	0	15	12	11	11	3	5	1	6	8	4	9	1	8	4"
TEST_INPUT_PROBLEM1 = "0   2   7   0"


def reallocate_current_block_state(curr_blocks: tuple) -> tuple:
    blocks = list(curr_blocks)
    num_blocks = len(blocks)

    points_to_redistribute = max(blocks)
    max_index = blocks.index(points_to_redistribute)
    blocks[max_index] = 0

    # redistribute its blocks amongst all other blocks
    while points_to_redistribute > 0:
        current_index = (max_index + points_to_redistribute) % num_blocks
        blocks[current_index] += 1
        points_to_redistribute -= 1
    return tuple(blocks)


def memory_reallocation(memory: str) -> Tuple[str, str]:
    blocks = tuple(int(block) for block in memory.split())

    total_reallocs = 0
    seen_before = {}
    seen_before[blocks] = 0

    while True:
        # reallocate_blocks
        blocks = reallocate_current_block_state(blocks)
        total_reallocs += 1

        if blocks in seen_before:
            break
        else:
            seen_before[blocks] = total_reallocs

    return (f'Total Realloc: {total_reallocs}',
            f'Redistribution Cycles: {total_reallocs - seen_before[blocks]}')


if __name__ == '__main__':
    print(memory_reallocation(TEST_INPUT_PROBLEM1))
    print(memory_reallocation(PROBLEM_INPUT))
    print('fin.')
