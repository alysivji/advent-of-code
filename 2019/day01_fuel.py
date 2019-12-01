import math
from typing import List


def fuel_required_per_module(mass: int) -> int:
    return math.floor(mass / 3) - 2


def test_fuel_required_per_module():
    assert fuel_required_per_module(12) == 2
    assert fuel_required_per_module(14) == 2
    assert fuel_required_per_module(1969) == 654
    assert fuel_required_per_module(100756) == 33583


def fuel_required_for_all_modules(modules: List[int]) -> int:
    return [fuel_required_per_module(module) for module in modules]


def fuel_required_for_fuel(total_fuel_required: int) -> int:
    total = 0
    curr = total_fuel_required
    while fuel_required_per_module(curr) > 0:
        total += fuel_required_per_module(curr)
        curr = fuel_required_per_module(curr)
    return total


def total_fuel_required(modules: List[int]) -> int:
    total_fuel = []
    for module in modules:
        fuel_for_module = fuel_required_per_module(module)
        fuel_for_fuel = fuel_required_for_fuel(fuel_for_module)
        total_fuel.append(fuel_for_module + fuel_for_fuel)
    return total_fuel


def test_total_fuel_required():
    assert total_fuel_required([14]) == 2
    assert total_fuel_required([1969]) == 966
    assert total_fuel_required([100756]) == 50346


if __name__ == "__main__":
    modules = []
    with open("2019/data/day01_input.txt") as f:
        for line in f.readlines():
            modules.append(int(line))

    fuel_for_modules = fuel_required_for_all_modules(modules)
    print(f"Fuel required for modules: {sum(fuel_for_modules)}")

    total_fuel = total_fuel_required(modules)
    print(f"Fuel required for modules: {sum(total_fuel)}")
