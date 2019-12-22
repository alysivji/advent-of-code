from collections import defaultdict
import itertools
import re
from typing import Dict, List, NamedTuple

import pytest

POSITIONS = r"<x=(?P<x>-*\d+), y=(?P<y>-*\d+), z=(?P<z>-*\d+)>"


class Position(NamedTuple):
    x: int
    y: int
    z: int

    def __add__(self, other):
        return Position(x=self.x + other.x, y=self.y + other.y, z=self.z + other.z)

    def __sub__(self, other):
        return Position(x=self.x - other.x, y=self.y - other.y, z=self.z - other.z)

    def __iadd_(self, other):
        return self + other

    def __isub__(self, other):
        return self - other

    def __mul__(self, other):
        if isinstance(other, int):
            result = []
            for value in list(self):
                result.append(value * other)
            return Position(*result)
        raise NotImplementedError("unreachable")

    def __rmul__(self, other):
        return self * other

    def motion_due_to_gravity(self, other):
        """Compare two planets, find out how they move with respect to each other"""

        result = []
        for value, other_value in zip(list(self), list(other)):
            if value == other_value:
                result.append(0)
            elif value > other_value:
                result.append(-1)
            elif value < other_value:
                result.append(1)
            else:
                raise ValueError("unrreachable")

        return Vector(*result)


Vector = Position  # TODO make this an actual different type


class Moon(NamedTuple):
    position: Position
    velocity: Vector


def load_positions(lines: List[str]) -> List[Moon]:
    """TODO abstract this into a generator"""
    p = re.compile(POSITIONS)
    moons = []
    for idx, line in enumerate(lines):
        cleaned_line = line.strip()
        m = p.match(cleaned_line)
        pos = Position(x=int(m.group("x")), y=int(m.group("y")), z=int(m.group("z")))
        vel = Vector(x=0, y=0, z=0)
        moons.append(Moon(position=pos, velocity=vel))
    return moons


def progress_time(initial_state: List[Moon], timesteps: int) -> List[Moon]:
    current_state = {index: moon for index, moon in enumerate(initial_state)}

    for timestep in range(1, timesteps + 1):
        motion_tracker = {key: Position(x=0, y=0, z=0) for key in current_state.keys()}
        for m1, m2 in itertools.combinations(current_state, r=2):
            moon1 = current_state[m1].position
            moon2 = current_state[m2].position

            gravity_delta = moon1.motion_due_to_gravity(moon2)
            motion_tracker[m1] += gravity_delta
            motion_tracker[m2] -= gravity_delta

        for key in motion_tracker.keys():
            motion_tracker[key] += current_state[key].velocity

        for key in current_state.keys():
            new_velocity = motion_tracker[key] * 1  # creates a copy
            new_position = current_state[key].position + motion_tracker[key]
            current_state[key] = Moon(position=new_position, velocity=new_velocity)

    return current_state


def calculate_energy(current_state: Dict[int, Moon]) -> int:
    total_energy = 0
    for key, state_details in current_state.items():
        potential_energy = sum(abs(val) for val in list(state_details.position))
        kinect_energy = sum(abs(val) for val in list(state_details.velocity))
        total_energy += potential_energy * kinect_energy

    return total_energy


TEST_INPUT1 = """<x=-1, y=0, z=2>
<x=2, y=-10, z=-7>
<x=4, y=-8, z=8>
<x=3, y=5, z=-1>"""

TEST_INPUT2 = """<x=-8, y=-10, z=0>
<x=5, y=5, z=10>
<x=2, y=-7, z=3>
<x=9, y=-8, z=-3>"""


@pytest.mark.parametrize(
    "positions, timesteps, expected_total_energy",
    [
        (TEST_INPUT1, 10, 179),
        (TEST_INPUT2, 100, 1940),
    ],
)
def test_calculate_total_energy(positions, timesteps, expected_total_energy):
    moons = load_positions(positions.split("\n"))
    state = progress_time(moons, timesteps=timesteps)
    assert calculate_energy(state) == expected_total_energy



if __name__ == "__main__":
    lines = []
    with open("2019/data/day12_input.txt", "r") as f:
        for line in f.readlines():
            lines.append(line.strip())

    moons = load_positions(lines)
    state = progress_time(moons, timesteps=1000)
    energy = calculate_energy(state)
    print(f"Total energy in the system is: {energy}")
