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


def calculate_penalty(firewall: Dict[int, List],
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

    raise RuntimeError('should never get here')


def assess_penalty(scanner: List) -> bool:
    if len(scanner) > 0:
        if scanner[0] == 'Forward':
            return True

    return False


def find_optimal_delay(firewall: Dict[int, List]) -> int:
    """Not very efficient. Need to come up with a better way
    """
    delay = 0
    while True:
        penalty = calculate_penalty(firewall, delay, early_exit=True)
        if penalty == 0:
            return delay
        else:
            delay += 1


class Scanner:
    def __init__(self, range_, depth):
        self.counter = range_
        self.depth = depth

    def increment_delay(self):
        """True means it is safe to cross; False means caught
        """
        while True:
            if self.depth == 0:
                yield True
            else:
                if self.counter % ((self.depth - 1) * 2) == 0:
                    yield False
                else:
                    yield True

            self.counter += 1


def find_delay(layers) -> int:
    # Build Firewall
    firewall = []

    counter = 0
    num_layers = max(layers.keys())
    while counter <= num_layers:
        if counter in layers:
            scanner = Scanner(counter, layers[counter])
        else:
            scanner = Scanner(counter, 0)

        scanner_iter = scanner.increment_delay()
        firewall.append(scanner_iter)
        counter += 1

    # import pdb; pdb.set_trace()

    delay = 0
    while True:
        delay_state = [next(scanner) for scanner in firewall]

        if all(delay_state):
            return delay

        delay += 1

    return firewall


if __name__ == '__main__':
    test_layers: Dict[int, int] = {}
    for line in TEST_INPUT.split('\n'):
        range_, depth = line.split(': ')
        test_layers[int(range_)] = int(depth)

    test_firewall = build_firewall(test_layers)
    assert calculate_penalty(test_firewall) == 24
    assert find_optimal_delay(test_firewall) == 10

    layers: Dict[int, int] = {}
    with open('13_input.txt', 'r') as f:
        for line in f.readlines():
            range_, depth = line.strip().split(': ')
            layers[int(range_)] = int(depth)

    firewall = build_firewall(layers)
    print(calculate_penalty(firewall))

    # new method
    assert find_delay(test_layers) == 10
    print(find_delay(test_layers))
    # find_delay(layers)

