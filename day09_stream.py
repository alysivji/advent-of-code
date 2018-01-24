"""Advent of Code 2017 -- Day 9

http://adventofcode.com/2017/day/9
"""


def get_score(stream: str) -> int:
    total_points = 0

    garbage_data = False  # refers to time when we have garbage data
    ignore_next_char = False  # for ! logic

    group_stack = list()

    for char in stream:
        # take care of ! char which ignores the next character
        if ignore_next_char:
            ignore_next_char = False
            continue
        if char == "!":
            ignore_next_char = True
            continue

        # if we are done with garbage data
        if garbage_data and char == '>':
            garbage_data = False
            continue

        # is data garbage
        if char == '<' and not garbage_data:
            garbage_data = True
            continue

        # group information
        if char == '{' and not garbage_data:
            group_stack.append(char)
            continue

        if char == '}' and not garbage_data:
            total_points += len(group_stack)
            group_stack.pop()
    return total_points


assert get_score('{}') == 1
assert get_score('{{{}}}') == 6
assert get_score('{{},{}}') == 5
assert get_score('{{{},{},{{}}}}') == 16
assert get_score('{<a>,<a>,<a>,<a>}') == 1
assert get_score('{{<ab>},{<ab>},{<ab>},{<ab>}}') == 9
assert get_score('{{<!!>},{<!!>},{<!!>},{<!!>}}') == 9
assert get_score('{{<a!>},{<a!>},{<a!>},{<ab>}}') == 3


def count_garbage(stream: str) -> int:
    total_garbage = 0

    garbage_data = False  # refers to time when we have garbage data
    ignore_next_char = False  # for ! logic

    group_stack = list()

    for char in stream:
        if garbage_data:
            total_garbage += 1

        # take care of ! char which ignores the next character
        if ignore_next_char:
            total_garbage -= 1  # cancelled garbage, doesn't count
            ignore_next_char = False
            continue
        if char == "!":
            total_garbage -= 1  # cancelled garbage, doesn't count
            ignore_next_char = True
            continue

        # if we are done with garbage data
        if garbage_data and char == '>':
            total_garbage -= 1  # not garbage, it's a marker
            garbage_data = False
            continue

        # is data garbage
        if char == '<' and not garbage_data:
            garbage_data = True
            continue

        # group information
        if char == '{' and not garbage_data:
            group_stack.append(char)
            continue

        if char == '}' and not garbage_data:
            group_stack.pop()

    return total_garbage


assert count_garbage('<>') == 0
assert count_garbage('<random characters>') == 17
assert count_garbage('<<<<>') == 3
assert count_garbage('<{!>}>') == 2
assert count_garbage('<!!>') == 0
assert count_garbage('<!!!>>') == 0
assert count_garbage('<{o"i!a,<{i<a>') ==10


if __name__ == '__main__':
    input_data = open('09_input.txt').read().strip()
    print(get_score(input_data))
    print(count_garbage(input_data))
