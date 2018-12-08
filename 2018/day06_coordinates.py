from collections import Counter
from typing import List, NamedTuple, Optional

from more_itertools import flatten


class Coordinate(NamedTuple):
    col: int
    row: int


class Bounds(NamedTuple):
    col_max: int
    row_max: int


def load_input(lines: List[str]) -> List[Coordinate]:
    all_coords = []
    for line in lines:
        x, y = line.strip().split(", ")
        all_coords.append(Coordinate(int(x), int(y)))
    return all_coords


def find_bounds(coordinates: List[Coordinate]) -> Bounds:
    cols = [coord.col for coord in coordinates]
    rows = [coord.row for coord in coordinates]
    return Bounds(col_max=max(cols), row_max=max(rows))


def manhattan_distance(first: Coordinate, second: Coordinate):
    return abs(first.col - second.col) + abs(first.row - second.row)


def find_closest(position, coordinates: List[Coordinate]) -> Optional[Coordinate]:
    all_pos = [(coord, manhattan_distance(position, coord)) for coord in coordinates]
    closest = min(all_pos, key=lambda x: x[1])

    total_num = 0
    for coord, distance in all_pos:
        if closest[1] == distance:
            total_num += 1
        if total_num > 1:
            return None
    return closest[0]


def generate_closest_point_grid(
    coordinates: List[Coordinate]
) -> List[List[Coordinate]]:
    bounds = find_bounds(coordinates)

    grid = []
    for _ in range(0, bounds.row_max + 1):
        row = [0] * (bounds.col_max + 1)
        grid.append(row)

    for row in range(0, len(grid)):
        for col in range(0, len(grid[row])):
            grid[row][col] = find_closest(Coordinate(row=row, col=col), coordinates)

    return grid


def find_largest_non_infinte(
    coordinates: List[Coordinate], grid: List[List[Coordinate]]
) -> Coordinate:
    all_coords = set(coordinates)

    # remove edges
    for item in grid[0]:
        all_coords.discard(item)
    for item in grid[-1]:
        all_coords.discard(item)
    for row in grid:
        all_coords.discard(row[0])
        all_coords.discard(row[-1])

    c = Counter()
    for item in flatten(grid):
        if item in all_coords:
            c[item] += 1

    return c.most_common(1)[0][1]


def num_square_safe(coordinates: List[Coordinate], max_distance: int) -> int:
    bounds = find_bounds(coordinates)

    grid = []
    for _ in range(0, bounds.row_max + 1):
        row = [0] * (bounds.col_max + 1)
        grid.append(row)

    total = 0
    for row in range(0, len(grid)):
        for col in range(0, len(grid[row])):
            total_distance = sum(
                manhattan_distance(Coordinate(row=row, col=col), coord)
                for coord in coordinates
            )
            grid[row][col] = 1 if total_distance <= max_distance else 0
            total += 1 if total_distance < max_distance else 0
    return total


TEST_INPUT = """1, 1
1, 6
8, 3
3, 4
5, 5
8, 9""".split(
    "\n"
)

test_coordinates = load_input(TEST_INPUT)
grid = generate_closest_point_grid(test_coordinates)
assert find_largest_non_infinte(test_coordinates, grid) == 17
assert num_square_safe(test_coordinates, max_distance=32) == 16


if __name__ == "__main__":
    with open("day06_input.txt") as f:
        lines = f.readlines()

    coordinates = load_input(lines)
    grid = generate_closest_point_grid(coordinates)
    print(find_largest_non_infinte(coordinates, grid))
    print(num_square_safe(coordinates, 10000))
