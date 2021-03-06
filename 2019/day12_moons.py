from collections import defaultdict
import functools
import itertools
import math
import re
from typing import Dict, List, NamedTuple

import pytest

POSITIONS = r"<x=(?P<x>-*\d+), y=(?P<y>-*\d+), z=(?P<z>-*\d+)>"


def lcm(denominators):
    """https://stackoverflow.com/a/49816058/4326704"""
    return functools.reduce(lambda a,b: a*b // math.gcd(a,b), denominators)


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


class State:
    def __init__(self):
        self._state = {}

    def __getitem__(self, key):
        return self._state[key]

    def __setitem__(self, key, value):
        self._state[key] = value

    def __iter__(self):
        return iter(self._state)

    def __repr__(self):
        return repr(self._state)

    def items(self):
        return self._state.items()

    def keys(self):
        return self._state.keys()

    @classmethod
    def from_moons(cls, moons: List[Moon]):
        self = cls()
        for index, moon_details in enumerate(moons):
            self[index] = moon_details
        return self


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


def simulate(initial_state: State, num_timesteps: int) -> State:
    """Given initial state, increment by timesteps, return state"""
    step = 0
    current_state = initial_state
    while True:
        motion_tracker = {key: Position(x=0, y=0, z=0) for key in current_state.keys()}
        for m1, m2 in itertools.combinations(current_state.keys(), r=2):
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

        step += 1
        if step >= num_timesteps:
            break

    return current_state


def calculate_energy(current_state: State) -> int:
    total_energy = 0
    for key, state_details in current_state.items():
        potential_energy = sum(abs(val) for val in list(state_details.position))
        kinect_energy = sum(abs(val) for val in list(state_details.velocity))
        total_energy += potential_energy * kinect_energy

    return total_energy


def find_orbit_pattern(initial_state: State):
    current_state = initial_state
    timestep = 0

    seen_xs = set()
    seen_ys = set()
    seen_zs = set()

    while True:
        timestep += 1
        current_state = simulate(current_state, num_timesteps=1)

        x = []
        y = []
        z = []
        for key in current_state.keys():
            pos = current_state[key].position
            vel = current_state[key].velocity
            x.extend([key, pos.x, vel.x])
            y.extend([key, pos.y, vel.y])
            z.extend([key, pos.z, vel.z])

        x = tuple(x)
        y = tuple(y)
        z = tuple(z)
        if x in seen_xs and y in seen_ys and z in seen_zs:
            return (len(seen_xs), len(seen_ys), len(seen_zs))

        seen_xs.add(x)
        seen_ys.add(y)
        seen_zs.add(z)


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
    [(TEST_INPUT1, 10, 179), (TEST_INPUT2, 100, 1940)],
)
def test_calculate_total_energy(positions, timesteps, expected_total_energy):
    moons = load_positions(positions.split("\n"))
    initial_state = State.from_moons(moons)
    final_state = simulate(initial_state, num_timesteps=timesteps)
    assert calculate_energy(final_state) == expected_total_energy


@pytest.mark.parametrize(
    "positions, expected_timesteps", [(TEST_INPUT2, 4686774924)]
)
def test_timesteps_before_repeat(positions, expected_timesteps):
    moons = load_positions(positions.split("\n"))
    initial_state = State.from_moons(moons)

    periodic_orbit = find_orbit_pattern(initial_state)
    assert lcm(periodic_orbit) == expected_timesteps


if __name__ == "__main__":
    lines = []
    with open("2019/data/day12_input.txt", "r") as f:
        for line in f.readlines():
            lines.append(line.strip())

    moons = load_positions(lines)
    initial_state = State.from_moons(moons)
    final_state = simulate(initial_state, num_timesteps=1000)
    energy = calculate_energy(final_state)
    print(f"Total energy in the system is: {energy}")

    initial_state = State.from_moons(moons)
    periodic_orbit = find_orbit_pattern(initial_state)
    timesteps = lcm(periodic_orbit)
    print(f"Num timesteps before repeating is: {timesteps}")
