from collections import defaultdict, deque
from enum import IntEnum
from typing import NamedTuple

import matplotlib.pyplot as plt

from utils import Halt, IntCodeComputer


class Move(IntEnum):
    NORTH = 1
    SOUTH = 2
    WEST = 3
    EAST = 4


class StatusCode(IntEnum):
    WALL = 0  # position has not changed
    MOVED = 1  # moved one step in the requested direction
    FOUND = 2  # moved one step in the requested direction and found system


class Tile(IntEnum):
    WALL = 0
    EMPTY  = 1
    OXYGEN_SYSTEM = 2


class XY(NamedTuple):
    x: int
    y: int

    def __add__(self, other):
        return XY(x=self.x + other.x, y=self.y + other.y)

    def __sub__(self, other):
        return XY(x=self.x - other.x, y=self.y - other.y)


move_to_xy = {
    Move.NORTH: XY(0, +1),
    Move.SOUTH: XY(0, -1),
    Move.EAST: XY(+1, 0),
    Move.WEST: XY(-1, 0),
}
reverse_move = {
    Move.NORTH: Move.SOUTH,
    Move.SOUTH: Move.NORTH,
    Move.EAST: Move.WEST,
    Move.WEST: Move.EAST,
}
tile_to_char = {
    Tile.WALL: "b",
    Tile.EMPTY: "w",
    Tile.OXYGEN_SYSTEM: "y",
}


class RepairDroid:
    def __init__(self, program: str):
        self.cpu = IntCodeComputer(
            program,
            pause_on_output=True,
            num_output_to_capture=1,
            memory_size=100_000,
            propogate_exceptions=True,
        )
        self.program = self.cpu.program

    def __repr__(self):
        return "<RepairDroid>"

    def map_out_floor_plan(self):
        floor_plan = {}
        path = []
        frontier = deque()

        initial_position = XY(0, 0)
        frontier.append((0, self.cpu.export_state(), initial_position))
        floor_plan[initial_position] = Tile.EMPTY

        while frontier:
            num_steps, state, curr_position = frontier.popleft()
            self.cpu.import_state(state)

            for movement_command, xy_delta in move_to_xy.items():
                xy_to_search = curr_position + xy_delta
                if xy_to_search in floor_plan:
                    continue

                status_code = self._run(movement_command.value)[0]
                if status_code == StatusCode.WALL:
                    floor_plan[xy_to_search] = Tile.WALL
                    continue

                if status_code == StatusCode.MOVED:
                    floor_plan[xy_to_search] = Tile.EMPTY
                elif status_code == StatusCode.FOUND:
                    floor_plan[xy_to_search] = Tile.OXYGEN_SYSTEM
                next_state = self.cpu.export_state()
                frontier.append((num_steps + 1, next_state, xy_to_search))
                self._run(reverse_move[movement_command])

        return floor_plan

    def _run(self, movement_command):
        self.cpu.input_value = movement_command

        while True:
            try:
                self.cpu.process()
            except Halt:
                break

            return self.cpu.captured_output
        raise ValueError("Unreachable. Program should loop forever")


def draw(floor_plan):
    xs = []
    ys = []
    values = []
    for position, tile in floor_plan.items():
        plt.scatter(position[0], position[1], c=tile_to_char[tile])
    plt.scatter(0, 0, c='r')
    plt.show()


def floor_plan_to_graph(floor_plan):
    graph = defaultdict(list)

    for position, tile in floor_plan.items():
        if tile == Tile.WALL:
            continue

        for xy_delta in move_to_xy.values():
            new_position = position + xy_delta
            if floor_plan[new_position] != Tile.WALL:
                graph[position].append(new_position)
                graph[new_position].append(position)
    return graph

def locate_oxygen_system(floor_plan):
    for position, tile in floor_plan.items():
        if tile == Tile.OXYGEN_SYSTEM:
            return position
    raise ValueError("Did not find oxygen system... did you submit a valid floor plan?")


def steps_to_goal(graph, end, start=XY(0, 0)) -> int:
    path = []
    seen = set()
    frontier = deque()
    frontier.append((0, start))

    while frontier:
        num_steps, curr_position = frontier.popleft()
        if curr_position == end:
            return num_steps

        for movement_command, xy_delta in move_to_xy.items():
            xy_to_search = curr_position + xy_delta

            if xy_to_search not in graph or xy_to_search in seen:
                continue

            seen.add((xy_to_search))
            frontier.append((num_steps + 1, xy_to_search))

    raise ValueError("Goal not found")


def max_depth_from_location(graph, location):
    max_depth = 0
    seen = set()
    frontier = [(0, location)]

    while frontier:
        current_depth, position = frontier.pop()
        seen.add(position)
        if current_depth > max_depth:
            max_depth = current_depth

        for neighbour in graph[position]:
            if neighbour not in seen:
                frontier.append((current_depth + 1, neighbour))

    return max_depth


if __name__ == "__main__":
    with open("2019/data/day15_input.txt", "r") as f:
        intcode_program = f.readline().strip()

    robot = RepairDroid(intcode_program)
    floor_plan = robot.map_out_floor_plan()
    g = floor_plan_to_graph(floor_plan)

    oxygen_system_position = locate_oxygen_system(floor_plan)
    steps = steps_to_goal(g, oxygen_system_position, start=XY(0, 0))
    print(f"Number of steps until the robot finds the oxygen system: {steps}")

    robot = RepairDroid(intcode_program)
    floor_plan = robot.map_out_floor_plan()
    g = floor_plan_to_graph(floor_plan)
    max_depth = max_depth_from_location(g, oxygen_system_position)
    print(f"Number of seconds for oxygen to fill: {max_depth}")
