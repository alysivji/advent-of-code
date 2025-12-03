import assert from "node:assert";
import fs from "node:fs";
import os from "node:os";

const TEST_INPUT = `987654321111111
811111111111119
234234234234278
818181911112111`;

const parseInput = (inputText: string): number[][] => {
  return inputText
    .trimEnd()
    .split(os.EOL)
    .map((bank) => bank.split("").map(Number));
};

const calculateTotalOutputJoltage = (
  batteryBanks: number[][],
  numBatteriesToUse: number,
): number => {
  // find each bank's joltage -- largest number with `numBatteriesToUse` digits
  // sum all joltages

  const joltages: number[] = [];

  for (const bank of batteryBanks) {
    const batteriesToUse: number[] = [];

    let start = 0;
    while (batteriesToUse.length < numBatteriesToUse) {
      const end = bank.length - numBatteriesToUse + batteriesToUse.length + 1;
      const batteriesToExamine = bank.slice(start, end);

      const largestDigit = [...batteriesToExamine].sort((a, b) => b - a)[0]!;

      batteriesToUse.push(largestDigit);

      start += batteriesToExamine.indexOf(largestDigit) + 1;
    }

    const joltage = batteriesToUse
      .map((value, idx) => value * 10 ** (batteriesToUse.length - idx - 1))
      .reduce((acc, value) => acc + value);

    joltages.push(joltage);
  }

  return joltages.reduce((acc, value) => acc + value);
};

const testBatteryBanks = parseInput(TEST_INPUT);

const puzzleInput = fs.readFileSync("data/day03_input.txt").toString();
const batteryBanks = parseInput(puzzleInput);

assert(
  calculateTotalOutputJoltage(testBatteryBanks, 2) === 357,
  "part 1 test failed",
);
console.log("part1", calculateTotalOutputJoltage(batteryBanks, 2));

assert(
  calculateTotalOutputJoltage(testBatteryBanks, 12) === 3121910778619,
  "part 2 test failed",
);
console.log("part2", calculateTotalOutputJoltage(batteryBanks, 12));
