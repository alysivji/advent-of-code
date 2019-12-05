from typing import List, NamedTuple


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

    def process(self) -> List[int]:
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
    def __init__(self, program: List[int], instruction_pointer: int):
        self.program = program
        self.instruction_pointer = instruction_pointer

    @classmethod
    def match(cls, code) -> bool:
        return code == cls.OP_CODE


class Add(Operation):
    OP_CODE = 1
    num_parameters = 3

    def execute(self) -> bool:
        code = self.program
        idx = self.instruction_pointer
        code[code[idx + 3]] = code[code[idx + 1]] + code[code[idx + 2]]


class Multiple(Operation):
    OP_CODE = 2
    num_parameters = 3

    def execute(self) -> bool:
        code = self.program
        idx = self.instruction_pointer
        code[code[idx + 3]] = code[code[idx + 1]] * code[code[idx + 2]]


class Terminate(Operation):
    OP_CODE = 99
    num_parameters = 0

    def execute(self) -> bool:
        raise Halt
