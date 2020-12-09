from itertools import combinations
from typing import List


TEST_INPUT = """35
20
15
25
47
40
62
55
65
95
102
117
150
182
127
219
299
277
309
576"""

numbers = [int(value) for value in TEST_INPUT.split("\n")]


def find_invalid_encoding(numbers: List[int], preamble_size: int) -> int:
    data = numbers[:preamble_size]
    current_index = preamble_size

    while True:
        element_to_check = numbers[current_index]

        for num1, num2 in combinations(data, r=2):
            if num1 + num2 == element_to_check:
                current_index += 1
                data = data[1:] + [element_to_check]
                break
        else:
            # if we cycle thru all combinations and don't find a match
            return element_to_check

    raise ValueError("should not get here")


assert find_invalid_encoding(numbers, preamble_size=5) == 127


def find_contiguous_set_that_adds_to(numbers: List[int], sum_to: int) -> List[int]:
    for start, number in enumerate(numbers):
        for end in range(start+1,len(numbers)):
            sum_range = sum(numbers[start:end])
            if sum_range == sum_to:
                return numbers[start:end]
            elif sum_range > sum_to:
                break

    raise ValueError("should not get here")


assert find_contiguous_set_that_adds_to(numbers, sum_to=127) == [15, 25, 47, 40]


def sum_largest_smallest(numbers: List[int]) -> int:
    return min(numbers) + max(numbers)


assert sum_largest_smallest([15, 25, 47, 40]) == 62


if __name__ == "__main__":
    with open("2020/data/day09_input.txt") as f:
        numbers = [int(line) for line in f.readlines()]

    result = find_invalid_encoding(numbers, preamble_size=25)
    print(f"part 1 is {result}")

    sum_to_range = find_contiguous_set_that_adds_to(numbers, sum_to=result)
    result = sum_largest_smallest(sum_to_range)
    print(f"part 2 is {result}")
