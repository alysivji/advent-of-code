from collections import Counter
from enum import IntEnum
from typing import NamedTuple

import matplotlib.pyplot as plt

from utils import Halt, IntCodeComputer


class Tile(IntEnum):
    EMPTY = 0
    WALL = 1
    BLOCK = 2
    PADDLE = 3  # horizontal paddle
    BALL = 4


MATPLOTLIB_TILE_MAPPING = {
    Tile.EMPTY: "w",
    Tile.WALL: "r",
    Tile.BLOCK: "b",
    Tile.PADDLE: "g",
    Tile.BALL: "y",
}


class JoystickDirection(IntEnum):
    LEFT = -1  # tilt left
    NEUTRAL = 0
    RIGHT = 1  # tilt right


class DrawInstruction(NamedTuple):
    x: int
    y: int
    tile: int


class ArcadeCabinet:
    def __init__(self, program):
        self.cpu = IntCodeComputer(
            program,
            input_value=JoystickDirection.LEFT,
            pause_on_output=True,
            num_output_to_capture=3,
            memory_size=100_000,
            propogate_exceptions=True,
        )
        self.score = 0

    def __repr__(self):
        return "<ArcadeCabinet>"

    def insert_quarters(self):
        self.cpu.update_memory_address(position=0, value=2)

    def move_joystick(self, direction):
        for possible_direction in JoystickDirection:
            if dirrection == possible_direction:
                self.cpu.input_value = direction

    def execute(self):
        screen = {}
        ball_position = None
        paddle_position = None
        while True:
            try:
                self.cpu.process()
            except Halt:
                break

            output = DrawInstruction(*self.cpu.captured_output)
            if output.x == -1 and output.y == 0:
                self.score = output.tile
            else:
                screen[(output.x, output.y)] = output.tile

            # get position of sprites we care about
            if output.tile == Tile.BALL:
                ball_position = (output.x, output.y)
            elif output.tile == Tile.PADDLE:
                paddle_position = (output.x, output.y)

            # have paddle follow ball
            if ball_position is not None and paddle_position is not None:
                if ball_position[0] > paddle_position[0]:
                    self.cpu.input_value = JoystickDirection.RIGHT
                elif ball_position[0] == paddle_position[0]:
                    self.cpu.input_value = JoystickDirection.NEUTRAL
                elif ball_position[0] < paddle_position[0]:
                    self.cpu.input_value = JoystickDirection.LEFT

        return screen


def count_tiles(screen, tile_type):
    counter = Counter()
    for position, tile in screen.items():
        counter.update([tile])

    return counter[tile_type]


def draw(screen):
    xs = []
    ys = []
    values = []
    for position, tile in screen.items():
        plt.scatter(position[0], position[1], c=MATPLOTLIB_TILE_MAPPING[tile])
    plt.show()


if __name__ == "__main__":
    with open("2019/data/day13_input.txt", "r") as f:
        intcode_program = f.readline().strip()

    arcade = ArcadeCabinet(intcode_program)
    screen = arcade.execute()
    num_blocks = count_tiles(screen, Tile.BLOCK)
    print(f"Number of blocks is: {num_blocks}")
    assert num_blocks == 315

    arcade = ArcadeCabinet(intcode_program)
    arcade.insert_quarters()
    screen = arcade.execute()
    print(f"Score is: {arcade.score}")
