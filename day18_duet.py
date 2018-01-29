"""Advent of Code -- Day 18

http://adventofcode.com/2017/day/18"""

from collections import defaultdict
from typing import NamedTuple


class NextInstruction(NamedTuple):
    continue_program: bool
    steps: int


class SoundCard(object):

    def __init__(self):
        self.values = defaultdict(int)
        self.last_sound_played = None
        self.recovers = None

    def process_instruction(self, instruction_string):
        instruction = instruction_string.split(' ')
        command = instruction[0]
        register = instruction[1]

        if len(instruction) == 2:
            if command == 'snd':
                self.last_sound_played = self.values[register]
            elif command == 'rcv':
                if self.values[register] != 0:
                    self.recovers = self.last_sound_played
                    return NextInstruction(False, self.recovers)
        else:
            operation_with_register = instruction[2] in self.values
            if operation_with_register:
                value = self.values[instruction[2]]
            else:
                value = int(instruction[2])

            if command == 'set':
                self.values[register] = value
            elif command == 'add':
                self.values[register] += value
            elif command == 'mul':
                self.values[register] *= value
            elif command == 'mod':
                self.values[register] = self.values[register] % value
            elif command == 'jgz':
                if self.values[register] > 0:
                    return NextInstruction(True, value)

        return NextInstruction(True, 1)


def calculate_value_of_recovered_frequency(instructions):
    # set up computer
    sound = SoundCard()
    curr_line = 0

    # loop thru instructions
    while True:
        continue_program, steps = (
            sound.process_instruction(instructions[curr_line]))

        if continue_program is False:
            return steps

        curr_line += steps
        stop_loop = curr_line < 0 or curr_line >= len(instructions)
        if stop_loop:
            break


TEST_INPUT = """set a 1
add a 2
mul a a
mod a 5
snd a
set a 0
rcv a
jgz a -1
set a 1
jgz a -2"""

if __name__ == '__main__':
    test_instructions = {}
    for count, line in enumerate(TEST_INPUT.split('\n')):
        test_instructions[count] = line

    assert calculate_value_of_recovered_frequency(test_instructions) == 4

    instructions = {}
    with open('day18_input.txt', 'r') as f:
        for count, line in enumerate(f.readlines()):
            instructions[count] = line.strip()

    print(calculate_value_of_recovered_frequency(instructions))
