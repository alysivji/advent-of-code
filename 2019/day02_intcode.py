from typing import List

import pytest


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


if __name__ == "__main__":
    with open("2019/data/day02_input.txt") as f:
        intcode = [int(val) for val in f.readline().strip().split(",")]

    intcode = restore_to_1202_state(intcode)
    processed_intcode = process_intcode_program(intcode)
    print(f"Value at position 0 is: {processed_intcode[0]}")
