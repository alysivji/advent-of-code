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

const part1 = (batteryBanks: number[][]): number => {
  // find each bank's joltage -- largest number we can put together
  // sum all joltages

  const joltages: number[] = [];

  for (const bank of batteryBanks) {
    // find largest number in 0 to n-1 elements
    const firstDigit = bank.slice(0, -1).sort((a, b) => b - a)[0]!;

    // first largest number in numbers after first digit
    const secondDigit = bank
      .slice(bank.indexOf(firstDigit) + 1)
      .sort((a, b) => b - a)[0]!;

    joltages.push(firstDigit * 10 + secondDigit);
  }

  return joltages.reduce((acc, value) => acc + value);
};

const testBatteryBanks = parseInput(TEST_INPUT);

const puzzleInput = fs.readFileSync("data/day03_input.txt").toString();
const batteryBanks = parseInput(puzzleInput);

assert(part1(testBatteryBanks) === 357, "part 1 test failed");
console.log("part1", part1(batteryBanks));
