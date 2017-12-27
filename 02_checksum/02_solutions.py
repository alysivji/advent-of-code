"""Advent of Code - Day 2
"""
import itertools


def read_file(file):
    contents = []

    with open(file, 'r') as f:
        for line in f.readlines():
            cleaned_line = line.rstrip()
            contents.append(cleaned_line)

    return contents


def line_ck_sum(values, ck_type):
    line_ck_sum = 0

    if ck_type is 'whole_num':
        all_pairs = list(itertools.permutations(values, r=2))
        for x, y in all_pairs:
            if x % y == 0:
                line_ck_sum += int(x / y)
                break
    else:  # default is min_max
        min_value = min(values)
        max_value = max(values)

        line_ck_sum = max_value - min_value

    return line_ck_sum


def calc_checksum(file, ck_type='min_max'):
    checksum = 0

    data = read_file(file)

    for row in data:
        values = [int(cell) for cell in row.split()]
        checksum += line_ck_sum(values, ck_type)

    return checksum


if __name__ == '__main__':
    assert calc_checksum('02_day/test_input.txt', ck_type='min_max') == 18
    print(calc_checksum('02_day/problem_input.txt', ck_type='min_max'))

    assert calc_checksum('02_day/test2_input.txt', ck_type='whole_num') == 9
    print(calc_checksum('02_day/problem_input.txt', ck_type='whole_num'))
