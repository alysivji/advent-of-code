from enum import IntEnum
from utils import IntCodeComputer, Halt


class Tile:
    EMPTY = 0
    SCAFFOLD = 1
    ROBOT_FACING_UP = 2
    ROBOT_FACING_DOWN = 3
    ROBOT_FACING_LEFT = 4
    ROBOT_FACING_RIGHT = 5


ASCII_TO_TILE = {
    10: "\n",
    35: Tile.SCAFFOLD,
    46: Tile.EMPTY,
    60: Tile.ROBOT_FACING_LEFT,
    62: Tile.ROBOT_FACING_RIGHT,
    94: Tile.ROBOT_FACING_UP,
    118: Tile.ROBOT_FACING_DOWN,
}
TILE_TO_ASCII = {
    Tile.SCAFFOLD: "#",
    Tile.EMPTY: ".",
    Tile.ROBOT_FACING_DOWN: "v",
    Tile.ROBOT_FACING_LEFT: "<",
    Tile.ROBOT_FACING_UP: "^",
    Tile.ROBOT_FACING_RIGHT: ">",
}


class RobotInterface:
    """Camera and Robot Interface

    Aft Scaffolding Control and Information Interface
    (ASCII, your puzzle input), provides access to the
    cameras and the vacuum robot.
    """

    def __init__(self, program):
        self.cpu = IntCodeComputer(
            program, pause_on_output=False, memory_size=4096, propogate_exceptions=True
        )

    def run(self):
        """This grabs the screen output"""
        try:
            self.cpu.process()
        except Halt:
            return self.cpu.captured_output[:]

        raise ValueError("Unrreachable")


def screen_to_grid(screen):
    grid = []
    line = []
    for item in screen:
        tile = ASCII_TO_TILE[item]
        if tile == "\n":
            grid.append(line)
            line = []
        else:
            line.append(tile)
    grid.pop()  # remove empty row
    return grid


def draw_grid(grid):
    output = ""
    for line in grid:
        output += "".join([TILE_TO_ASCII[col] for col in line]) + "\n"
    return output[:-1]


def find_intersections(grid):
    intersections = []
    for y, row in enumerate(grid):
        for x, col in enumerate(row):
            if grid[y][x] == Tile.SCAFFOLD:
                if is_intersection(grid, (x, y)):
                    intersections.append((x, y))
    return intersections


def is_intersection(grid, point_to_check):
    x, y = point_to_check
    x_min = 0
    x_max = len(grid[0])
    y_min = 0
    y_max = len(grid)

    for x_delta, y_delta in [(+1, 0), (-1, 0), (0, -1), (0, +1)]:
        new_x = x + x_delta
        new_y = y + y_delta

        if x_min <= new_x < x_max and y_min <= new_y < y_max:
            if grid[new_y][new_x] != grid[y][x]:
                return False
        else:  # point is on the boundary
            return False

    return True


def calculate_alignment_parameters(intersections):
    alignment_parameters = 0
    for x, y in intersections:
        alignment_parameters += x * y
    return alignment_parameters


TEST_INPUT = """..#..........
..#..........
#######...###
#.#...#...#.#
#############
..#...#...#..
..#####...^.."""


def test_calculate_alignment_parameters():
    lines = TEST_INPUT.split("\n")
    grid = []
    for row in lines:
        line = []
        for item in row:
            line.append(ASCII_TO_TILE[ord(item)])
        grid.append(line)
    intersections = find_intersections(grid)
    alignment_parameters = calculate_alignment_parameters(intersections)
    assert alignment_parameters == 76


if __name__ == "__main__":
    with open("2019/data/day17_input.txt", "r") as f:
        intcode_program = f.readline().strip()

    robot = RobotInterface(intcode_program)
    screen = robot.run()
    grid = screen_to_grid(screen)
    intersections = find_intersections(grid)
    alignment_parameters = calculate_alignment_parameters(intersections)
    print(f"Sum of alignment parameters is {alignment_parameters}")
