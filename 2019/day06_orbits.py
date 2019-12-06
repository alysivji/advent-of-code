from collections import defaultdict, deque
import re
from typing import List, NamedTuple, Tuple


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
    orbits: dict
    reverse: dict
    graph: dict


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
    all_planets = set()
    orbit_tracker = defaultdict(list)  # parent is key, children are in list
    reverse_orbit = defaultdict(list)  # child is key, parent is value
    graph = defaultdict(list)  # graph

    for orbit in orbits:
        orbit_tracker[orbit.inner].append(orbit.outer)
        reverse_orbit[orbit.outer].append(orbit.inner)

        graph[orbit.inner].append(orbit.outer)
        graph[orbit.outer].append(orbit.inner)

    root_planet = graph.keys() - reverse_orbit.keys()
    return Map(
        root_planet.pop(), orbits=orbit_tracker, reverse=reverse_orbit, graph=graph
    )


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


def shortest_path(graph: dict, start: str, end: str) -> Tuple[List, int]:
    planet_queue = deque()
    visited = set([start])
    neighbours = [(planet, 1) for planet in graph[start]]
    planet_queue.extend(neighbours)

    while planet_queue:
        current_planet, distance = planet_queue.popleft()

        if current_planet in visited:
            continue
        visited.add(current_planet)

        if current_planet == end:
            return distance

        neighbours = graph[current_planet]
        distance += 1
        planet_queue.extend([(planet, distance) for planet in neighbours])

    raise ValueError("Did not converge")


def test_shortest_path():
    orbits = load_orbits(TEST_INPUT.strip().split("\n"))
    orbit_map = build_orbit_map(orbits)
    graph = orbit_map.graph
    result = shortest_path(graph, "K", "I")
    assert result == 4


if __name__ == "__main__":
    with open("2019/data/day06_input.txt") as f:
        lines = f.readlines()
    orbits = load_orbits(lines)
    orbits_map = build_orbit_map(orbits)
    total_orbits = total_direct_and_indirect_orbits(orbits_map)

    start = orbits_map.reverse["YOU"][0]
    end = orbits_map.reverse["SAN"][0]

    shortest_distance = shortest_path(orbits_map.graph, start=start, end=end)

    print(f"Total orbits: {total_orbits}")
    print(f"Shortest distance: {shortest_distance}")
