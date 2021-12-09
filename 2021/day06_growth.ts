import assert from "assert";
import fs from "fs";

const stepPart1 = (fishAges: number[]): number[] => {
  const fishAgesUpdate = fishAges.map((value) => value - 1);
  fishAgesUpdate.forEach((value, index, array) => {
    if (value === -1) {
      array.push(8);
    }
  });
  return fishAgesUpdate.map((value) => {
    if (value == -1) {
      return 6;
    } else {
      return value;
    }
  });
};

const part1 = (fishAges: number[], numDays: number): number => {
  let fishAgesCopy = fishAges.slice();
  for (let i = 0; i < numDays; i++) {
    fishAgesCopy = stepPart1(fishAgesCopy);
  }
  return fishAgesCopy.length;
};

const parseInputPart1 = (inputString: string): number[] => {
  return inputString.split(",").map(Number);
};

const TEST_INPUT = "3,4,3,1,2";
assert(part1(parseInputPart1(TEST_INPUT), 18) == 26);
assert(part1(parseInputPart1(TEST_INPUT), 80) == 5934);

const laternfishAges = fs
  .readFileSync("2021/data/day06_input.txt")
  .toString()
  .trim();
console.log(part1(parseInputPart1(laternfishAges), 80));

const parseInputPart2 = (inputString: string): number[] => {
  const fishAges = inputString.split(",").map(Number);
  return fishAges.reduce((acc, currValue) => {
    acc[currValue] += 1;
    return acc;
  }, Array(9).fill(0));
};

const stepPart2 = (fishAges: number[]): number[] => {
  const fishAgesUpdate = fishAges.slice();
  const fishReadyToGiveBirth = fishAgesUpdate.shift() || 0;
  fishAgesUpdate.push(fishReadyToGiveBirth);
  fishAgesUpdate[6] += fishReadyToGiveBirth;
  return fishAgesUpdate;
};

const part2 = (fishAges: number[], numDays: number): number => {
  let fishAgesCopy = fishAges.slice();
  for (let i = 0; i < numDays; i++) {
    fishAgesCopy = stepPart2(fishAgesCopy);
  }
  return fishAgesCopy.reduce((a, b) => a + b);
};

assert(part2(parseInputPart2(TEST_INPUT), 256) == 26984457539);
console.log(part2(parseInputPart2(laternfishAges), 256));
