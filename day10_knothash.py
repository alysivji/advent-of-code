"""Advent of Code 2017 -- Day 10

http://adventofcode.com/2017/day/10"""

from functools import reduce
from operator import xor


def get_mutated_list(input_list, input_lengths, curr_index=0, step_size=0):
    circular_list = input_list[:]
    list_size = len(circular_list)

    for length in input_lengths:
        end_index = (curr_index + length) % list_size

        if end_index < curr_index or length == list_size:
            # pop off back of list
            items_to_reverse = []
            items_to_reverse.extend(circular_list[curr_index:])
            items_to_reverse.extend(circular_list[:end_index])

            # put back on list (in reverse order)
            for index, _ in enumerate(circular_list[curr_index:]):
                circular_list[curr_index + index] = items_to_reverse.pop()
            for index, _ in enumerate(circular_list[:end_index]):
                circular_list[index] = items_to_reverse.pop()
        else:
            items_to_reverse = circular_list[curr_index:end_index]

            circular_list[curr_index:end_index] = items_to_reverse[::-1]

        # import pdb; pdb.set_trace()
        curr_index += length + step_size
        curr_index = curr_index % list_size
        step_size += 1

    return (circular_list, curr_index, step_size)


def knot_hash(input_):
    INPUT_LENGTHS2 = [ord(item) for item in input_]
    INPUT_LENGTHS2.extend([17, 31, 73, 47, 23])

    result = (list(range(256)), 0, 0)
    for _ in range(64):
        curr_list = result[0]
        curr_index = result[1]
        curr_step = result[2]
        result = get_mutated_list(curr_list,
                                  INPUT_LENGTHS2,
                                  curr_index=curr_index,
                                  step_size=curr_step)

    slices = [slice(16*(x), 16*(x+1)) for x in range(16)]
    blocks = [result[0][single_slice] for single_slice in slices]
    xor_result = [reduce(xor, block) for block in blocks]
    return ''.join([format(block, '2x') for block in xor_result])


if __name__ == '__main__':
    TEST_INPUT_LENGTHS = [int(item) for item in "3 4 1 5".split()]
    my_ans = get_mutated_list(list(range(5)),
                              TEST_INPUT_LENGTHS,
                              curr_index=0,
                              step_size=0)

    INPUT_LENGTHS = [int(item) for item in "206,63,255,131,65,80,238,157,254,24,133,2,16,0,1,3".split(',')]  # noqa
    result = get_mutated_list(list(range(256)),
                              INPUT_LENGTHS,
                              curr_index=0,
                              step_size=0)

    result = knot_hash("206,63,255,131,65,80,238,157,254,24,133,2,16,0,1,3")
    print(result)
