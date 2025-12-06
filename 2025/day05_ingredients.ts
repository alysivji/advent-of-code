import assert from "node:assert";
import fs from "node:fs";
import os from "node:os";

const TEST_INPUT = `3-5
10-14
16-20
12-18

1
5
8
11
17
32`;

type Range = {
  start: number;
  end: number;
};

type Ingredients = {
  fresh: Range[];
  available: number[];
};

const parseInput = (input: string): Ingredients => {
  const parts = input.trimEnd().split(os.EOL + os.EOL);

  const fresh = [];
  for (const freshRange of parts[0]!.split(os.EOL)) {
    const parts = freshRange.split("-");
    fresh.push({
      start: Number(parts[0]),
      end: Number(parts[1]),
    });
  }

  const available = [];
  for (const availableIngredient of parts[1]!.split(os.EOL)) {
    available.push(Number(availableIngredient));
  }

  return { fresh, available };
};

const part1 = (ingredients: Ingredients) => {
  // count number of available ingredients that fall within the range

  const availableFreshIngredients = new Set<number>();
  for (const availableIngredient of ingredients.available) {
    for (const freshRange of ingredients.fresh) {
      if (
        availableIngredient >= freshRange.start &&
        availableIngredient <= freshRange.end
      ) {
        availableFreshIngredients.add(availableIngredient);
      }
    }
  }

  return availableFreshIngredients.size;
};

const part2 = (ingredients: Ingredients) => {
  // sorting the range makes it easier to check
  const rangesToCheck = ingredients.fresh.sort(
    (range1, range2) => range1.start - range2.start,
  );

  const mergedRanges: Range[] = [rangesToCheck[0]!];
  for (const rangeToCheck of rangesToCheck.slice(1)) {
    const lastRangeInsered = mergedRanges.pop()!;

    if (lastRangeInsered.end < rangeToCheck.start) {
      mergedRanges.push(lastRangeInsered);
      mergedRanges.push(rangeToCheck);
      continue;
    }

    const combinedRange = {
      start: lastRangeInsered.start,
      end: Math.max(...[lastRangeInsered.end, rangeToCheck.end]),
    };
    mergedRanges.push(combinedRange);
  }

  return mergedRanges
    .map((range) => range.end - range.start + 1)
    .reduce((acc, value) => acc + value);
};

const testIngredients = parseInput(TEST_INPUT);

const puzzleInput = fs.readFileSync("data/day05_input.txt").toString();
const ingredients = parseInput(puzzleInput);

assert(part1(testIngredients) === 3, "part 1 test failed");
console.log("part1", part1(ingredients));

assert(part2(testIngredients) === 14, "part 2 test failed");
console.log("part2", part2(ingredients));
