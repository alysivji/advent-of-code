import copy
import itertools
import time
from typing import Iterator, NamedTuple


class GridPosition(NamedTuple):
    row: int
    col: int

    def add(self, row: int, col: int) -> "GridPosition":
        return GridPosition(row=self.row + row, col=self.col + col)


Tower = dict[GridPosition, str]


def simulate_tetris(jet_pattern_iterator, num_pieces_to_place: int) -> Tower:
    BLOCK_PATTERN = ["horizontal_line", "plus", "backwards_l", "vertical_line", "box"]
    blocks_iterator = itertools.cycle(BLOCK_PATTERN)

    board: Tower = {}
    # draw floor
    for i in range(7):
        board[GridPosition(0, i)] = "-"

    num_pieces_placed = 0
    while True:
        max_row = max(key.row for key in board)
        shape = generate_shape(next(blocks_iterator), max_row=max_row)
        board = process_falling_rock(board, jet_pattern_iterator, shape)
        num_pieces_placed += 1

        if num_pieces_placed == num_pieces_to_place:
            break

        # if num_pieces_placed % 1000 == 0:
        # print(num_pieces_placed)

    return board


def draw(board: Tower, shape: list[GridPosition]):
    output = ""
    board_to_draw = copy.deepcopy(board)
    for block in shape:
        board_to_draw[block] = "@"

    # import pdb; pdb.set_trace()
    max_row = max(key.row for key in board_to_draw)
    output = ""
    for row in range(max_row, -1, -1):
        output += "|"
        for col in range(0, 7):
            point = board_to_draw.get(GridPosition(row, col), ".")
            output += point
        output += "|\n"

    print(output)


def process_falling_rock(
    board: Tower,
    jet_pattern_iterator: Iterator[str],
    shape: list[GridPosition],
) -> Tower:
    while True:
        # can the block be moved by the jet of gas?
        wind_direction = next(jet_pattern_iterator)
        col = 0
        if wind_direction == ">":
            col = 1
        elif wind_direction == "<":
            col = -1
        else:
            raise ValueError("unexpected wind direction")

        new_shape = []
        for block in shape:
            new_block = block.add(row=0, col=col)
            new_shape.append(new_block)

        for block in new_shape:
            # hits wall
            if block.col < 0 or block.col > 6:
                break
            # hits another piece
            if block in board:
                break
        else:
            shape = new_shape

        # can the block fall a unit?
        new_shape = []
        for block in shape:
            new_block = block.add(row=-1, col=0)
            new_shape.append(new_block)

        block_falling = True
        for block in new_shape:
            if block in board:
                block_falling = False

        if block_falling:
            shape = new_shape
        else:
            for block in shape:
                board[block] = "#"
            break

    return board


def generate_shape(shape_type: str, max_row: int) -> list[GridPosition]:
    points = []
    if shape_type == "horizontal_line":
        for col in range(2, 6):
            points.append(GridPosition(row=max_row + 4, col=col))
    elif shape_type == "plus":
        points.append(GridPosition(row=max_row + 4, col=3))
        for col in range(2, 5):
            points.append(GridPosition(row=max_row + 5, col=col))
        points.append(GridPosition(row=max_row + 6, col=3))
    elif shape_type == "backwards_l":
        for col in range(2, 4):
            points.append(GridPosition(row=max_row + 4, col=col))
        for row in range(max_row + 4, max_row + 7):
            points.append(GridPosition(row=row, col=4))
    elif shape_type == "vertical_line":
        for row in range(max_row + 4, max_row + 8):
            points.append(GridPosition(row=row, col=2))
    elif shape_type == "box":
        for col in range(2, 4):
            points.append(GridPosition(row=max_row + 4, col=col))
        for col in range(2, 4):
            points.append(GridPosition(row=max_row + 5, col=col))
    else:
        raise ValueError("unexpected shape_type")

    return points


if __name__ == "__main__":
    # sample data
    TEST_PATTERN = ">>><<><>><<<>><>>><<<>>><<<><<<>><>><<>>"
    jet_pattern_iterator = itertools.cycle(TEST_PATTERN)

    start_time = time.time()
    board = simulate_tetris(jet_pattern_iterator, num_pieces_to_place=2022)
    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"Sample data execution time: {elapsed_time} seconds")

    max_row = max(key.row for key in board)
    assert max_row == 3068

    # real data
    with open("2022/data/day17_input.txt") as f:
        pattern = f.read().strip()
    PUZZLE_PATTERN = pattern
    jet_pattern_iterator = itertools.cycle(PUZZLE_PATTERN)

    start_time = time.time()
    board = simulate_tetris(jet_pattern_iterator, num_pieces_to_place=2022)
    end_time = time.time()
    elapsed_time = end_time - start_time
    max_row = max(key.row for key in board)
    print(f"Part 1: {max_row} | Execution time: {elapsed_time} seconds")
