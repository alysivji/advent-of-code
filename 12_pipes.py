"""Advent of Code -- Day 12

http://adventofcode.com/2017/day/12"""

# from collections import defaultdict
from typing import Dict, List

TEST_DATA = """0 <-> 2
1 <-> 1
2 <-> 0, 3, 4
3 <-> 2, 4
4 <-> 2, 3, 6
5 <-> 6
6 <-> 4, 5"""


def map_connections(connections: List[str]) -> Dict[int, List]:
    pipes = dict()

    for connection in connections:
        origin, neighbours = connection.split(' <-> ')
        pipes[int(origin)] = [int(item) for item in neighbours.split(',')]

    return pipes


def get_neighbours(connections_map: Dict[int, List], center: str) -> set:
    neighbours = set()

    # add first element to search space
    search_stack = []
    search_stack.append(center)

    while search_stack:
        new_group_member = search_stack.pop()
        neighbours.add(new_group_member)
        direct_connections = connections_map[new_group_member]

        for neighbour in direct_connections:
            if neighbour not in neighbours:
                search_stack.append(neighbour)

    return neighbours


def find_groups(connections_map: Dict[int, List]) -> int:
    connections_copy = dict(connections_map)
    groups = []

    # loop thru dict items until none are left
    while connections_copy:
        key, value = connections_copy.popitem()
        group_members = get_neighbours(connections_map, key)

        groups.append(list(group_members))
        for group in group_members:
            if group in connections_copy:
                del connections_copy[group]

    return groups


if __name__ == "__main__":
    connections = TEST_DATA.splitlines()
    connections_map = map_connections(connections)
    result = get_neighbours(connections_map, 0)
    groups = find_groups(connections_map)

    assert len(result) == 6
    assert len(groups) == 2

    with open('12_input.txt', 'r')  as f:
        connections_map = map_connections(f.readlines())

    result = get_neighbours(connections_map, 0)
    groups = find_groups(connections_map)
