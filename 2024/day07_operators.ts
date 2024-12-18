import assert from "assert";
import fs from "fs";

const TEST_INPUT = `190: 10 19
3267: 81 40 27
83: 17 5
156: 15 6
7290: 6 8 6 15
161011: 16 10 13
192: 17 8 14
21037: 9 7 18 13
292: 11 6 16 20
`;

type Equation = {
  value: number;
  nums: number[];
};

const parseInput = (input: string): Equation[] => {
  return input
    .trim()
    .split("\n")
    .map((line) => {
      const parts = line.split(": ");
      const value = Number(parts[0]);
      const nums = parts[1].split(" ").map(Number);
      return { value, nums };
    });
};

const findValidEquations = (
  equations: Equation[],
  isPart2: boolean = false,
) => {
  const isValid = (eq: Equation): boolean => {
    // base case
    if (eq.nums.length === 1) return eq.nums[0] === eq.value;

    // recursive case
    const firstValue = eq.nums.shift()!;

    // addition
    const addArr = [...eq.nums];
    addArr[0] = addArr[0] + firstValue;
    const addEquation: Equation = {
      value: eq.value,
      nums: addArr,
    };
    const addIsValid = isValid(addEquation);

    // multiplication
    const multiArr = [...eq.nums];
    multiArr[0] = multiArr[0] * firstValue;
    const multEquation: Equation = {
      value: eq.value,
      nums: multiArr,
    };
    const multIsValid = isValid(multEquation);

    if (!isPart2) return addIsValid || multIsValid;

    // concatenation
    const concatArr = [...eq.nums];
    concatArr[0] = Number(String(firstValue) + String(concatArr[0]));
    const concatEq: Equation = {
      value: eq.value,
      nums: concatArr,
    };
    const concatIsValid = isValid(concatEq);

    return addIsValid || multIsValid || concatIsValid;
  };

  return structuredClone(equations).filter((equation) => isValid(equation));
};

const calculateTotalCalibrationResult = (equations: Equation[]) => {
  return equations
    .map((equation) => equation.value)
    .reduce((num, acc) => num + acc, 0);
};

const testEquations = parseInput(TEST_INPUT);
const testValidEquations = findValidEquations(testEquations);
assert(
  calculateTotalCalibrationResult(testValidEquations) === 3749,
  "part 1 test failed",
);

const testValidEquationsPart2 = findValidEquations(testEquations, true);
assert(
  calculateTotalCalibrationResult(testValidEquationsPart2) === 11387,
  "part 2 test failed",
);

const puzzleInput = fs.readFileSync("data/day07_input.txt").toString();
const equations = parseInput(puzzleInput);

console.time("part1");
const validEquations = findValidEquations(equations);
console.log("Part 1:", calculateTotalCalibrationResult(validEquations));
console.timeEnd("part1");

console.time("part2");
const validEquationsPart2 = findValidEquations(equations, true);
console.log("Part 2:", calculateTotalCalibrationResult(validEquationsPart2));
console.timeEnd("part2");
