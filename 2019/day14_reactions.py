from collections import deque
import re
from typing import NamedTuple, List, Dict, Set


class Ingredient(NamedTuple):
    qty: int
    chemical: str


TEST_INPUT = """9 ORE => 2 A
8 ORE => 3 B
7 ORE => 5 C
3 A, 4 B => 1 AB
5 B, 7 C => 1 BC
4 C, 1 A => 1 CA
2 AB, 3 BC, 4 CA => 1 FUEL"""

REACTION_REGEX = r"(?P<input>\d+ \w+,? )*=> (?P<output>\d+ \w+)"


def create_recipe_dict(lines):
    all_recipes = {}

    p = re.compile(REACTION_REGEX)
    for idx, line in enumerate(lines):
        cleaned_line = line.strip()
        m = p.match(cleaned_line)

        inputs = m.group("input").strip().split(", ")
        cleaned_inputs = []
        for r in inputs:
            qty, chemical = r.split(" ")
            item = Ingredient(qty=int(qty), chemical=chemical)
            cleaned_inputs.append(item)

        qty, chemical = m.group("output").split(" ")
        output = Ingredient(qty=int(qty), chemical=chemical)

        all_recipes[output] = cleaned_inputs
    return all_recipes


def ore_required_for_fuel(recipes: dict) -> int:
    steps_to_complete = deque([recipes[Ingredient(qty=1, chemical='FUEL')]])
    ore_needed = 0

    while steps_to_complete:
        curr_step: Ingredient = steps_to_complete.popleft()
        for ingredient in curr_step:
            if ingredient.chemical == "ORE":
                ore_needed += ingredient.qty
            else:
                # TODO need to figure out how to handle
                # ingredients_required = recipes[ingredient.chemical] * ingredient.qty
                # steps_to_complete.extend(ingredients_required)
                pass

    return ore_needed


def test_fuel_required():
    recipes = create_recipe_dict(TEST_INPUT.split("\n"))
    ore_required = ore_required_for_fuel(recipes)

    assert False


if __name__ == "__main__":
    output = create_recipe_dict()

    for item in output:
        print(item)
