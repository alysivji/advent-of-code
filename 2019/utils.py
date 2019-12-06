from typing import List, NamedTuple


class Halt(Exception):
    pass


class IntCodeComputer:
    def __str__(self):
        return ",".join([str(val) for val in self.program])

    def __init__(self, program: str, *, input_value: int = None):
        self.program: List[int] = [int(val) for val in program.split(",")]
        self.instruction_pointer: int = 0
        self.input = input_value
        self.OPERATIONS = [Add, Multiple, Terminate, Input, Output]

    def process(self) -> List[int]:
        self.captured_output = []
        while True:
            instruction_op_code = str(self.program[self.instruction_pointer])
            op_code = int(instruction_op_code[-2:])
            mode = instruction_op_code[: len(instruction_op_code) - 2]

            for op in self.OPERATIONS:
                if op.match(op_code):
                    break
            else:
                raise ValueError("Invalid op code")

            operation = op(
                self.program, self.instruction_pointer, mode, input_value=self.input
            )
            try:
                output = operation.execute()  # not all operations return output
                if output is not None:
                    self.captured_output.append(output)
            except Halt:
                break
            self.instruction_pointer += operation.num_parameters + 1

        return self.program


class Operation:
    def __init__(
        self,
        program: List[int],
        instruction_pointer: int,
        modes: str,
        *args,
        **kwargs
    ):
        self.program = program
        self.instruction_pointer = instruction_pointer
        # reverse modes as it goes from right to left
        modes_reversed = modes.zfill(self.num_parameters)[::-1]
        self.modes: List[int] = [int(val) for val in modes_reversed]

    @classmethod
    def match(cls, code) -> bool:
        return code == cls.OP_CODE


class Add(Operation):
    OP_CODE = 1
    num_parameters = 3

    def execute(self) -> None:
        code = self.program
        idx = self.instruction_pointer

        val1 = calculate_value_given_mode(code, idx, self.modes, 1)
        val2 = calculate_value_given_mode(code, idx, self.modes, 2)
        code[code[idx + 3]] = val1 + val2


class Multiple(Operation):
    OP_CODE = 2
    num_parameters = 3

    def execute(self) -> None:
        code = self.program
        idx = self.instruction_pointer

        # first parameter is in position mode
        val1 = calculate_value_given_mode(code, idx, self.modes, 1)
        val2 = calculate_value_given_mode(code, idx, self.modes, 2)
        code[code[idx + 3]] = val1 * val2


class Input(Operation):
    OP_CODE = 3
    num_parameters = 1

    def __init__(self, *args, **kwargs):
        input_value = kwargs.pop("input_value", None)
        if not input_value:
            raise ValueError("Input requires input_value")
        self.input = input_value
        super().__init__(*args, **kwargs)

    def execute(self) -> None:
        code = self.program
        idx = self.instruction_pointer
        code[code[idx + 1]] = self.input


class Output(Operation):
    OP_CODE = 4
    num_parameters = 1

    def execute(self) -> int:
        code = self.program
        idx = self.instruction_pointer
        return calculate_value_given_mode(code, idx, self.modes, 1)


class Terminate(Operation):
    OP_CODE = 99
    num_parameters = 0

    def execute(self) -> bool:
        raise Halt


def calculate_value_given_mode(
    code: List[int], index: int, modes: List[int], offset: int
) -> int:
    if modes[offset - 1] == 0:  # parameter mode
        return code[code[index + offset]]
    elif modes[offset - 1] == 1:  # immediate mode
        return code[index + offset]
    else:
        raise ValueError("Invalid mode value")
