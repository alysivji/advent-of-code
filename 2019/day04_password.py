from collections import defaultdict
from typing import Union
import pytest


def valid_password__part_a(value: Union[int, str]) -> bool:
    digits = [int(num) for num in str(value)]

    num_repeated = 0
    for left, right in zip(digits, digits[1:]):
        difference = right - left

        if right - left < 0:  # decreases
            return False
        if difference == 0:
            num_repeated += 1

    if num_repeated == 0:  # doesn't repeat digit
        return False
    return True


@pytest.mark.parametrize(
    "value, is_valid",
    [("122345", True), ("111111", True), ("223450", False), ("123789", False)],
)
def test_valid_password__part_a(value, is_valid):
    assert valid_password__part_a(value) == is_valid


def num_valid_passwords_in_range__part_a(lo, hi):
    num_valid_passwords = 0
    for possible_password in range(lo, hi + 1):
        if valid_password__part_a(possible_password):
            num_valid_passwords += 1
    return num_valid_passwords


def valid_password__part_b(value: Union[int, str]) -> bool:
    digits = [int(num) for num in str(value)]

    repeated_digits = defaultdict(int)
    for left, right in zip(digits, digits[1:]):
        difference = right - left

        if right - left < 0:  # decreases
            return False
        if difference == 0:
            repeated_digits[left] += 1

    two_adjacent_matching_not_part_of_larger_group = False
    for key, value in repeated_digits.items():
        if value == 1:  # if it's repeated once that means there is a group of 2
            two_adjacent_matching_not_part_of_larger_group = True

    if not two_adjacent_matching_not_part_of_larger_group:
        return False
    return True


@pytest.mark.parametrize(
    "value, is_valid",
    [("112233", True), ("123444", False), ("111122", True)],
)
def test_valid_password__part_b(value, is_valid):
    assert valid_password__part_b(value) == is_valid


def num_valid_passwords_in_range__part_b(lo, hi):
    num_valid_passwords = 0
    for possible_password in range(lo, hi + 1):
        if valid_password__part_b(possible_password):
            num_valid_passwords += 1
    return num_valid_passwords


if __name__ == "__main__":
    result = valid_password__part_a("122345")

    password_range__low, password_range__high = (134792, 675810)
    num_valid = num_valid_passwords_in_range__part_a(password_range__low, password_range__high)
    print(f"Number of valid passwords in part a is {num_valid}")

    num_valid = num_valid_passwords_in_range__part_b(password_range__low, password_range__high)
    print(f"Number of valid passwords in part b is {num_valid}")
