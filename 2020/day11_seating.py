from typing import Dict
import pytest


@pytest.fixture
def seating_map():
    return """L.LL.LL.LL
    LLLLLLL.LL
    L.L.L..L..
    LLLL.LL.LL
    L.LL.LL.LL
    L.LLLLL.LL
    ..L.L.....
    LLLLLLLLLL
    L.LLLLLL.L
    L.LLLLL.LL"""


def create_seating_chart(seat_layout):
    seats = {}
    for row_idx, row in enumerate(seat_layout.split("\n")):
        for col_idx, seat in enumerate(row.strip()):
            seats[(row_idx, col_idx)] = seat
    return seats


def print_seat(seat_dict):
    rows = 0
    while True:
        if (rows + 1, 0) not in seat_dict:
            break
        rows += 1

    cols = 0
    while True:
        if (0, cols + 1) not in seat_dict:
            break
        cols += 1

    for i in range(rows):
        row = ""
        for j in range(cols):
            row += seat_dict[(i, j)]
        print(row)

DIRECTIONS = [
    (-1, 0),  # up
    (1, 0),  # down
    (0, -1),  # left
    (0, 1),  # right
    (-1, -1),  # up,left
    (1, 1),  # down, right
    (-1, 1),  # up, right
    (1, -1),  # down, left
]


def step_part1(seats: Dict):
    new_layout = seats.copy()
    for location, seat in seats.items():
        # how many occupied seats adjacent to this one
        x, y = location
        occupied_seats = 0
        for dx, dy in DIRECTIONS:
            x_to_check = x + dx
            y_to_check = y + dy

            try:
                if seats[(x_to_check, y_to_check)] == "#":
                    occupied_seats += 1
            except KeyError:
                continue

        if seat == "L":
            if occupied_seats == 0:
                new_layout[location] = "#"
        elif seat == "#":
            if occupied_seats >= 4:
                new_layout[location] = "L"

    return new_layout


def find_adjacent_occupied(seats, location):
    x, y = location
    occupied_seats = 0
    for dx, dy in DIRECTIONS:
        multiplication_factor = 0
        looking_for_seat = True
        while looking_for_seat:
            multiplication_factor += 1
            x_to_check = x + dx * multiplication_factor
            y_to_check = y + dy * multiplication_factor

            try:
                if seats[(x_to_check, y_to_check)] == "#":
                    occupied_seats += 1
                    looking_for_seat = False
                elif seats[(x_to_check, y_to_check)] == "L":
                    looking_for_seat = False
            except KeyError:
                looking_for_seat = False
    return occupied_seats


INPUT_1 = """.......#.
...#.....
.#.......
.........
..#L....#
....#....
.........
#........
...#....."""
INPUT_2 = """.............
.L.L.#.#.#.#.
............."""
INPUT_3 = """.##.##.
#.#.#.#
##...##
...L...
##...##
#.#.#.#
.##.##."""


@pytest.mark.parametrize(
    "input_str,location,occupied_seats",
    [
        (INPUT_1, (4, 3), 8),
        (INPUT_2, (1, 1), 0),
        (INPUT_2, (1, 3), 1),
        (INPUT_3, (3, 3), 0),
    ],
)
def test_find_adjacent_occupied(input_str, location, occupied_seats):
    seats = create_seating_chart(input_str)
    result = find_adjacent_occupied(seats, location)

    assert result == occupied_seats


def step_part2(seats: Dict):
    new_layout = seats.copy()
    for location, seat in seats.items():
        occupied_seats = find_adjacent_occupied(seats, location)
        if seat == "L":
            if occupied_seats == 0:
                new_layout[location] = "#"
        elif seat == "#":
            if occupied_seats >= 5:
                new_layout[location] = "L"

    return new_layout


def num_seats_occupied_when_pattern_converges(seats, step_fn):
    while True:
        result = step_fn(seats)
        if seats == result:
            break
        seats = result

    occupied_seats = 0
    for key, value in seats.items():
        if value == "#":
            occupied_seats += 1

    return occupied_seats


def test_converge_part_1(seating_map):
    seats = create_seating_chart(seating_map)

    assert num_seats_occupied_when_pattern_converges(seats, step_part1) == 37


def test_converge_part_2(seating_map):
    seats = create_seating_chart(seating_map)

    assert num_seats_occupied_when_pattern_converges(seats, step_part2) == 26


if __name__ == "__main__":
    with open("2020/data/day11_input.txt") as f:
        seating_input = f.read().strip()
        seats = create_seating_chart(seating_input)

    result = num_seats_occupied_when_pattern_converges(seats, step_part1)
    print(f"part 1 is {result}")

    result = num_seats_occupied_when_pattern_converges(seats, step_part2)
    print(f"part 2 is {result}")
