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

const findValidEquations = (equations: Equation[]) => {
  const isValid = (equation: Equation): boolean => {
    // base case
    if (equation.nums.length === 1) return equation.value === equation.nums[0];

    // recursive case
    const lastNum = equation.nums.slice(-1)[0];

    const reducedEquation: Equation = {
      value: equation.value - lastNum,
      nums: equation.nums.slice(0, -1),
    };
    const subtractNumberCase = isValid(reducedEquation);
    let multipleNumberCase = false;

    if (equation.value % lastNum === 0) {
      const reducedEquation: Equation = {
        value: equation.value / lastNum,
        nums: equation.nums.slice(0, -1),
      };
      multipleNumberCase = isValid(reducedEquation);
    }

    return subtractNumberCase || multipleNumberCase;
  };

  return equations.filter((equation) => isValid(equation));
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

const puzzleInput = fs.readFileSync("data/day07_input.txt").toString();
const equations = parseInput(puzzleInput);
const validEquations = findValidEquations(equations);
console.log(calculateTotalCalibrationResult(validEquations));
