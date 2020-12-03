import math
from typing import Set, NamedTuple


class Square(NamedTuple):
    row: int
    column: int


class Grid(NamedTuple):
    rows: int
    columns: int
    trees: Set[Square]


def create_grid(lines):
    trees = set()
    for row, line in enumerate(lines):
        line = line.strip()
        for col, square in enumerate(line):
            if square == "#":
                trees.add(Square(row, col))

    return Grid(rows=len(lines), columns=len(line), trees=trees)


def number_of_trees_hit(grid: Grid, right: int, down: int) -> int:
    current_square = Square(row=0, column=0)
    num_trees_hit = 0
    while current_square.row < grid.rows:
        if (
            Square(row=current_square.row, column=current_square.column % grid.columns)
            in grid.trees
        ):
            num_trees_hit += 1
        current_square = Square(
            row=current_square.row + down, column=current_square.column + right
        )

    return num_trees_hit


def test_number_of_trees_hit():
    TEST_INPUT = """..##.......
    #...#...#..
    .#....#..#.
    ..#.#...#.#
    .#...##..#.
    ..#.##.....
    .#.#.#....#
    .#........#
    #.##...#...
    #...##....#
    .#..#...#.#"""
    grid = create_grid(TEST_INPUT.split("\n"))

    trees_hit = number_of_trees_hit(grid, right=3, down=1)

    assert trees_hit == 7


def test_part_two():
    TEST_INPUT = """..##.......
    #...#...#..
    .#....#..#.
    ..#.#...#.#
    .#...##..#.
    ..#.##.....
    .#.#.#....#
    .#........#
    #.##...#...
    #...##....#
    .#..#...#.#"""
    grid = create_grid(TEST_INPUT.split("\n"))

    trees_hit = []
    for (right, left) in [(1, 1), (3, 1), (5, 1), (7, 1), (1, 2)]:
        hit = number_of_trees_hit(grid, right, left)
        trees_hit.append(hit)

    return math.prod(trees_hit) == 336


if __name__ == "__main__":
    with open("2020/data/day03_input.txt") as f:
        grid = create_grid(f.readlines())

    trees_hit = number_of_trees_hit(grid, right=3, down=1)
    print(f"Part 1 answer is {trees_hit}")

    trees_hit = []
    for (right, left) in [(1, 1), (3, 1), (5, 1), (7, 1), (1, 2)]:
        hit = number_of_trees_hit(grid, right, left)
        trees_hit.append(hit)
    result = math.prod(trees_hit)
    print(f"Part 2 answer is {result}")
