"""Advent of Code -- Day 16

http://adventofcode.com/2017/day/16"""

from typing import Dict, List


def create_initial_position(num_programs: int) -> List[str]:
    """a stats at 0 and so on until we hit num_programs"""

    letter_a_position = ord('a')
    starting_grid = []
    for letter in range(letter_a_position, letter_a_position + num_programs):
        starting_grid.append(chr(letter))

    return starting_grid


def spin(positions: List[str], x) -> List[str]:
    """Makes X programs move from the end to the front"""
    new_positions = list(positions[-x:]) + list(positions[:-x])
    return new_positions


def exchange(positions: List[str], swap1: int, swap2: int) -> List[str]:
    """makes the programs at positions A and B swap places"""
    new_positions = list(positions)
    new_positions[swap1], new_positions[swap2] = \
        new_positions[swap2], new_positions[swap1]

    return new_positions


def parnter(positions: List[str], item1: str, item2: str) -> List[str]:
    """makes the programs named A and B swap places"""
    position1 = positions.index(item1)
    position2 = positions.index(item2)
    return exchange(positions, position1, position2)


def dance_puppets(position: List[str], moves: List[str]) -> List[str]:
    dance_position = list(position)
    for move in all_moves:
        action = move[:1]
        remaining_move = move[1:]

        if action == 's':
            dance_position = spin(dance_position, int(remaining_move))
        elif action == 'x':
            pos1, pos2 = remaining_move.split('/')
            dance_position = exchange(dance_position, int(pos1), int(pos2))
        elif action == 'p':
            item1, item2 = remaining_move.split('/')
            dance_position = parnter(dance_position, item1, item2)
    return dance_position


def get_pattern(positions: List[str],
                moves: List[str],
                num_dances: int) -> Dict[int, str]:
    """Find pattern"""
    dance_position = list(position)

    pattern_finder = {}
    for count in range(num_dances):
        dance_position = dance_puppets(dance_position, moves)
        pattern_finder[count + 1] = ''.join(dance_position)

    return pattern_finder


if __name__ == '__main__':
    TEST_NUM_PROGRAMS = 5
    TEST_START_POSITION = create_initial_position(TEST_NUM_PROGRAMS)
    assert spin(TEST_START_POSITION, 3) == ['c', 'd', 'e', 'a', 'b']

    first_move = spin(TEST_START_POSITION, 1)
    assert first_move == ['e', 'a', 'b', 'c', 'd']

    second_move = exchange(first_move, 3, 4)
    assert second_move == ['e', 'a', 'b', 'd', 'c']

    third_move = parnter(second_move, 'e', 'b')
    assert third_move == ['b', 'a', 'e', 'd', 'c']

    # read in input
    all_moves: List[str] = []
    with open('day16_input.txt', 'r') as f:
        all_moves = f.readline().strip().split(',')

    position = create_initial_position(16)
    final_position = dance_puppets(position, all_moves)
    print(''.join(final_position))

    # using trial and error we see pattern repeats every 30
    pattern = get_pattern(position, all_moves, 30)
    print(pattern[1_000_000_000 % 30])
