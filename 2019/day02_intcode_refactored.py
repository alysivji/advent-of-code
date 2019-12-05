from typing import List, NamedTuple

import pytest


class Halt(Exception):
    pass


class TunedParameters(NamedTuple):
    noun: int
    verb: int


class IntCodeComputer:
    def __init__(self, program: List[int]):
        self.program = program
        self.instruction_pointer = 0
        self.possible_operations = [Add, Multiple, Terminate]

    def process(self):
        while True:
            op_code = self.program[self.instruction_pointer]
            for op in self.possible_operations:
                if op.match(op_code):
                    break
            else:
                raise ValueError("Invalid op code")

            operation = op(self.program, self.instruction_pointer)
            try:
                operation.execute()
            except Halt:
                break
            self.instruction_pointer += operation.num_parameters + 1

        return self.program


class Operation:
    def __init__(self, program, instruction_pointer):
        self.program = program
        self.instruction_pointer = instruction_pointer

    @classmethod
    def match(cls, code):
        return code == cls.OP_CODE


class Add(Operation):
    OP_CODE = 1
    num_parameters = 3

    def execute(self):
        code = self.program
        idx = self.instruction_pointer
        code[code[idx + 3]] = code[code[idx + 1]] + code[code[idx + 2]]


class Multiple(Operation):
    OP_CODE = 2
    num_parameters = 3

    def execute(self):
        code = self.program
        idx = self.instruction_pointer
        code[code[idx + 3]] = code[code[idx + 1]] * code[code[idx + 2]]


class Terminate(Operation):
    OP_CODE = 99
    num_parameters = 0

    def execute(self):
        raise Halt


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
    assert IntCodeComputer(vals).process() == output_vals


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
            cpu = IntCodeComputer(initial_memory_state)
            processed_intcode = cpu.process()
            if processed_intcode[0] == 19690720:
                return TunedParameters(noun, verb)
    return TunedParameters(None, None)


if __name__ == "__main__":
    with open("2019/data/day02_input.txt") as f:
        intcode = [int(val) for val in f.readline().strip().split(",")]

    memory_state_1202 = restore_to_1202_state(intcode)
    cpu = IntCodeComputer(memory_state_1202)
    processed_intcode = cpu.process()
    print(f"Value at position 0 is: {processed_intcode[0]}")

    noun, verb = parameter_tuning(intcode)
    print(f"Noun is {noun}, verb is {verb}, 100 * noun + verb = {100 * noun + verb}")
