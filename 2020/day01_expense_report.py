from functools import reduce
import itertools


def multiply_pair_that_sums_to(entries, sum_to):
    pairs = itertools.combinations(entries, r=2)

    for num1, num2 in pairs:
        total = num1 + num2
        if total == sum_to:
             return num1 * num2
    raise ValueError("no pairs found")


def multiply_triple_that_sums_to(entries, sum_to):
    triples = itertools.combinations(entries, r=3)

    for num1, num2, num3 in triples:
        total = num1 + num2 + num3
        if total == sum_to:
             return num1 * num2 * num3
    raise ValueError("no triples found")


def multiply_n_numbers_that_sum_to(entries, n, sum_to):
    numbers = itertools.combinations(entries, r=n)

    for nums in numbers:
        if sum(nums) == sum_to:
            return reduce(lambda a, b: a * b, nums)
    raise ValueError("not found")


def test_multiply_pair_that_sums_to():
    TEST_INPUT_PART_1 = """1721
    979
    366
    299
    675
    1456""".split("\n")
    entries = [int(item) for item in TEST_INPUT_PART_1]

    result = multiply_pair_that_sums_to(entries, sum_to=2020)
    assert result == 514_579
    assert result == multiply_n_numbers_that_sum_to(entries, n=2, sum_to=2020)


def test_multiply_triple_that_sums_to():
    TEST_INPUT_PART_1 = """1721
    979
    366
    299
    675
    1456""".split("\n")
    entries = [int(item) for item in TEST_INPUT_PART_1]

    result = multiply_triple_that_sums_to(entries, sum_to=2020)
    assert result == 241861950
    assert result == multiply_n_numbers_that_sum_to(entries, n=3, sum_to=2020)



if __name__ == "__main__":
    with open("2020/data/day01_input.txt") as f:
        entries = [int(line) for line in f.readlines()]

    part_one_result = multiply_n_numbers_that_sum_to(entries, n=2, sum_to=2020)
    print(part_one_result)

    part_two_result = multiply_n_numbers_that_sum_to(entries, n=3, sum_to=2020)
    print(part_two_result)
