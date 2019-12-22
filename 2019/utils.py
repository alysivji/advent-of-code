from typing import List, NamedTuple


class Halt(Exception):
    pass


class IntCodeComputer:

    def __str__(self):
        return ",".join([str(val) for val in self.program[:self.original_program_size]])

    def __init__(
        self,
        program: str,
        *,
        input_value: int = None,
        phase: int = None,
        pause_on_output: bool = False,
        relative_base: int = 0,
        memory_size: int = None,
    ):
        self.program: List[int] = self._write_program_to_memory(program, memory_size=memory_size)
        self.instruction_pointer: int = 0
        self.input_value = input_value
        self.input = iter(self._generate_input(phase))
        self.pause_on_output = pause_on_output
        self.relative_base = relative_base
        ALL_OPERATIONS = [
            Add,
            Multiply,
            Input,
            Output,
            JumpIfTrue,
            JumpIfFalse,
            LessThan,
            Equals,
            ModifyRelativeBase,
            Terminate,
        ]
        self.operations_map = {op.OP_CODE: op for op in ALL_OPERATIONS}

    def process(self) -> List[int]:
        self.captured_output = []
        while True:
            instruction_op_code = str(self.program[self.instruction_pointer])
            op_code = int(instruction_op_code[-2:])
            mode = instruction_op_code[: len(instruction_op_code) - 2]

            try:
                op = self.operations_map[op_code]
            except IndexError:
                raise ValueError("Invalid op code")

            operation = op(
                self.program,
                self.relative_base,
                self.instruction_pointer,
                mode,
                input_value=next(self.input),
            )
            try:
                output = operation.execute()  # not all operations return output
            except Halt:
                break

            if self.relative_base != operation.relative_base:
                self.relative_base = operation.relative_base

            self._capture_output(output)
            self.instruction_pointer = self._next_instruction(operation)

            if self.captured_output and self.pause_on_output:
                break

        return self.program

    def _write_program_to_memory(self, program: str, memory_size: int = None) -> List[int]:
        program = [int(val) for val in program.split(",")]
        self.original_program_size = len(program)

        if not memory_size:
            memory_size = len(program)

        empty_blocks_to_add = memory_size - len(program)
        for _ in range(empty_blocks_to_add):
            program.append(0)

        return program

    def _generate_input(self, phase=None):
        if phase is not None:
            yield phase
        while True:
            yield self.input_value

    def _next_instruction(self, operation) -> int:
        if operation.instruction_pointer_changed:
            return operation.instruction_pointer
        return self.instruction_pointer + operation.num_parameters + 1

    def _update_relative_base(self, output: int) -> None:
        if operation.relative_base_changed:
            self.captured_output.append(output)

    def _capture_output(self, output: int) -> None:
        if output is not None:
            self.captured_output.append(output)


class Operation:
    def __init__(
        self,
        program: List[int],
        relative_base: int,
        instruction_pointer: int,
        modes: str,
        *args,
        **kwargs,
    ):
        self.program = program
        self.instruction_pointer = instruction_pointer
        self.relative_base = relative_base
        # reverse modes as it goes from right to left
        modes_reversed = modes.zfill(self.num_parameters)[::-1]
        self.modes: List[int] = [int(val) for val in modes_reversed]

        # parameters that inform
        self.instruction_pointer_changed = False
        self.relative_base_changed = False

    @classmethod
    def match(cls, code) -> bool:
        return code == cls.OP_CODE


class Add(Operation):
    OP_CODE = 1
    num_parameters = 3

    def execute(self) -> None:
        code = self.program
        idx = self.instruction_pointer

        val1 = calculate_value_given_mode(code, idx, self.modes, 1, self.relative_base)
        val2 = calculate_value_given_mode(code, idx, self.modes, 2, self.relative_base)
        index_to_update = calculate_index_given_mode(code, idx, self.modes, 3, self.relative_base)
        code[index_to_update] = val1 + val2


class Multiply(Operation):
    OP_CODE = 2
    num_parameters = 3

    def execute(self) -> None:
        code = self.program
        idx = self.instruction_pointer

        # first parameter is in position mode
        val1 = calculate_value_given_mode(code, idx, self.modes, 1, self.relative_base)
        val2 = calculate_value_given_mode(code, idx, self.modes, 2, self.relative_base)
        index_to_update = calculate_index_given_mode(code, idx, self.modes, 3, self.relative_base)
        code[index_to_update] = val1 * val2


class Input(Operation):
    OP_CODE = 3
    num_parameters = 1

    def __init__(self, *args, **kwargs):
        input_value = kwargs.pop("input_value", None)
        if input_value is None:
            raise ValueError("Input requires input_value")
        self.input = input_value
        super().__init__(*args, **kwargs)

    def execute(self) -> None:
        code = self.program
        idx = self.instruction_pointer
        index_to_update = calculate_index_given_mode(code, idx, self.modes, 1, self.relative_base)

        code[index_to_update] = self.input


class Output(Operation):
    OP_CODE = 4
    num_parameters = 1

    def execute(self) -> int:
        code = self.program
        idx = self.instruction_pointer
        return calculate_value_given_mode(code, idx, self.modes, 1, self.relative_base)


class JumpIfTrue(Operation):
    OP_CODE = 5
    num_parameters = 2

    def execute(self) -> None:
        code = self.program
        idx = self.instruction_pointer
        val1 = calculate_value_given_mode(code, idx, self.modes, 1, self.relative_base)
        val2 = calculate_value_given_mode(code, idx, self.modes, 2, self.relative_base)

        if val1 != 0:
            self.instruction_pointer_changed = True
            self.instruction_pointer = val2


class JumpIfFalse(Operation):
    OP_CODE = 6
    num_parameters = 2

    def execute(self) -> None:
        code = self.program
        idx = self.instruction_pointer
        val1 = calculate_value_given_mode(code, idx, self.modes, 1, self.relative_base)
        val2 = calculate_value_given_mode(code, idx, self.modes, 2, self.relative_base)

        if val1 == 0:
            self.instruction_pointer_changed = True
            self.instruction_pointer = val2


class LessThan(Operation):
    OP_CODE = 7
    num_parameters = 3

    def execute(self) -> None:
        code = self.program
        idx = self.instruction_pointer
        val1 = calculate_value_given_mode(code, idx, self.modes, 1, self.relative_base)
        val2 = calculate_value_given_mode(code, idx, self.modes, 2, self.relative_base)
        index_to_update = calculate_index_given_mode(code, idx, self.modes, 3, self.relative_base)

        if val1 < val2:
            code[index_to_update] = 1
        else:
            code[index_to_update] = 0


class Equals(Operation):
    OP_CODE = 8
    num_parameters = 3

    def execute(self) -> None:
        code = self.program
        idx = self.instruction_pointer
        val1 = calculate_value_given_mode(code, idx, self.modes, 1, self.relative_base)
        val2 = calculate_value_given_mode(code, idx, self.modes, 2, self.relative_base)
        index_to_update = calculate_index_given_mode(code, idx, self.modes, 3, self.relative_base)

        if val1 == val2:
            code[index_to_update] = 1
        else:
            code[index_to_update] = 0


class ModifyRelativeBase(Operation):
    OP_CODE = 9
    num_parameters = 1

    def execute(self) -> int:
        code = self.program
        idx = self.instruction_pointer
        val1 = calculate_value_given_mode(code, idx, self.modes, 1, self.relative_base)

        self.relative_base += val1
        self.relative_base_changed = True


class Terminate(Operation):
    OP_CODE = 99
    num_parameters = 0

    def execute(self) -> None:
        raise Halt


def calculate_value_given_mode(
    code: List[int], index: int, modes: List[int], offset: int, relative_base: int,
) -> int:
    if modes[offset - 1] == 0:  # parameter mode
        return code[code[index + offset]]
    elif modes[offset - 1] == 1:  # immediate mode
        return code[index + offset]
    elif modes[offset - 1] == 2:  # relative mode
        return code[relative_base + code[index + offset]]
    else:
        raise ValueError("Invalid mode value")


def calculate_index_given_mode(
    code: List[int], index: int, modes: List[int], offset: int, relative_base: int,
):
    if modes[offset - 1] == 2:  # relative mode
        return relative_base + code[index + offset]
    else:
        return code[index + offset]
