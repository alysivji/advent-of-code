"""Advent of Code Day 15

http://adventofcode.com/2017/day/15"""

from typing import Generator


def next_num_in_sequence(seed: int, factor: int, divide_by=1) -> int:
    last_num = seed

    while True:
        value = (last_num * factor) % 2_147_483_647
        if value % divide_by == 0:
            yield value
        last_num = value


# test next_num_in_sequence
test_generator_A = next_num_in_sequence(65, 16_807)
test_generator_B = next_num_in_sequence(8_921, 48_271)

test_result_A = []
test_result_B = []

for _ in range(5):
    test_result_A.append(next(test_generator_A))
    test_result_B.append(next(test_generator_B))

assert test_result_A == [1092455, 1181022009, 245556042, 1744312007, 1352636452]
assert test_result_B == [430625591, 1233683848, 1431495498, 137874439, 285222916]


def match_lowest_16_bits(num: int, other_num: int) -> bool:
    if bin(num)[-16:] == bin(other_num)[-16:]:
        return True
    return False


# test new generator
test_genA = next_num_in_sequence(65, 16_807, divide_by=4)
test_genB = next_num_in_sequence(8_921, 48_271, divide_by=8)

test_result_A = []
test_result_B = []

for _ in range(5):
    test_result_A.append(next(test_genA))
    test_result_B.append(next(test_genB))

assert test_result_A == [1352636452, 1992081072, 530830436, 1980017072, 740335192]
assert test_result_B == [1233683848, 862516352, 1159784568, 1616057672, 412269392]

is_match = []
for num, other_num in zip(test_result_A, test_result_B):
    is_match.append(match_lowest_16_bits(num, other_num))

assert is_match == [False, False, False, False, False]


def count_matching_pairs(upper_bound: int,
                         genA: Generator,
                         genB: Generator) -> bool:
    judge_count = 0
    for _ in range(upper_bound):
        if match_lowest_16_bits(next(genA), next(genB)):
            judge_count += 1

    return judge_count


if __name__ == '__main__':
    test_generator_A = next_num_in_sequence(65, 16_807)
    test_generator_B = next_num_in_sequence(8_921, 48_271)
    # print(count_matching_pairs(40_000_000, test_generator_A, test_generator_B))

    generator_A = next_num_in_sequence(618, 16_807)
    generator_B = next_num_in_sequence(814, 48_271)
    # print(count_matching_pairs(40_000_000, generator_A, generator_B))

    test_generator_A = next_num_in_sequence(65, 16_807, divide_by=4)
    test_generator_B = next_num_in_sequence(8_921, 48_271, divide_by=8)
    # print(count_matching_pairs(5_000_000, test_generator_A, test_generator_B))

    generator_A = next_num_in_sequence(618, 16_807, divide_by=4)
    generator_B = next_num_in_sequence(814, 48_271, divide_by=8)
    print(count_matching_pairs(5_000_000, generator_A, generator_B))
