from collections import Counter
from enum import IntEnum
from typing import NamedTuple

from utils import Halt, IntCodeComputer


class Tile(IntEnum):
    EMPTY = 0
    WALL = 1
    BLOCK = 2
    PADDLE = 3  # horizontal paddle
    BALL = 4


class DrawInstruction(NamedTuple):
    x: int
    y: int
    tile: int


class ArcadeCabinet:
    def __init__(self, program):
        self.cpu = IntCodeComputer(
            program,
            pause_on_output=True,
            num_output_to_capture=3,
            memory_size=100_000,
            propogate_exceptions=True,
        )

    def __repr__(self):
        return "<ArcadeCabinet>"

    def process(self):
        screen = {}
        while True:
            try:
                self.cpu.process()
            except Halt:
                break

            output = DrawInstruction(*self.cpu.captured_output)
            screen[(output.x, output.y)] = output.tile

        return screen


def count_tiles(screen, tile_type):
    counter = Counter()
    for position, tile in screen.items():
        counter.update([tile])

    return counter[tile_type]


if __name__ == "__main__":
    with open("2019/data/day13_input.txt", "r") as f:
        intcode_program = f.readline().strip()

    arcade = ArcadeCabinet(intcode_program)
    screen = arcade.process()
    num_blocks = count_tiles(screen, Tile.BLOCK)
    print(f"Number of blocks is: {num_blocks}")


# TODO be able to reach into intCodeComputer
# to change memory addresses of program

# figure out how score changes by time
