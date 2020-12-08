from typing import List, NamedTuple


class Instruction(NamedTuple):
    operation: str
    argument: int


TEST_INPUT = """nop +0
acc +1
jmp +4
acc +3
jmp -3
acc -99
acc +1
jmp -4
acc +6"""


def parse_instructions(instruction_set):
    parsed_instructions = []
    for line in instruction_set:
        op, arg = line.split(" ")
        instruction = Instruction(op, int(arg))
        parsed_instructions.append(instruction)

    return parsed_instructions


test_instructions = parse_instructions(TEST_INPUT.split("\n"))


def run_program(instruction_set: List[Instruction]):
    accumulator_value = 0
    lines_executed = set()
    index = 0

    while True:
        if index in lines_executed or index >= len(instruction_set):
            break

        lines_executed.add(index)
        current_instruction = instruction_set[index]

        if current_instruction.operation == "nop":
            index += 1
        elif current_instruction.operation == "acc":
            accumulator_value += current_instruction.argument
            index += 1
        elif current_instruction.operation == "jmp":
            index += current_instruction.argument

    program_halted = True if len(instruction_set) - 1 in lines_executed else False
    return accumulator_value, program_halted


assert run_program(test_instructions) == (5, False)


def change_single_instruction_and_run_program(instruction_set: List[Instruction]):
    for idx, instruction in enumerate(instruction_set):
        if instruction.operation == "jmp":
            changed_instruction = Instruction("nop", instruction.argument)
        elif instruction.operation == "nop":
            changed_instruction = Instruction("jmp", instruction.argument)
        else:
            continue

        if idx == 0:
            new_instruction_set = [changed_instruction] + instruction_set[1:]
        else:
            new_instruction_set = (
                instruction_set[0:idx]
                + [changed_instruction]
                + instruction_set[idx + 1 :]
            )

        result, program_halted = run_program(new_instruction_set)

        if program_halted:
            return result

assert change_single_instruction_and_run_program(test_instructions) == 8


if __name__ == "__main__":
    with open("2020/data/day08_input.txt") as f:
        instruction_set = parse_instructions(f.readlines())

    result, program_halted = run_program(instruction_set)
    print(f"Part 1 is {result}")
    print(f"Part 2 is {change_single_instruction_and_run_program(instruction_set)}")
