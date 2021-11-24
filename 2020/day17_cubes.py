from collections import defaultdict
from itertools import permutations

import pytest


@pytest.fixture
def test_input():
    return """.#.
    ..#
    ###"""


def generate_initial_state_3d(config: str):
    state = {}
    for x_idx, row in enumerate(config.split("\n")):
        for y_idx, value in enumerate(row.strip()):
            state[(x_idx, y_idx, 0)] = True if value == "#" else False
    return state


def step_3d(state):
    # get all coordinates for next step_3d
    all_coordinates = set()
    for current_coordinate in state.keys():
        for adj_coordinate in adjacent_coordinates_3d(current_coordinate):
            all_coordinates.add(adj_coordinate)

    # count up all adjacent
    adj_active = defaultdict(int)
    for coord in all_coordinates:
        for neighbour in adjacent_coordinates_3d(coord):
            if state.get(neighbour, False):
                adj_active[coord] += 1

    new_state = {}
    for coord in all_coordinates:
        num_active = adj_active[coord]
        prev_state_is_active = state.get(coord, False)
        if prev_state_is_active:
            if 2 <= num_active <= 3:
                new_state[coord] = True
            else:
                new_state[coord] = False
        else:
            if num_active == 3:
                new_state[coord] = True
            else:
                new_state[coord] = False

    return new_state


def count_active(state):
    count = 0
    for k, v in state.items():
        if v:
            count += 1
    return count


def adjacent_coordinates_3d(coordinate):
    x, y, z = coordinate

    for x_diff in [-1, 0, 1]:
        for y_diff in [-1, 0, 1]:
            for z_diff in [-1, 0, 1]:
                # skip current coordinate
                if x_diff == y_diff == z_diff == 0:
                    continue
                yield (x + x_diff, y + y_diff, z + z_diff)


def test_generate_initial_state_3d(test_input):
    state = generate_initial_state_3d(test_input)
    assert len(state) == 9


def test_part1(test_input):
    state = generate_initial_state_3d(test_input)
    for _ in range(6):
        state = step_3d(state)
    assert count_active(state) == 112


def print_state_3d(state):
    z_min = min(z for x, y, z in state.keys())
    z_max = max(z for x, y, z in state.keys())
    x_min = min(x for x, y, z in state.keys())
    x_max = max(x for x, y, z in state.keys())

    for curr_z in range(z_min, z_max + 1):
        coordinates = {
            (x, y, z): value for (x, y, z), value in state.items() if z == curr_z
        }
        print(f"z={curr_z}")
        output = ""
        for curr_x in range(x_min, x_max + 1):
            for curr_y in range(x_min, x_max + 1):
                output += "#" if state[(curr_x, curr_y, curr_z)] else "."
            output += "\n"

        print(output)


def generate_initial_state_4d(config: str):
    state = {}
    for x_idx, row in enumerate(config.split("\n")):
        for y_idx, value in enumerate(row.strip()):
            state[(x_idx, y_idx, 0, 0)] = True if value == "#" else False
    return state


def step_4d(state):
    # get all coordinates for next step_4d
    all_coordinates = set()
    for current_coordinate in state.keys():
        for adj_coordinate in adjacent_coordinates_4d(current_coordinate):
            all_coordinates.add(adj_coordinate)

    # count up all adjacent
    adj_active = defaultdict(int)
    for coord in all_coordinates:
        for neighbour in adjacent_coordinates_4d(coord):
            if state.get(neighbour, False):
                adj_active[coord] += 1

    new_state = {}
    for coord in all_coordinates:
        num_active = adj_active[coord]
        prev_state_is_active = state.get(coord, False)
        if prev_state_is_active:
            if 2 <= num_active <= 3:
                new_state[coord] = True
            else:
                new_state[coord] = False
        else:
            if num_active == 3:
                new_state[coord] = True
            else:
                new_state[coord] = False

    return new_state


def adjacent_coordinates_4d(coordinate):
    x, y, z, w = coordinate

    for x_diff in [-1, 0, 1]:
        for y_diff in [-1, 0, 1]:
            for z_diff in [-1, 0, 1]:
                for w_diff in [-1, 0, 1]:
                    # skip current coordinate
                    if x_diff == y_diff == z_diff == w_diff == 0:
                        continue
                    yield (x + x_diff, y + y_diff, z + z_diff, w + w_diff)


if __name__ == "__main__":
    with open('2020/data/day17_input.txt', 'r') as f:
        initial_state = f.read()

    state = generate_initial_state_3d(initial_state)
    for _ in range(6):
        state = step_3d(state)
    print(f"Result for part 1 is {count_active(state)}")

    state = generate_initial_state_4d(initial_state)
    for _ in range(6):
        state = step_4d(state)
    print(f"Result for part 2 is {count_active(state)}")
