from collections import defaultdict, deque
from typing import Dict, List, NamedTuple
import re


class Bag(NamedTuple):
    number: int
    color: str


TEST_INPUT = """light red bags contain 1 bright white bag, 2 muted yellow bags.
dark orange bags contain 3 bright white bags, 4 muted yellow bags.
bright white bags contain 1 shiny gold bag.
muted yellow bags contain 2 shiny gold bags, 9 faded blue bags.
shiny gold bags contain 1 dark olive bag, 2 vibrant plum bags.
dark olive bags contain 3 faded blue bags, 4 dotted black bags.
vibrant plum bags contain 5 faded blue bags, 6 dotted black bags.
faded blue bags contain no other bags.
dotted black bags contain no other bags."""


def generate_bag_map(lines):
    bag_map = defaultdict(list)
    for line in lines:
        parent_bag, child_bags = line.split(" bags contain ")
        for child in child_bags.split(", "):
            m = re.match(r"(?P<number>\d+) (?P<color>.*) (bag|bags)", child)
            if m:
                bag = Bag(int(m.group("number")), m.group("color"))
                bag_map[parent_bag].append(bag)
            else:
                bag_map[parent_bag]

    return bag_map


def can_be_inside_how_many_bags(bag_map: Dict[str, List[Bag]], bag_color: str):
    seen = set()
    queue = deque([bag_color])

    while queue:
        current_bag = queue.popleft()

        for parent_bag_color, children_bags in bag_map.items():
            for child in children_bags:
                if child.color == current_bag:
                    if parent_bag_color not in seen:
                        seen.add(parent_bag_color)
                        queue.append(parent_bag_color)

    return len(seen)


bag_map = generate_bag_map(TEST_INPUT.split("\n"))
assert can_be_inside_how_many_bags(bag_map, "shiny gold") == 4


def count_total_bags_inside(bag_map: Dict[str, List[Bag]], bag_color: str):
    queue = deque([(1, bag_color)])
    total_bags = 0

    while queue:
        num_bags, bag_color = queue.popleft()
        total_bags += num_bags

        for num, color in bag_map[bag_color]:
            queue.append((num * num_bags, color))

    return total_bags - 1


assert count_total_bags_inside(bag_map, "shiny gold") == 32


if __name__ == "__main__":
    with open("2020/data/day07_input.txt") as f:
        bag_map = generate_bag_map(f.readlines())

    print(f"Part 1: {can_be_inside_how_many_bags(bag_map, 'shiny gold')}")
    print(f"Part 2: {count_total_bags_inside(bag_map, 'shiny gold')}")
