from itertools import cycle


def load_input(filename):
    with open(filename, "r") as f:
        lines = f.readlines()
    return lines


def visited_twice(values):
    total = 0
    visited = set([total])
    for item in cycle(values):
        total += item
        if total in visited:
            return total
        visited.add(total)


assert visited_twice([+1, -1]) == 0
assert visited_twice([+3, +3, +4, -2, -4]) == 10
assert visited_twice([-6, +3, +8, +5, -6]) == 5
assert visited_twice([+7, +7, -2, -7, -4]) == 14


if __name__ == "__main__":
    values = load_input("day1_input.txt")
    values = [int(line.strip()) for line in values]

    print(sum(values))
    print(visited_twice(values))
