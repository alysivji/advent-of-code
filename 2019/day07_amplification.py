import itertools
import math

from utils import IntCodeComputer


def process_thru_amplification_circuit(intcode_program, phase_seq):
    amplifer_a = IntCodeComputer(intcode_program, input_value=[phase_seq[0], 0])
    amplifer_a.process()
    output_a = amplifer_a.captured_output[-1]

    amplifer_b = IntCodeComputer(intcode_program, input_value=[phase_seq[1], output_a])
    amplifer_b.process()
    output_b = amplifer_b.captured_output[-1]

    amplifer_c = IntCodeComputer(intcode_program, input_value=[phase_seq[2], output_b])
    amplifer_c.process()
    output_c = amplifer_c.captured_output[-1]

    amplifer_d = IntCodeComputer(intcode_program, input_value=[phase_seq[3], output_c])
    amplifer_d.process()
    output_d = amplifer_d.captured_output[-1]

    amplifer_e = IntCodeComputer(intcode_program, input_value=[phase_seq[4], output_d])
    amplifer_e.process()
    output_e = amplifer_e.captured_output[-1]

    return output_e


def test_process_thru_amplification_circuit():
    intcode_program = "3,15,3,16,1002,16,10,16,1,16,15,15,4,15,99,0,0"
    phase_seq = [4, 3, 2, 1, 0]

    result = process_thru_amplification_circuit(intcode_program, phase_seq)

    assert result == 43210


def find_highest_signal(intcode_program):
    possible_phase_sequence = itertools.permutations([0, 1, 2, 3, 4], 5)
    max_signal = -math.inf

    for phase_seq in possible_phase_sequence:
        signal = process_thru_amplification_circuit(intcode_program, phase_seq)
        if signal > max_signal:
            max_signal = signal

    return max_signal, phase_seq


def test_find_highest_signal():
    intcode_program = "3,15,3,16,1002,16,10,16,1,16,15,15,4,15,99,0,0"

    result = find_highest_signal(intcode_program)

    assert result == (43210, (4, 3, 2, 1, 0))


if __name__ == "__main__":
    with open("2019/data/day07_input.txt", "r") as f:
        intcode_program = f.readline().strip()

    result = find_highest_signal(intcode_program)
    print(f"Highest signal is: {result[0]}")
