from typing import List, NamedTuple

import pytest


class TunedParameters(NamedTuple):
    noun: int
    verb: int


def process_intcode_program(intcode: List[int]) -> List[int]:
    idx = 0
    while True:
        optcode = intcode[idx]
        if optcode == 1:
            intcode[intcode[idx + 3]] = intcode[intcode[idx + 1]] + intcode[intcode[idx + 2]]
        elif optcode == 2:
            intcode[intcode[idx + 3]] = intcode[intcode[idx + 1]] * intcode[intcode[idx + 2]]
        elif optcode == 99:
            break
        idx += 4

    return intcode


@pytest.mark.parametrize(
    "test_input, expected_output",
    [
        ("1,9,10,3,2,3,11,0,99,30,40,50", "3500,9,10,70,2,3,11,0,99,30,40,50"),
        ("1,0,0,0,99", "2,0,0,0,99"),
        ("2,3,0,3,99", "2,3,0,6,99"),
        ("2,4,4,5,99,0", "2,4,4,5,99,9801"),
        ("1,1,1,4,99,5,6,0,99", "30,1,1,4,2,5,6,0,99"),
    ],
)
def test_process_intcode_program(test_input, expected_output):
    vals = [int(val) for val in test_input.split(",")]
    output_vals = [int(val) for val in expected_output.split(",")]
    assert process_intcode_program(vals) == output_vals


def restore_to_1202_state(intcode: List[int]) -> List[int]:
    new_intcode = intcode[:]
    new_intcode[1] = 12
    new_intcode[2] = 2
    return new_intcode


def create_initial_memory_state(intcode: List[int], noun: int, verb: int) -> List[int]:
    initial_memory_state = intcode[:]
    initial_memory_state[1] = noun
    initial_memory_state[2] = verb
    return initial_memory_state


def parameter_tuning(intcode, target=19690720):
    for noun in range(100):
        for verb in range(100):
            initial_memory_state = create_initial_memory_state(intcode, noun, verb)
            result = process_intcode_program(initial_memory_state)
            if result[0] == 19690720:
                return TunedParameters(noun, verb)
    return TunedParameters(None, None)


if __name__ == "__main__":
    with open("2019/data/day02_input.txt") as f:
        intcode = [int(val) for val in f.readline().strip().split(",")]

    memory_state_1202 = restore_to_1202_state(intcode)
    processed_intcode = process_intcode_program(memory_state_1202)
    print(f"Value at position 0 is: {processed_intcode[0]}")

    noun, verb = parameter_tuning(intcode)
    print(f"Noun is {noun}, verb is {verb}, 100 * noun + verb = {100 * noun + verb}")
