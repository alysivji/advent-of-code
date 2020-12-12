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
        for col_idx, seat in enumerate(row):
            if seat == "L":
                seats[(row_idx, col_idx)] = "L"
    return seats


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

            if (x_to_check, y_to_check) in seats:
                if seats[(x_to_check, y_to_check)] == "#":
                    occupied_seats += 1

        if seat == "L":
            if occupied_seats == 0:
                new_layout[location] = "#"
        else:
            if occupied_seats >= 4:
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


if __name__ == "__main__":
    with open("2020/data/day11_input.txt") as f:
        seating_map = f.read().strip()
        seats = create_seating_chart(seating_map)

    result = num_seats_occupied_when_pattern_converges(seats, step_part1)
    print(f"part 1 is {result}")
