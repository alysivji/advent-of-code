from dataclasses import dataclass
from typing import List, NamedTuple

import pytest


class Schedule(NamedTuple):
    timestamp: int
    buses: List[int]


@dataclass
class Bus:
    period: int
    offset: int
    time: int = 0

    @property
    def time_without_offset(self):
        return self.time - self.offset

    def __next__(self):
        self.time += self.period
        while True:
            return self.time


def parse_bus_schedule(lines):
    timestamp, to_process = lines
    active_buses = [
        int(value) for value in to_process.strip().split(",") if value != "x"
    ]
    return Schedule(int(timestamp), active_buses)


def next_bus(buses, timestamp):
    time_to_wait = []
    for bus in buses:
        num_trips = timestamp // bus
        last_bus = num_trips * bus
        time_to_wait.append(last_bus + bus - timestamp)

    time_to_wait_for_next_bus = min(time_to_wait)
    bus_number = buses[time_to_wait.index(time_to_wait_for_next_bus)]
    return time_to_wait_for_next_bus * bus_number


def test_find_next_bus():
    TEST_INPUT = """939
    7,13,x,x,59,x,31,19"""
    schedule = parse_bus_schedule(TEST_INPUT.split("\n"))

    assert next_bus(schedule.buses, schedule.timestamp) == 295


def parse_bus_and_offsets(businfo):
    buses = []
    for idx, period in enumerate(businfo.split(",")):
        if period == "x":
            continue
        bus = Bus(int(period), idx)
        next(bus)
        buses.append(bus)
    return buses


def part_2(schedule: List[Bus]):
    while True:
        time_without_offset = [bus.time_without_offset for bus in schedule]
        differences = [item == time_without_offset[0] for item in time_without_offset]
        if all(differences):
            return time_without_offset[0]

        # take the lowest one that isn't the first element
        min_bus = min(time_without_offset)
        idx = time_without_offset.index(min_bus)

        bus_to_increment = schedule[idx]
        next(bus_to_increment)


@pytest.mark.parametrize(
    "input_str,timestamp",
    [
        ("7,13,x,x,59,x,31,19", 1068781),
        ("17,x,13,19", 3417),
        ("67,7,59,61", 754018),
        ("67,x,7,59,61", 779210),
        ("67,7,x,59,61", 1261476),
        ("1789,37,47,1889", 1202161486),
    ],
)
def test_find_timestamp(input_str, timestamp):
    schedule = parse_bus_and_offsets(input_str)
    result = part_2(schedule)
    assert result == timestamp


if __name__ == "__main__":
    with open("2020/data/day13_input.txt") as f:
        schedule = parse_bus_schedule(f.readlines())

    print(f"Part 1 is {next_bus(schedule.buses, schedule.timestamp)}")
