import pytest
from utils import IntCodeComputer


def test_process_copy_of_itself():
    intcode_program = "109,1,204,-1,1001,100,1,100,1008,100,16,101,1006,101,0,99"
    cpu = IntCodeComputer(intcode_program, memory_size=1024)
    cpu.process()
    assert str(cpu) == intcode_program


def test_output_has_16_chars():
    intcode_program = "1102,34915192,34915192,7,4,7,99,0"
    cpu = IntCodeComputer(intcode_program, memory_size=1024)
    cpu.process()
    assert len(str(cpu.captured_output[0])) == 16


def test_output_produces_middle_number():
    intcode_program = "104,1125899906842624,99"
    cpu = IntCodeComputer(intcode_program, memory_size=1024)
    cpu.process()
    assert cpu.captured_output[0] == 1125899906842624


if __name__ == "__main__":
    with open("2019/data/day09_input.txt", "r") as f:
        intcode_program = f.readline().strip()

    cpu = IntCodeComputer(intcode_program, memory_size=1_000_000, input_value=1)
    cpu.process()
    print(f"Test program output: {cpu.captured_output[0]})

    cpu = IntCodeComputer(intcode_program, memory_size=1_000_000, input_value=2)
    cpu.process()
    print(f"Boost program output: {cpu.captured_output[0]})
