"""Advent of Code 2017 -- Day 13

http://adventofcode.com/2017/day/13"""

from typing import Dict, List

TEST_INPUT = """0: 3
1: 2
4: 4
6: 4"""


def build_firewall(layers: Dict[int, int]) -> Dict[int, List]:
    """This function builds a firewall

    Each list holds the record of where the scanner currently is and in which
    direction it will move next"""
    firewall: Dict[int, List] = {}

    counter = 0
    num_layers = max(layers.keys())

    while counter <= num_layers:
        if counter in layers:
            scanner = [None for i in range(layers[counter])]
            scanner[0] = 'Forward'
            firewall[counter] = scanner
        else:
            firewall[counter] = []  # defaultdict would not be as explicit

        counter += 1

    return firewall


def calculate_penalty(
        firewall: Dict[int, List],
        delay: int=0,
        early_exit: bool=False) -> int:
    packet_position = 0
    total_penalty = 0
    num_layers = max(firewall.keys())

    for _ in range(delay):
        firewall = next_step(firewall)

    while packet_position <= num_layers:
        caught = assess_penalty(firewall[packet_position])
        if caught:
            total_penalty += len(firewall[packet_position]) * packet_position

            if early_exit:
                return 1

        firewall = next_step(firewall)

        packet_position += 1

    return total_penalty


def next_step(curr_firewall: Dict[int, List]) -> Dict[int, List]:
    next_firewall = curr_firewall.copy()
    for range_, scanner in next_firewall.items():
        if len(scanner) > 0:
            next_firewall[range_] = scanner_next_position(scanner)

    return next_firewall


def scanner_next_position(scanner: List) -> List:
    # find forward
    try:
        pos = scanner.index('Forward')
        if pos < (len(scanner) - 1):
            scanner = [None for i in range(len(scanner))]
            scanner[pos + 1] = 'Forward'

            # at the end of the list
            if pos + 1 == (len(scanner) - 1):
                scanner[pos + 1] = 'Backward'

            return scanner
    except ValueError:
        pos = scanner.index('Backward')
        if pos > 0:
            scanner = [None for i in range(len(scanner))]
            scanner[pos - 1] = 'Backward'

        # at the start of the list
        if (pos - 1) == 0:
            scanner = [None for i in range(len(scanner))]
            scanner[0] = 'Forward'

        return scanner

    raise


def assess_penalty(scanner: List) -> bool:
    if len(scanner) > 0:
        if scanner[0] == 'Forward':
            return True

    return False


def find_optimal_delay(firewall: Dict[int, List]) -> int:
    delay = 0
    while True:
        penalty = calculate_penalty(firewall, delay, early_exit=True)
        if penalty == 0:
            return delay
        else:
            delay += 1


if __name__ == '__main__':
    layers: Dict[int, int] = {}
    for line in TEST_INPUT.split('\n'):
        range_, depth = line.split(': ')
        layers[int(range_)] = int(depth)

    test_firewall = build_firewall(layers)
    assert calculate_penalty(test_firewall) == 24
    assert find_optimal_delay(test_firewall) == 10

    layers: Dict[int, int] = {}
    with open('13_input.txt', 'r') as f:
        for line in f.readlines():
            range_, depth = line.strip().split(': ')
            layers[int(range_)] = int(depth)

    firewall = build_firewall(layers)
    print(calculate_penalty(firewall))
    print(find_optimal_delay(firewall))
