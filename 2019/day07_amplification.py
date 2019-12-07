import itertools
import math

import pytest

from utils import IntCodeComputer


def process_thru_amplification_circuit(intcode_program, phase):
    amplifer_a = IntCodeComputer(intcode_program, input_value=0, phase=phase[0])
    amplifer_a.process()
    output_a = amplifer_a.captured_output[-1]

    amplifer_b = IntCodeComputer(intcode_program, input_value=output_a, phase=phase[1])
    amplifer_b.process()
    output_b = amplifer_b.captured_output[-1]

    amplifer_c = IntCodeComputer(intcode_program, input_value=output_b, phase=phase[2])
    amplifer_c.process()
    output_c = amplifer_c.captured_output[-1]

    amplifer_d = IntCodeComputer(intcode_program, input_value=output_c, phase=phase[3])
    amplifer_d.process()
    output_d = amplifer_d.captured_output[-1]

    amplifer_e = IntCodeComputer(intcode_program, input_value=output_d, phase=phase[4])
    amplifer_e.process()
    output_e = amplifer_e.captured_output[-1]

    return output_e


def test_process_thru_amplification_circuit():
    intcode_program = "3,15,3,16,1002,16,10,16,1,16,15,15,4,15,99,0,0"
    phase = [4, 3, 2, 1, 0]

    result = process_thru_amplification_circuit(intcode_program, phase)

    assert result == 43210


def find_highest_signal(intcode_program):
    possible_phase_sequence = itertools.permutations([0, 1, 2, 3, 4], 5)
    max_signal = -math.inf

    for phase in possible_phase_sequence:
        signal = process_thru_amplification_circuit(intcode_program, phase)
        if signal > max_signal:
            max_signal = signal

    return max_signal, phase


def test_find_highest_signal():
    intcode_program = "3,15,3,16,1002,16,10,16,1,16,15,15,4,15,99,0,0"

    result = find_highest_signal(intcode_program)

    assert result == (43210, (4, 3, 2, 1, 0))


def process_thru_amplification_feedback_circuit(intcode_program, phase):
    amplifiers = [
        ("a", IntCodeComputer(intcode_program, phase=phase[0], pause_on_output=True)),
        ("b", IntCodeComputer(intcode_program, phase=phase[1], pause_on_output=True)),
        ("c", IntCodeComputer(intcode_program, phase=phase[2], pause_on_output=True)),
        ("d", IntCodeComputer(intcode_program, phase=phase[3], pause_on_output=True)),
        ("e", IntCodeComputer(intcode_program, phase=phase[4], pause_on_output=True)),
    ]
    feedback_circuit = itertools.cycle(amplifiers)
    input_value = 0

    while True:
        name, amplifier = next(feedback_circuit)
        amplifier.input_value = input_value
        amplifier.process()

        try:
            input_value = amplifier.captured_output.pop()
        except IndexError:
            break

    return input_value


TEST_INPUT1 = (
    "3,26,1001,26,-4,26,3,27,1002,27,2,27,1,27,26,"
    "27,4,27,1001,28,-1,28,1005,28,6,99,0,0,5"
)

TEST_INPUT2 = (
    "3,52,1001,52,-5,52,3,53,1,52,56,54,1007,54,5,55,1005,55,26,1001,54,"
    "-5,54,1105,1,12,1,53,54,53,1008,54,0,55,1001,55,1,55,2,53,55,53,4,"
    "53,1001,56,-1,56,1005,56,6,99,0,0,0,0,10"
)


@pytest.mark.parametrize(
    "intcode_program, phase, expected_output",
    [
        (TEST_INPUT1, [9, 8, 7, 6, 5], 139629729),
        (TEST_INPUT2, [9, 7, 8, 5, 6], 18216)
    ],
)
def test_process_thru_amplification_feedback_circuit(
    intcode_program, phase, expected_output
):
    result = process_thru_amplification_feedback_circuit(intcode_program, phase)
    assert result == expected_output


def find_highest_signal_feedback(intcode_program):
    possible_phase_sequence = itertools.permutations([5, 6, 7, 8, 9], 5)
    max_signal = -math.inf

    for phase in possible_phase_sequence:
        signal = process_thru_amplification_feedback_circuit(intcode_program, phase)
        if signal > max_signal:
            max_signal = signal

    return max_signal, phase


if __name__ == "__main__":
    with open("2019/data/day07_input.txt", "r") as f:
        intcode_program = f.readline().strip()

    result = find_highest_signal(intcode_program)
    print(f"Highest signal is: {result[0]}")

    result = find_highest_signal_feedback(intcode_program)
    print(f"Highest signal with feedback is: {result[0]}")
