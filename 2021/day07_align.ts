import assert from "assert";
import fs from "fs";

const parseInput = (inputString: string): number[] => {
  return inputString.split(",").map(Number);
};

const alignCrabs = (crabPositions: number[]): number => {
  const maxValue = crabPositions.reduce((max, val) => (max > val ? max : val));
  const fuelSpentInitial = Array(maxValue + 1).fill(0);
  const fuelSpent = fuelSpentInitial.map((value, index) => {
    let fuelSpentGoingToPosition = 0;
    crabPositions.forEach((value) => {
      fuelSpentGoingToPosition += Math.abs(value - index);
    });
    return fuelSpentGoingToPosition;
  });
  return fuelSpent.reduce((min, val) => (min < val ? min : val));
};

const TEST_INPUT = "16,1,2,0,4,2,7,1,2,14"
assert(alignCrabs(parseInput(TEST_INPUT)) == 37)

const crabPositions = fs
  .readFileSync("2021/data/day07_input.txt")
  .toString()
  .trim();
console.log(alignCrabs(parseInput(crabPositions)))

const alignCrabsPart2 = (crabPositions: number[]): number => {
  const maxValue = crabPositions.reduce((max, val) => (max > val ? max : val));
  const fuelSpentInitial = Array(maxValue + 1).fill(0);
  const fuelSpent = fuelSpentInitial.map((value, index) => {
    let fuelSpentGoingToPosition = 0;
    crabPositions.forEach((value) => {
      const n = Math.abs(value - index);
      // https://en.wikipedia.org/wiki/1_%2B_2_%2B_3_%2B_4_%2B_%E2%8B%AF
      fuelSpentGoingToPosition += (n * (n + 1) / 2)
    });
    return fuelSpentGoingToPosition;
  });
  return fuelSpent.reduce((min, val) => (min < val ? min : val));
};

assert(alignCrabsPart2(parseInput(TEST_INPUT)) == 168)
console.log(alignCrabsPart2(parseInput(crabPositions)))
