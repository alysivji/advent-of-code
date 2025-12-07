import assert from "node:assert";
import fs from "node:fs";
import os from "node:os";

const TEST_INPUT = `123 328  51 64
 45 64  387 23
  6 98  215 314
*   +   *   +  `;
const puzzleInput = fs.readFileSync("data/day06_input.txt").toString();

type Worksheet = {
  rows: number[][];
  operators: string[];
};

const solveWorksheet = (worksheet: Worksheet, cephalopod: boolean = false) => {
  return worksheet.operators
    .map((operator, index) => {
      let numbers;
      if (cephalopod === false) {
        numbers = worksheet.rows.map((row) => row[index]!);
      } else {
        numbers = worksheet.rows[index] || [];
      }

      const initialValue = operator === "*" ? 1 : 0;
      return numbers.reduce(
        (acc, value) => (operator === "*" ? acc * value : acc + value),
        initialValue,
      );
    })
    .reduce((acc, value) => acc + value);
};

const parseInputPart1 = (input: string): Worksheet => {
  const parsedInput = input
    .trim()
    .split(os.EOL)
    .map((line) => line.trim().split(/\s+/));

  return {
    rows: parsedInput.slice(0, -1).map((row) => row.map(Number)!),
    operators: parsedInput.slice(-1)[0]!,
  };
};

const parseInputPart2 = (input: string) => {
  const lines = input.split(os.EOL).filter((value) => value !== "");

  const numberLines = lines.slice(0, -1);
  const operatorLine = lines.slice(-1)[0]!;

  const rows: number[][] = [];
  const operators: string[] = [];

  const longestNumberLine = Math.max(...numberLines.map((line) => line.length));

  let currentOp = "";
  let numbers: number[] = [];
  for (let index = 0; index < longestNumberLine; index++) {
    const op = operatorLine[index];
    if (op === "+") {
      currentOp = "+";
    } else if (op === "*") {
      currentOp = "*";
    }

    const number = Number(
      numberLines
        .map((value) => value[index] || "")
        .reduce((acc, value) => acc + value)
        .trim(),
    );

    if (number === 0) {
      rows.push(numbers);
      operators.push(currentOp);
      numbers = [];
      continue;
    } else if (index === longestNumberLine - 1) {
      numbers.push(number);
      rows.push(numbers);
      operators.push(currentOp);
      numbers = [];
      continue;
    } else {
      numbers.push(number);
    }
  }

  return {
    rows: rows,
    operators: operators,
  };
};

const testWorksheetPart1 = parseInputPart1(TEST_INPUT);
const worksheetPart1 = parseInputPart1(puzzleInput);

assert(solveWorksheet(testWorksheetPart1) === 4277556, "part 1 is incorrect");
console.log("part 1:", solveWorksheet(worksheetPart1));

const testWorksheetPart2 = parseInputPart2(TEST_INPUT);
const worksheetPart2 = parseInputPart2(puzzleInput);

assert(
  solveWorksheet(testWorksheetPart2, true) === 3263827,
  "part 2 is incorrect",
);
console.log("part 2:", solveWorksheet(worksheetPart2, true));
