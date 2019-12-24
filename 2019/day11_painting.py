from collections import defaultdict
from enum import IntEnum
from typing import NamedTuple

import matplotlib.pyplot as plt

from utils import Halt, IntCodeComputer


class Panel(IntEnum):
    BLACK = 0
    WHITE = 1


class HullPaintingRobotOutput(NamedTuple):
    color: int
    direction: int


class Position(NamedTuple):
    x: int
    y: int

    def __add__(self, other):
        return Position(self.x + other.x, self.y + other.y)


left_mapper = {"^": "<", "<": "V", "V": ">", ">": "^"}
right_mapper = {"^": ">", ">": "V", "V": "<", "<": "^"}
direction_mapper = {0: left_mapper, 1: right_mapper}
advance_direction = {
    "^": Position(0, 1),
    "<": Position(-1, 0),
    "V": Position(0, -1),
    ">": Position(1, 0),
}


class HullPaintingRobot:
    def __init__(self, program, input_value):
        self.cpu = IntCodeComputer(
            program,
            input_value=input_value,
            pause_on_output=True,
            num_output_to_capture=2,
            memory_size=1024,
            propogate_exceptions=True,
        )

    def __repr__(self):
        return "<HullPaintingRobot>"

    def process(self):
        panels = defaultdict(int)
        panels_colored = 0
        curr_position = Position(0, 0)
        direction = "^"
        while True:
            try:
                self.cpu.process()
            except Halt:
                break

            output = HullPaintingRobotOutput(*self.cpu.captured_output)
            old_color = panels[curr_position]
            panels[curr_position] = output.color
            if panels[curr_position] != old_color:
                panels_colored += 1
            direction = direction_mapper[output.direction][direction]
            curr_position += advance_direction[direction]
            self.cpu.input_value = panels[curr_position]

        return panels

def draw(positions):
    points = []
    for position, color in positions.items():
        if color == Panel.WHITE:
            points.append(position)

    xs = [point.x for point in points]
    ys = [point.y for point in points]
    plt.scatter(xs, ys, s=10)
    plt.show()


if __name__ == "__main__":
    with open("2019/data/day11_input.txt", "r") as f:
        intcode_program = f.readline().strip()

    robot = HullPaintingRobot(intcode_program, input_value=Panel.BLACK)
    paint_job = robot.process()
    num_panels_painted = len(paint_job)
    print(f"Painted {num_panels_painted} panels at least once.")

    robot = HullPaintingRobot(intcode_program, input_value=Panel.WHITE)
    paint_job = robot.process()
    draw(paint_job)
