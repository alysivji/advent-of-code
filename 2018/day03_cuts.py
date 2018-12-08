from collections import defaultdict
import re
from typing import Dict, List, NamedTuple, Tuple

CUT = r"#(?P<num>\d+) @ (?P<left>\d+),(?P<top>\d+): (?P<width>\d+)+x(?P<height>\d+)"


class Claim(NamedTuple):
    num: int
    left: int
    top: int
    width: int
    height: int


def load_input(lines: List[str]) -> List[Claim]:
    p = re.compile(CUT)
    claims = []
    for line in lines:
        cleaned_line = line.strip()
        m = p.match(cleaned_line)
        claim = Claim(
            num=int(m.group("num")),
            left=int(m.group("left")),
            top=int(m.group("top")),
            width=int(m.group("width")),
            height=int(m.group("height")),
        )
        claims.append(claim)
    return claims


def load_input_improved(lines: List[str]) -> List[Claim]:
    claims = [Claim(*map(int, re.findall(r"-?\d+", line))) for line in lines]
    return claims


def process_cloth(claims: List[Claim]) -> Dict[Tuple[int, int], List[int]]:
    cloth: Dict[Tuple[int, int], List[int]] = defaultdict(list)
    for claim in claims:
        for x in range(claim.left + 1, claim.left + claim.width + 1):
            for y in range(claim.top + 1, claim.top + claim.height + 1):
                cloth[(x, y)].append(claim.num)
    return cloth


def find_overlap(claims: List[Claim]) -> int:
    cloth = process_cloth(claims)
    overlap = 0
    for key, value in cloth.items():
        if len(value) > 1:
            overlap += 1
    return overlap


def nonoverlapping_claim(claims: List[Claim]) -> int:
    all_claims = {claim.num: claim for claim in claims}
    cloth = process_cloth(claims)

    for key, value in cloth.items():
        if len(value) > 1:
            for claim in value:
                all_claims.pop(claim, None)

    if len(all_claims) > 1:
        raise ValueError
    return list(all_claims.keys())[0]


test_input = """#1 @ 1,3: 4x4
#2 @ 3,1: 4x4
#3 @ 5,5: 2x2""".split("\n")
test_claims = load_input_improved(test_input)
assert find_overlap(test_claims) == 4
assert nonoverlapping_claim(test_claims) == 3


if __name__ == "__main__":
    with open("day03_input.txt", "r") as f:
        lines = f.readlines()
    claims = load_input_improved(lines)
    print(find_overlap(claims))
    print(nonoverlapping_claim(claims))
