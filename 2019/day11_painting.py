from collections import defaultdict
from enum import IntEnum
from typing import NamedTuple

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
    def __init__(self, program):
        self.cpu = IntCodeComputer(
            program, input_value=0, pause_on_output=True, memory_size=1024, propogate_exceptions=True
        )

    def __repr__(self):
        return "<HullPaintingRobot>"

    def process(self):
        panels = defaultdict(int)
        panels_colored = 0
        curr_position = Position(0, 0)
        direction = "^"
        while True:
            captured_output = []
            try:
                while len(captured_output) < 2:
                    self.cpu.process()
                    captured_output.extend(self.cpu.captured_output)
            except Halt:
                break

            output = HullPaintingRobotOutput(*captured_output)
            old_color = panels[curr_position]
            panels[curr_position] = output.color
            if panels[curr_position] != old_color:
                panels_colored += 1
            direction = direction_mapper[output.direction][direction]
            curr_position += advance_direction[direction]
            self.cpu.set_input_value(panels[curr_position])

        return panels


if __name__ == "__main__":
    with open("2019/data/day11_input.txt", "r") as f:
        intcode_program = f.readline().strip()

    robot = HullPaintingRobot(intcode_program)
    result = robot.process()
    num_panels_painted = len(result)

    print(f"Painted {num_panels_painted} panels at least once.")
