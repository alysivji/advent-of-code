"""Avent of Code 2017 -- Day 8

http://adventofcode.com/2017/day/8
"""

from collections import defaultdict
import re
from typing import Dict, List, NamedTuple

INSTRUCTION_REGEX = re.compile(
    "(\w+)\s(inc|dec)\s(\-*\d+)\sif\s(\w+)\s(<|>|<=|>=|==|!=)\s(\-*\d+)")
TEST_INPUT = """b inc 5 if a > 1
a inc 1 if b < 5
c dec -10 if a >= 1
c inc -20 if c == 10"""


class Instruction(NamedTuple):
    register: str
    op: str
    amount: int
    conditional_register: str
    conditional_op: str
    conditional_amount: int


def parse_instructions(lines: str) -> List[Instruction]:
    instructions = []

    for line in lines.splitlines():
        parts = INSTRUCTION_REGEX.search(line)

        (register, op, amount, conditional_register,
         conditional_op, conditional_amount) = parts.groups()

        result = Instruction(register,
                             '+' if op == 'inc' else '-',
                             int(amount),
                             conditional_register,
                             conditional_op,
                             int(conditional_amount))
        instructions.append(result)

    return instructions


def largest_register_value(instructions: List[Instruction]) -> int:
    # # get all distinct registers
    # registers = [instruction.register for instruction in instructions]
    # registers += [instruction.conditional_register
    #               for instruction in instructions]
    # distinct_registers = set(registers)

    # # initialize register values
    # register_values = {}
    # for register in distinct_registers:
    #     register_values[register] = 0
    # ------------------------------------------------------------------------
    # improvement ... could add a default dict here
    register_values: Dict[str, int] = defaultdict(int)

    max_value = 0

    # run thru each instruction and evaluate
    for instruction in instructions:
        # check condition
        condition = (
            f"register_values['{instruction.conditional_register}'] " +
            f"{instruction.conditional_op} {instruction.conditional_amount}")

        if eval(condition):
            expression = (
                f"register_values['{instruction.register}'] " +
                f"{instruction.op}= {instruction.amount}")
            exec(expression)

        if max(register_values.values()) >= max_value:
            max_value = max(register_values.values())

    print(f'Lifetime max value: {max_value}')

    return max(register_values.values())


if __name__ == '__main__':
    instructions = parse_instructions(TEST_INPUT)
    assert largest_register_value(instructions) == 1

    with open('08_input.txt', 'r') as f:
        instructions = parse_instructions(f.read())
        print(largest_register_value(instructions))
