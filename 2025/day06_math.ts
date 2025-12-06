import assert from "node:assert";
import fs from "node:fs";
import os from "node:os";

const TEST_INPUT = `123 328  51 64
 45 64  387 23
  6 98  215 314
*   +   *   +  `;

type Worksheet = {
  rows: number[][];
  operators: string[];
};

const parseInput = (input: string): Worksheet => {
  const parsedInput = input
    .trim()
    .split(os.EOL)
    .map((line) => line.trim().split(/\s+/));

  return {
    rows: parsedInput.slice(0, -1).map((row) => row.map(Number)),
    operators: parsedInput.slice(-1)[0],
  };
};

const part1 = (worksheet: Worksheet) => {
  const results = worksheet.operators.map((operator, index) => {
    const numbers = worksheet.rows.map((row) => row[index]);
    const initialValue = operator === "*" ? 1 : 0;
    const a = numbers.reduce(
      (acc, value) => (operator === "*" ? acc * value : acc + value),
      initialValue,
    );
    return a;
  });
  return results.reduce((acc, value) => acc + value);
};

// const testWorksheet = parseInput(TEST_INPUT);

const puzzleInput = fs.readFileSync("data/day06_input.txt").toString();
const puzzleWorksheet = parseInput(puzzleInput);

// assert(part1(testWorksheet) === 4277556, "part 1 is incorrect");
console.log("part 1:", part1(puzzleWorksheet));
