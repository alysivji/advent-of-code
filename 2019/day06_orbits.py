from collections import defaultdict, deque
import re
from typing import List, NamedTuple


ORBIT = r"(?P<inner>[\w\d]+)\)(?P<outer>[\w\d]+)"

TEST_INPUT = """COM)B
B)C
C)D
D)E
E)F
B)G
G)H
D)I
E)J
J)K
K)L
"""


class Orbit(NamedTuple):
    inner: str
    outer: str


class Map(NamedTuple):
    center: str
    orbits: list


def load_orbits(lines: List[str]) -> List[Orbit]:
    p = re.compile(ORBIT)
    orbits = []
    for idx, line in enumerate(lines):
        cleaned_line = line.strip()
        m = p.match(cleaned_line)
        orbit = Orbit(inner=m.group("inner"), outer=m.group("outer"))
        orbits.append(orbit)
    return orbits


def build_orbit_map(orbits: List[Orbit]) -> Map:
    """Give a list of orbits, return root planet"""
    all_planets = set()
    orbit_tracker = defaultdict(list)  # parent is key, children are in list
    reverse_orbit = defaultdict(list)  # child is key, parent is value

    for orbit in orbits:
        all_planets.add(orbit.inner)
        all_planets.add(orbit.outer)
        orbit_tracker[orbit.inner].append(orbit.outer)
        reverse_orbit[orbit.outer].append(orbit.inner)

    root_planet = all_planets - reverse_orbit.keys()
    return Map(root_planet.pop(), orbit_tracker)


def total_direct_and_indirect_orbits(orbit_map: Map) -> int:
    num_orbits = {}
    planets_queue = deque()
    planets_queue.append((orbit_map.center, -1))

    while planets_queue:
        current_planet, num_indirect_orbits = planets_queue.popleft()

        number_of_direct_and_indirect_orbits = num_indirect_orbits + 1
        num_orbits[current_planet] = number_of_direct_and_indirect_orbits

        new_planets_to_process = [
            (planet, number_of_direct_and_indirect_orbits)
            for planet in orbit_map.orbits[current_planet]
        ]
        planets_queue.extend(new_planets_to_process)

    return sum(num_orbits.values())


def test_total_direct_and_indirect_orbits():
    orbits = load_orbits(TEST_INPUT.strip().split("\n"))
    orbit_map = build_orbit_map(orbits)
    assert total_direct_and_indirect_orbits(orbit_map) == 42


if __name__ == "__main__":
    with open("2019/data/day06_input.txt") as f:
        lines = f.readlines()
    orbits = load_orbits(lines)
    orbits_map = build_orbit_map(orbits)
    total_orbits = total_direct_and_indirect_orbits(orbits_map)

    print(f"Total orbits: {total_orbits}")
