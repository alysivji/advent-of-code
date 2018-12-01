from itertools import cycle
from typing import List, Optional


def load_input(filename: str) -> List[int]:
    with open(filename, "r") as f:
        lines = f.readlines()
    return [int(line.strip()) for line in lines]


def get_ending_frequency(values: List[int]) -> int:
    return sum(values)


assert get_ending_frequency([+1, +1, +1]) == 3
assert get_ending_frequency([+1, +1, -2]) == 0
assert get_ending_frequency([-1, -2, -3]) == -6


def visited_twice(values: List[int]) -> Optional[int]:
    total = 0
    visited = set([total])
    for item in cycle(values):
        total += item
        if total in visited:
            return total
        visited.add(total)
    return None


assert visited_twice([+1, -1]) == 0
assert visited_twice([+3, +3, +4, -2, -4]) == 10
assert visited_twice([-6, +3, +8, +5, -6]) == 5
assert visited_twice([+7, +7, -2, -7, -4]) == 14


if __name__ == "__main__":
    values = load_input("day1_input.txt")
    print(get_ending_frequency(values))
    print(visited_twice(values))
