"""Advent of Code -- Day 17

http://adventofcode.com/2017/day/17"""

from typing import List


def insert_value(circular_buffer: List, num_steps: int) -> List:
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


def find_item_after(ciricular_buffer: List, item: int) -> int:
    position = ciricular_buffer.index(item)
    return ciricular_buffer[position + 1]


if __name__ == '__main__':
    NUM_STEPS = 386
    starting_buffer = [0]
    test_buffer = starting_buffer
    buffer = starting_buffer

    for _ in range(2017):
        test_buffer = insert_value(test_buffer, num_steps=3)
        buffer = insert_value(buffer, num_steps=386)

    # this is really slow because python insert is O(n)
    # need to optimize... O(1) insertion of linked list...
    angry_buffer = starting_buffer
    for count in range(50_000_000):
        if count % 10_000 == 0:
            print(count)
        angry_buffer = insert_value(angry_buffer, num_steps=386)

    assert find_item_after(test_buffer, 2017) == 638
    print(find_item_after(buffer, 2017))
    print(find_item_after(angry_buffer, 0))
