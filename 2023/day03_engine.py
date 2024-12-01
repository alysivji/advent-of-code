from typing import NamedTuple

class Point(NamedTuple):
    x: int
    y: int

    def get_diagonals(self: "Point") -> list["Point"]:
        return [
            Point(self.x + 1, self.y),
            Point(self.x - 1, self.y),
            Point(self.x, self.y + 1),
            Point(self.x, self.y - 1),
            Point(self.x + 1, self.y - 1),
            Point(self.x + 1, self.y + 1),
            Point(self.x - 1, self.y + 1),
            Point(self.x - 1, self.y - 1),
        ]

SAMPLE_INPUT = """467..114..
...*......
..35..633.
......#...
617*......
.....+.58.
..592.....
......755.
...$.*....
.664.598..
"""


def read_input(input: str) -> dict[Point, str]:
    lines = input.split("\n")
    engine = {}
    for y, line in enumerate(lines):
        for x, value in enumerate(line):
            engine[Point(x, y)] = value
    return engine

def sum_part_numbers(engine: dict[Point, str]) -> int:
    part_number_sum = 0
    for point, value in engine.items():
        if str.isnumeric(value):
            continue
        if value == ".":
            continue
        all_directions = point.get_diagonals()

        for direction in all_directions:
            if direction not in engine:
                continue
            direction_value = engine[direction]
            if str.isnumeric(direction_value):
                part_number_sum += int(direction_value)
    return part_number_sum



# with open("data/day03_input.txt") as f:
#     lines = [line.strip() for line in f.readlines()]


engine = read_input(SAMPLE_INPUT)
result = sum_part_numbers(engine)
