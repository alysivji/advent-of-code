import functools
from typing import List, Set

import pytest


def device_joltage_adapter(adapters: List[int]):
    return max(adapters) + 3


@pytest.fixture
def few_adapters():
    TEST_ADAPTERS = """16
    10
    15
    5
    1
    11
    7
    19
    6
    12
    4"""

    return [int(rating) for rating in TEST_ADAPTERS.split("\n")]

# @pytest.fixture
def more_adapters():
    TEST_ADAPTERS = """28
    33
    18
    42
    31
    14
    46
    20
    48
    47
    24
    23
    49
    45
    19
    38
    39
    11
    1
    32
    25
    35
    8
    17
    7
    9
    4
    2
    34
    10
    3"""

    return [int(rating) for rating in TEST_ADAPTERS.split("\n")]

def test_device_joltage_adapter(few_adapters):
    assert device_joltage_adapter(few_adapters) == 22


def use_all_adapters(adapters: List[int]):
    adapters_left = set(adapters)
    adapters_left.add(device_joltage_adapter(adapters_left))
    adapters_left.add(0)  # charging outlet

    difference_of_1 = 0
    difference_of_3 = 0
    while len(adapters_left) > 1:
        current_adapter = min(adapters_left)
        adapters_left.remove(current_adapter)
        next_adapter = min(adapters_left)

        difference = next_adapter - current_adapter
        if difference == 1:
            difference_of_1 += 1
        elif difference == 3:
            difference_of_3 += 1
        else:
            raise ValueError

    return (difference_of_1, difference_of_3)


def test_use_all_adapters_1(few_adapters):
    difference_of_1, difference_of_3 = use_all_adapters(few_adapters)
    assert difference_of_1 * difference_of_3 == 35


def test_use_all_adapters_2(more_adapters):
    difference_of_1, difference_of_3 = use_all_adapters(more_adapters)
    assert difference_of_1 * difference_of_3 == 22 * 10


@functools.lru_cache()
def count_adapter_paths(adapters_str: str, current_adapter: int):
    adapters = [int(value) for value in adapters_str.split(",")]
    max_adapters = max(adapters)
    if current_adapter == max_adapters:
        return 1

    paths = 0
    if current_adapter + 1 in adapters:
        paths += count_adapter_paths(adapters_str, current_adapter + 1)
    if current_adapter + 2 in adapters:
        paths += count_adapter_paths(adapters_str, current_adapter + 2)
    if current_adapter + 3 in adapters:
        paths += count_adapter_paths(adapters_str, current_adapter + 3)

    return paths


def test_count_adapter_paths(few_adapters, more_adapters):
    assert count_adapter_paths(few_adapters, current_adapter=0) == 8
    assert count_adapter_paths(more_adapters, current_adapter=0) == 19208


if __name__ == "__main__":
    with open("2020/data/day10_input.txt") as f:
        adapters = [int(rating) for rating in f.readlines()]

    difference_of_1, difference_of_3 = use_all_adapters(adapters)
    print(difference_of_1 * difference_of_3)

    adapters_str = ",".join(str(value) for value in adapters)
    print(count_adapter_paths(adapters_str, current_adapter=0))
