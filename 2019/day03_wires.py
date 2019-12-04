from collections import defaultdict
from typing import List, NamedTuple, Set

import pytest


class Coordinate(NamedTuple):
    x: int
    y: int


class Segment(NamedTuple):
    direction: str
    distance: int


def convert_movement_to_list(path: str) -> List[Segment]:
    segments = path.strip().split(",")
    return [Segment(segment[0], int(segment[1:])) for segment in segments]


def trace_wire_on_grid(segments: List[Segment]) -> Set[Coordinate]:
    wire_path = set()
    current_coordinate = Coordinate(0, 0)  # start at (0, 0)

    for segment in segments:
        for idx in range(1, segment.distance + 1):
            if segment.direction == "U":
                direction = Coordinate(1, 0)
            elif segment.direction == "D":
                direction = Coordinate(-1, 0)
            elif segment.direction == "R":
                direction = Coordinate(0, 1)
            elif segment.direction == "L":
                direction = Coordinate(0, -1)
            new_x = current_coordinate.x + direction.x
            new_y = current_coordinate.y + direction.y
            current_coordinate = Coordinate(new_x, new_y)
            wire_path.add(current_coordinate)

    return wire_path


def find_manhattan_distance_to_closest_interesection(wire1_locations, wire2_locations):
    intersections = wire1_locations.intersection(wire2_locations)
    return min(abs(x) + abs(y) for x, y in intersections)


def find_closest_distance_given_wire_path(wire1_path, wire2_path):
    wire1_segements = convert_movement_to_list(wire1_path)
    wire1_locations = trace_wire_on_grid(wire1_segements)

    wire2_segments = convert_movement_to_list(wire2_path)
    wire2_locations = trace_wire_on_grid(wire2_segments)

    return find_manhattan_distance_to_closest_interesection(wire1_locations, wire2_locations)


@pytest.mark.parametrize("wire1_path, wire2_path, expected_distance", (
    ("R8,U5,L5,D3", "U7,R6,D4,L4", 6),
    ("R75,D30,R83,U83,L12,D49,R71,U7,L72", "U62,R66,U55,R34,D71,R55,D58,R83", 159),
    ("R98,U47,R26,D63,R33,U87,L62,D20,R33,U53,R51", "U98,R91,D20,R16,D67,R40,U7,R15,U6,R7", 135),
))
def test_find_closest_distance_given_wire_path(wire1_path, wire2_path, expected_distance):
    distance = find_closest_distance_given_wire_path(wire1_path, wire2_path)
    assert distance == expected_distance


if __name__ == "__main__":
    with open("2019/data/day03_input.txt") as f:
        wire1_path = f.readline()
        wire2_path = f.readline()

    distance = find_closest_distance_given_wire_path(wire1_path, wire2_path)
    print(f"Closest distance to interesction is: {distance}")
