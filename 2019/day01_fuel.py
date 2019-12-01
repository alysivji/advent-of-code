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
    return sum(fuel_required_per_module(module) for module in modules)


if __name__ == "__main__":
    modules = []
    with open("2019/data/day01_input.txt") as f:
        for line in f.readlines():
            modules.append(int(line))

    fuel_for_modules = fuel_required_for_all_modules(modules)
    print(f"Fuel required for modules: {fuel_for_modules}")
