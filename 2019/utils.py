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

            operation = op(self.program, self.instruction_pointer, mode, self.input)
            try:
                output = operation.execute()  # not all operations return output
                if output:
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
        parameter_modes: str,
        *args, **kwargs
    ):
        self.program = program
        self.instruction_pointer = instruction_pointer
        # reverse parameter_modes as it goes from right to left
        modes = parameter_modes.zfill(self.num_parameters)[::-1]
        self.parameter_modes = [int(val) for val in modes]

    @classmethod
    def match(cls, code) -> bool:
        return code == cls.OP_CODE


class Add(Operation):
    OP_CODE = 1
    num_parameters = 3

    def execute(self) -> None:
        code = self.program
        idx = self.instruction_pointer

        # first parameter is in position mode
        if self.parameter_modes[0] == 0:
            val1 = code[code[idx + 1]]
        else:
            val1 = code[idx + 1]

        # second parameter is in position mode
        if self.parameter_modes[1] == 0:
            val2 = code[code[idx + 2]]
        else:
            val2 = code[idx + 2]

        param2_position_mode = self.parameter_modes[1] == 0
        code[code[idx + 3]] = val1 + val2


class Multiple(Operation):
    OP_CODE = 2
    num_parameters = 3

    def execute(self) -> None:
        code = self.program
        idx = self.instruction_pointer

        # first parameter is in position mode
        if self.parameter_modes[0] == 0:
            val1 = code[code[idx + 1]]
        else:
            val1 = code[idx + 1]

        # second parameter is in position mode
        if self.parameter_modes[1] == 0:
            val2 = code[code[idx + 2]]
        else:
            val2 = code[idx + 2]

        param2_position_mode = self.parameter_modes[1] == 0
        code[code[idx + 3]] = val1 * val2


class Input(Operation):
    OP_CODE = 3
    num_parameters = 1

    def __init__(self, program, instruction_pointer, mode, input_value, *args, **kwargs):
        self.input = input_value
        super().__init__(program, instruction_pointer, mode, *args, **kwargs)

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

        # first parameter is in position mode
        if self.parameter_modes[0] == 0:
            return code[code[idx + 1]]
        else:
            return code[idx + 1]


class Terminate(Operation):
    OP_CODE = 99
    num_parameters = 0

    def execute(self) -> bool:
        raise Halt
