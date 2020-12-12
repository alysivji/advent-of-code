from typing import List, NamedTuple

DIRECTION_MAPPING = {"N": 0, "E": 90, "S": 180, "W": 270}
DEGREE_MAPING = {value: key for key, value in DIRECTION_MAPPING.items()}


class Action(NamedTuple):
    type: str
    value: int


class Ship:
    def __init__(self, initial_direction):
        self.direction = DIRECTION_MAPPING[initial_direction]
        self.north_south = 0
        self.east_west = 0

    def __repr__(self):
        return f"Ship(NS={self.north_south},EW={self.east_west})"

    def perform_actions(self, actions: List[Action]):
        for action in actions:
            self.move(action.type, action.value)

    def move(self, action, value):
        if action == "N":
            self.north_south += value
        elif action == "S":
            self.north_south -= value
        elif action == "E":
            self.east_west += value
        elif action == "W":
            self.east_west -= value
        elif action == "L":
            self.direction = (self.direction - value) % 360
        elif action == "R":
            self.direction = (self.direction + value) % 360
        elif action == "F":
            direction = DEGREE_MAPING[self.direction]
            self.move(direction, value)
        else:
            raise ValueError("should not get here")

    @property
    def manhattan_distance(self):
        return abs(self.north_south) + abs(self.east_west)


TEST_INPUT = """F10
N3
F7
R90
F11"""


def test_ship_part_1():
    ship = Ship("E")
    actions = [Action(value[:1], int(value[1:])) for value in TEST_INPUT.split("\n")]
    ship.perform_actions(actions)

    assert ship.manhattan_distance == 25


class Waypoint:
    def __init__(self, east_offset, north_offset, ship):
        self.north_south = north_offset
        self.east_west = east_offset
        self.ship = ship

    def __repr__(self):
        return f"Waypoint(NS={self.north_south},EW={self.east_west})"

    def perform_actions(self, actions: List[Action]):
        for action in actions:
            self.move(action.type, action.value)

    def move(self, action, value):
        if action == "N":
            self.north_south += value
        elif action == "S":
            self.north_south -= value
        elif action == "E":
            self.east_west += value
        elif action == "W":
            self.east_west -= value
        elif action == "L" or action == "R":
            if action == "L":
                degrees = value
            else:
                degrees = 360 - value
            if degrees == 90:
                self.north_south, self.east_west = self.east_west, -self.north_south
            elif degrees == 180:
                self.north_south, self.east_west = -self.north_south, -self.east_west
            elif degrees == 270:
                self.north_south, self.east_west = -self.east_west, self.north_south
            else:
                raise ValueError("cannot be here")
        elif action == "F":
            self.ship.move("N", value * self.north_south)
            self.ship.move("E", value * self.east_west)
        else:
            raise ValueError("should not get here")

    @property
    def manhattan_distance(self):
        return abs(self.north_south) + abs(self.east_west)


def test_ship_part_2():
    ship = Ship("E")
    waypoint = Waypoint(10, 1, ship=ship)
    actions = [Action(value[:1], int(value[1:])) for value in TEST_INPUT.split("\n")]
    waypoint.perform_actions(actions)

    assert ship.manhattan_distance == 286



if __name__ == "__main__":
    with open("2020/data/day12_input.txt") as f:
        actions = [Action(value[:1], int(value[1:])) for value in f.readlines()]

    ship = Ship("E")
    ship.perform_actions(actions)
    print(f"Part 1 answer is {ship.manhattan_distance}")

    ship = Ship("E")
    waypoint = Waypoint(10, 1, ship=ship)
    waypoint.perform_actions(actions)
    print(f"Part 2 answer is {ship.manhattan_distance}")
