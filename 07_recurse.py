"""Advent of Code 2017 -- Day 7

http://adventofcode.com/2017/day/7
"""

from typing import Dict, List, Set, Tuple

SUBPROGRAM_FLAG = '-> '
INPUT = '07_input.txt'
TEST_INPUT = '07_test_input.txt'

# SivjiNote: Solved Part 1 in a very inefficient way
#
# def get_all_programs_and_subprograms(file: str) -> Tuple[List[str], List[str]]:
#     with open(file, 'r') as f:
#         all_programs = []
#         all_subprograms = []
#         for line in f.readlines():
#             program, subprogram = (
#                 current_programs_and_subprograms(line.strip()))
#             all_programs.append(program)
#             all_subprograms.extend(subprogram)
#     return all_programs, all_subprograms


# def get_bottom_program(program: List[str], subprograms: List[str]) -> Set:
#     return set(programs) - set(subprograms)

def current_programs_and_subprograms(stack: str) -> Tuple[str, List[str]]:
    curr_program = stack.split()[0]
    subprograms: List[str] = []

    if stack.find(SUBPROGRAM_FLAG) > 0:
        subprograms = stack.split(SUBPROGRAM_FLAG)[1].split(', ')

    return (curr_program, subprograms)


def parse_call_stack(prog_info: str) -> Tuple[Dict, Dict, List]:
    weights = {}
    subprograms = {}
    all_subprograms = []
    with open(prog_info, 'r') as f:
        for line in f.readlines():
            name, tower = current_programs_and_subprograms(line.strip())

            weight = int(line[line.find('(') + 1: line.find(')')])
            weights[name] = weight

            if tower:
                subprograms[name] = tower
                all_subprograms.extend(tower)
    return weights, subprograms, all_subprograms


def get_weight(node):
    """Recursively get weight

    As a side effect, let's answer the question
    """
    # if leaf
    if node in leaves:
        return weights[node]

    tower_weights = []
    additional_info = {}
    for subprogram in subprograms[node]:
        subprogram_weight = get_weight(subprogram)
        additional_info[subprogram] = get_weight(subprogram)
        tower_weights.append(subprogram_weight)

    total_weight = sum(tower_weights) + weights[node]

    if len(set(tower_weights)) > 1:
        print(additional_info, set(tower_weights))

    return total_weight


if __name__ == "__main__":
    # programs, subprograms = get_all_programs_and_subprograms(TEST_INPUT)
    # assert get_bottom_program(programs, subprograms) == {'tknk'}

    # programs, subprograms = get_all_programs_and_subprograms(INPUT)
    # print(get_bottom_program(programs, subprograms))
    weights, subprograms, all_subprograms = parse_call_stack(INPUT)
    root = (set(weights.keys()) - set(all_subprograms)).pop()
    print(f'Bottom Program: {root}')

    # get the weight of the leaves in
    leaves = set(weights.keys()) - set(subprograms.keys())

    get_weight(root)
    print('fin.')
