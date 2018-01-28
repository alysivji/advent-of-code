"""Advent of Code -- Day 17

http://adventofcode.com/2017/day/17"""

from collections import deque


def insert_value(circular_buffer, num_steps):
    new_buffer = list(circular_buffer)

    pos_of_max_element = circular_buffer.index(max(circular_buffer))
    insert_position = (pos_of_max_element + num_steps) % len(circular_buffer) + 1
    value_to_insert = len(new_buffer)

    new_buffer.insert(insert_position, value_to_insert)
    return new_buffer


TEST_NUM_STEPS = 3
assert insert_value([0], TEST_NUM_STEPS) == [0, 1]
assert insert_value([0, 1], TEST_NUM_STEPS) == [0, 2, 1]
assert insert_value([0, 2, 1], TEST_NUM_STEPS) == [0, 2, 3, 1]
assert insert_value([0, 2, 3, 1], TEST_NUM_STEPS) == [0, 2, 4, 3, 1]


def find_item_after(ciricular_buffer, item):
    position = ciricular_buffer.index(item)
    return ciricular_buffer[position + 1]


def brute_force_deque(upper_bound, num_steps, value_after):
    buffer = deque()
    buffer.append(0)

    for value_to_insert in range(1, upper_bound + 1):
        buffer.rotate(-num_steps)
        buffer.append(value_to_insert)

    # this is python 3.5+
    return buffer[(buffer.index(value_after) + 1) % len(buffer)]


def get_value_after_zero(upper_bound, num_steps):
    """Note 0 does not move because it is the first element in the list

    Thanks to reddit for the shortcut solution
    https://www.reddit.com/r/adventofcode/comments/7kc0xw/2017_day_17_solutions/
    """
    insert_loc = 0
    value_after_zero = 0

    for value_to_insert in range(1, upper_bound+1):
        size_of_buffer = value_to_insert
        insert_loc = (insert_loc + num_steps) % size_of_buffer
        insert_loc += 1
        # i.e. 0 does not move
        if insert_loc == 1:
            value_after_zero = value_to_insert

    return value_after_zero


if __name__ == '__main__':
    NUM_STEPS = 386
    starting_buffer = [0]
    test_buffer = starting_buffer
    buffer = starting_buffer

    for _ in range(2017):
        test_buffer = insert_value(test_buffer, num_steps=3)
        buffer = insert_value(buffer, num_steps=386)

    assert find_item_after(test_buffer, 2017) == 638
    print(find_item_after(buffer, 2017))

    # # this is really slow because python insert is O(n)
    # angry_buffer = starting_buffer
    # for count in range(50_000_000):
    #     if count % 10_000 == 0:
    #         print(count)
    #     angry_buffer = insert_value(angry_buffer, num_steps=386)
    # print(find_item_after(angry_buffer, 0))

    # Use a deque which has O(1) inserts at ends of list
    # We can also rotate which is O(k) where k = number of steps to rotate
    # assert brute_force_deque(2017, 386, 2017) == 419
    # print(brute_force_deque(50000000, 386, 0))

    # Shortcut solution
    print(get_value_after_zero(50000000, 386))
