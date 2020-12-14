from collections import defaultdict
from itertools import product
import re


to_binary = lambda x, n: bin(x)[2:].zfill(n)
MEMORY_UPDATE_PATTERN = re.compile(r"^mem\[(?P<address>\d+)\] = (?P<value>\d+)$")
p = re.compile(MEMORY_UPDATE_PATTERN)


class InitializationProgramV1:
    def __init__(self):
        self.memory = defaultdict(lambda x: "0" * 36)

    def process_instructions(self, instructions):
        for instruction in instructions:
            if instruction.startswith("mask = "):
                value = instruction.split("mask = ")[1]
                self._update_mask(value)
            elif instruction.startswith("mem["):
                m = p.match(instruction)
                address = int(m.group("address"))
                value = int(m.group("value"))
                binary_value = to_binary(value, 36)
                self._apply_mask(address, binary_value)

    def _update_mask(self, mask):
        self.mask = mask

    def _apply_mask(self, memory_address, value_to_write):
        modified_value = ""
        for mask_i, value_i in zip(self.mask, value_to_write):
            if mask_i == "X":
                modified_value += value_i
            else:
                modified_value += mask_i
        self.memory[memory_address] = modified_value

    def sum_memory(self):
        total = 0
        for key, value in self.memory.items():
            total += int(value, 2)
        return total


TEST_INPUT_1 = """mask = XXXXXXXXXXXXXXXXXXXXXXXXXXXXX1XXXX0X
mem[8] = 11
mem[7] = 101
mem[8] = 0"""


def test_part_1():
    program = InitializationProgramV1()
    instructions = TEST_INPUT_1.split("\n")
    program.process_instructions(instructions)
    assert program.sum_memory() == 165


class InitializationProgramV2:
    def __init__(self):
        self.memory = defaultdict(lambda x: "0" * 36)

    def process_instructions(self, instructions):
        for instruction in instructions:
            if instruction.startswith("mask = "):
                value = instruction.split("mask = ")[1]
                self._update_mask(value)
            elif instruction.startswith("mem["):
                m = p.match(instruction)
                address = int(m.group("address"))
                value = int(m.group("value"))
                binary_value = to_binary(value, 36)
                self._apply_mask(address, binary_value)

    def _update_mask(self, mask):
        self.mask = mask

    def _apply_mask(self, memory_address, value_to_write):
        # apply mask to memory
        memory_address_binary = to_binary(memory_address, 36)

        memory_value = ""
        for mask_i, value_i in zip(self.mask, memory_address_binary):
            if mask_i == "0":
                memory_value += value_i
            elif mask_i == "1":
                memory_value += "1"
            elif mask_i == "X":
                memory_value += "X"
            else:
                raise ValueError("should not get here")

        num_addresses_to_update = memory_value.count("X")
        for n_pairs in product(["0", "1"], repeat=num_addresses_to_update):
            remaining = list(n_pairs)

            current_memory_value = ""
            for bit in memory_value:
                if bit == "X":
                    current_memory_value += remaining.pop()
                else:
                    current_memory_value += bit

            self.memory[current_memory_value] = value_to_write

    def sum_memory(self):
        total = 0
        for key, value in self.memory.items():
            total += int(value, 2)
        return total


TEST_INPUT_2 = """mask = 000000000000000000000000000000X1001X
mem[42] = 100
mask = 00000000000000000000000000000000X0XX
mem[26] = 1"""


def test_part_2():
    program = InitializationProgramV2()
    instructions = TEST_INPUT_2.split("\n")
    program.process_instructions(instructions)
    assert program.sum_memory() == 208


if __name__ == "__main__":
    with open("2020/data/day14_input.txt") as f:
        instructions = f.readlines()

    program = InitializationProgramV1()
    program.process_instructions(instructions)
    result = program.sum_memory()
    print(f"Part 1 is {result}")

    program = InitializationProgramV2()
    program.process_instructions(instructions)
    result = program.sum_memory()
    print(f"Part 2 is {result}")
