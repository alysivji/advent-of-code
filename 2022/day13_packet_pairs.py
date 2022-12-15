import itertools
from typing import NamedTuple, Union


class Pair(NamedTuple):
    left: list
    right: list


def parseInput(filePath: str):
    with open(filePath, "r") as f:
        pairs = f.read().strip().split("\n\n")

    all_pairs = []
    for pair in pairs:
        left, right = pair.split("\n")
        all_pairs.append(Pair(eval(left), eval(right)))

    return all_pairs


def isPairInRightOrder(left, right, mixed_type=False) -> bool:
    print(left, right)
    cummulative = True
    if type(left) == int and type(right) == int:
        if left > right:
            cummulative = cummulative and False
    elif type(left) == int and type(right) == list:
        return isPairInRightOrder([left], right, mixed_type=True)
    elif type(left) == list and type(right) == int:
        return isPairInRightOrder(left, [right], mixed_type=True)
    elif type(left) == list and type(right) == list:
        for (l, r) in zip(left, right):
            if type(l) == type(r) == list:
                cummulative = cummulative and isPairInRightOrder(l, r, mixed_type=False)
            else:
                cummulative = cummulative and isPairInRightOrder(l, r, mixed_type=False)

        if mixed_type is False and len(left) > len(right):
            cummulative = cummulative and False

    return cummulative


def get_list(obj: Union[int, list]):
    return [obj] if isinstance(obj, int) else obj


def isPacketInRightOrder(p1: Union[list, int], p2: Union[list, int]) -> bool:
    cummulative = True

    print(p1, p2)
    left = get_list(p1)
    right = get_list(p2)
    for (l, r) in itertools.zip_longest(left, right):
        print(l, r)

        if r is None:
            cummulative = cummulative and False

        if l is None:
            cummulative = cummulative and True

        if isinstance(l, int) and isinstance(r, int):
            if l > r:
                cummulative = cummulative and False
        elif isinstance(l, list) and isinstance(r, list):
            for (sub_l, sub_r) in zip(l, r):
                cummulative = cummulative and isPacketInRightOrder(sub_l, sub_r)
            return cummulative

    return cummulative


def sumIndicesInRightOrder(pairs) -> int:
    total = 0
    for idx, pair in enumerate(pairs, start=1):
        result = isPacketInRightOrder(pair.left, pair.right)
        if result:
            total += idx
        print(idx, result)
        print("\n")
    return total


if __name__ == "__main__":
    pairs = parseInput("2022/data/day13_sample.txt")
    # assert sumIndicesInRightOrder(pairs) == 13

    # pairs = parseInput("2022/data/day13_input.txt")
    print(sumIndicesInRightOrder(pairs))
