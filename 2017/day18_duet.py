"""Advent of Code -- Day 18

http://adventofcode.com/2017/day/18"""

from collections import defaultdict, deque
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


class Computer(object):

    def __init__(self, program_id, program_queue, other_queue):
        self.program_id = program_id

        self.values = defaultdict(int)
        self.values['p'] = self.program_id

        self.rcv_queue = program_queue
        self.snd_queue = other_queue
        self.send_count = 0

    def process_instruction(self, instruction_string):
        instruction = instruction_string.split(' ')
        command = instruction[0]
        register = instruction[1]

        if len(instruction) == 2:
            if command == 'snd':
                self.snd_queue.append(self.values[register])
                self.send_count += 1
            elif command == 'rcv':
                if len(self.rcv_queue) > 0:
                    self.values[register] = self.rcv_queue.popleft()
                    return NextInstruction(True, 1)
                return NextInstruction(True, 0)
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


def calculate_number_of_times_program1_sends_value(instructions):
    # todo, print and walk thru via pdb or pudb
    # use pudb to figure out what's up

    program0_queue = deque()
    program1_queue = deque()

    program0 = Computer(0, program0_queue, program1_queue)
    program1 = Computer(1, program1_queue, program0_queue)

    curr_line_program0 = 0
    curr_line_program1 = 0

    while True:
        continue_program0, steps_program0 = (
            program0.process_instruction(instructions[curr_line_program0]))
        continue_program1, steps_program1 = (
            program1.process_instruction(instructions[curr_line_program1]))

        print(continue_program0, steps_program0)
        print(continue_program1, steps_program1)

        # deadlock
        if steps_program0 == 0 and steps_program1 == 0:
            return program1.send_count

        curr_line_program0 += steps_program0
        curr_line_program1 += steps_program1


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

TEST_INPUT_DUET = """snd 1
snd 2
snd p
rcv a
rcv b
rcv c
rcv d"""

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

    test_instructions_problem2 = {}
    for count, line in enumerate(TEST_INPUT_DUET.split('\n')):
        test_instructions_problem2[count] = line

    assert calculate_number_of_times_program1_sends_value(test_instructions_problem2) == 3
    print(calculate_number_of_times_program1_sends_value(instructions))
