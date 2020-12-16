from collections import defaultdict

import pytest


def speak_number(initial, stop_num):
    # given history, speak next number
    history = defaultdict(list)
    turn = 0
    for num in initial:
        turn += 1
        history[num].append(turn)
        last_spoken = num

    while turn < stop_num:
        turn += 1
        if len(history[last_spoken]) == 1:
            last_spoken = 0
        else:
            spoken_history = history[last_spoken]
            last_spoken = spoken_history[-1] - spoken_history[-2]

        history[last_spoken].append(turn)

    return last_spoken


@pytest.mark.parametrize(
    "list_o_numbers, number",
    [
        ([0, 3, 6], 436),
        ([1, 3, 2], 1),
        ([2, 1, 3], 10),
        ([1, 2, 3], 27),
        ([2, 3, 1], 78),
        ([3, 2, 1], 438),
        ([3, 1, 2], 1836),
    ],
)
def test_speak_number(list_o_numbers, number):
    assert speak_number(list_o_numbers, 2020) == number


@pytest.mark.parametrize(
    "list_o_numbers, num_turns",
    [
        # ([0, 3, 6], 175594),
        # ([1, 3, 2], 2578),
        # ([2, 1, 3], 3544142),
        # ([1, 2, 3], 261214),
        # ([2, 3, 1], 6895259),
        # ([3, 2, 1], 18),
        # ([3, 1, 2], 362),
    ],
)
def test_speak_number_part_2(list_o_numbers, num_turns):
    assert speak_number([0, 3, 6], 30000000) == 436


if __name__ == "__main__":
    with open("2020/data/day15_input.txt") as f:
        puzzle_input = [int(value) for value in f.read().split(",")]
    result = speak_number(puzzle_input, 2020)
    print(f"Part 1 is {result}")

    result = speak_number(puzzle_input, 30000000)
    print(f"Part 2 is {result}")
