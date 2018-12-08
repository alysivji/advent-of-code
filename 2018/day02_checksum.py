from collections import Counter
from typing import Generator, List, Optional


def load_input(filename: str) -> List[str]:
    with open(filename, "r") as f:
        lines = f.readlines()
    return [line.strip() for line in lines]


def calculate_checksum(boxes: List[str]) -> int:
    appears_twice = 0
    appears_thrice = 0

    for box in boxes:
        counts = Counter(box)
        values = set(counts.values())

        if 2 in values:
            appears_twice += 1
        if 3 in values:
            appears_thrice += 1

    return appears_twice * appears_thrice


test_input_part_one = """abcdef
bababc
abbcde
abcccd
aabcdd
abcdee
ababab"""

assert calculate_checksum(test_input_part_one.split()) == 12


def find_similar_boxes(boxes: List[str]) -> Generator:
    box_char_count = [Counter(box) for box in boxes]

    for i in range(len(box_char_count)):
        for j in range(i, len(box_char_count)):
            box1 = box_char_count[i]
            box2 = box_char_count[j]
            diff = box1 - box2
            if len(diff) == 1:
                yield boxes[i], boxes[j]


def find_prototype_box_common_letters(boxes: List[str]) -> Optional[str]:
    for box1, box2 in find_similar_boxes(boxes):
        diff = 0
        same = ""
        for letter1, letter2 in zip(list(box1), list(box2)):
            if letter1 != letter2:
                diff += 1
            else:
                same += letter1
        if diff == 1:
            return same
    return None


test_input_part_two = """abcde
fghij
klmno
pqrst
fguij
axcye
wvxyz"""

assert find_prototype_box_common_letters(test_input_part_two.split()) == "fgij"


def find_prototype_box_single_pass(boxes: List[str]) -> Optional[str]:
    for i in range(len(boxes)):
        for j in range(i, len(boxes)):
            diff = 0
            same = ""
            for letter1, letter2 in zip(list(boxes[i]), list(boxes[j])):
                if letter1 != letter2:
                    diff += 1
                    if diff > 1:
                        break
                else:
                    same += letter1
            if diff == 1:
                return same
    return None


assert find_prototype_box_single_pass(test_input_part_two.split()) == "fgij"

if __name__ == "__main__":
    boxes = load_input("day02_input.txt")
    print(calculate_checksum(boxes))
    print(find_prototype_box_common_letters(boxes))
    print(find_prototype_box_single_pass(boxes))
