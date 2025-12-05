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

// options
// |----| |---|
const combineOverlaps = (ranges: Range[]) => {
  const newRanges: Range[] = [];

  for (let i = 0; i <= ranges.length - 1; i++) {
    for (let j = i + 1; j <= ranges.length - 1; j++) {
      const firstRange = ranges[i]!;
      const secondRange = ranges[j]!;

      console.log("firstRange", firstRange);
      console.log("secondRange", secondRange);

      // no overlap
      if (
        firstRange.end < secondRange.start &&
        secondRange.end < firstRange.start
      ) {
        console.log("test1");
        newRanges.push(firstRange);
        newRanges.push(secondRange);
        continue;
      }

      // second range within first range
      if (
        firstRange.start < secondRange.start &&
        firstRange.end > secondRange.end
      ) {
        console.log("test2");
        newRanges.push(firstRange);
        continue;
      }

      // first range contains second range start -- second range end is past first range end
      if (
        firstRange.start < secondRange.start &&
        secondRange.start < firstRange.end &&
        firstRange.end < secondRange.end
      ) {
        console.log("test3");
        newRanges.push({ start: firstRange.start, end: secondRange.end });
        continue;
      }

      // second range contains first range start -- first range end is past second range end
      if (
        secondRange.start < firstRange.start &&
        firstRange.start < secondRange.end &&
        secondRange.end < firstRange.start
      ) {
        console.log("test4");
        newRanges.push({ start: secondRange.start, end: firstRange.end });
        continue;
      }
    }
  }

  console.log("how", newRanges);

  return newRanges;
};

const part2 = (ingredients: Ingredients) => {
  let rangesToCheck = ingredients.fresh;
  console.log(rangesToCheck);
  let numRanges;

  do {
    numRanges = rangesToCheck.length;
    const updatedRanges = combineOverlaps(rangesToCheck)!;
    rangesToCheck = updatedRanges;
  } while (numRanges !== rangesToCheck.length);
};

const testIngredients = parseInput(TEST_INPUT);

const puzzleInput = fs.readFileSync("data/day05_input.txt").toString();
const ingredients = parseInput(puzzleInput);

assert(part1(testIngredients) === 3, "part 1 test failed");
console.log("part1", part1(ingredients));

console.log(part2(testIngredients));
// assert(part2(testIngredients) === 14, "part 2 test failed");
// console.log("part2", part2(ingredients));
