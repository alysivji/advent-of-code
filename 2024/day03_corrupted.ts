import assert from "node:assert";
import fs from "fs";

const parseInput = (input: string) => {
  return input.trim().split("\n");
};

const findUncorrptedMemory = (
  section: string,
  conditionsEnabled: boolean = false,
) => {
  let PATTERN: RegExp;
  if (!conditionsEnabled) {
    PATTERN = new RegExp("mul\\(\\d+,\\d+\\)", "g");
  } else {
    PATTERN = new RegExp("mul\\(\\d+,\\d+\\)|do\\(\\)|don\\'t\\(\\)", "g");
  }
  return Array.from(section.matchAll(PATTERN)).map(String);
};

const runMultiplicationInstruction = (instruction: string) => {
  // instruction will look like mul(2,4)
  if (!instruction.startsWith("mul")) throw Error("unexpected instruction");

  const firstNum = Number(instruction.split("(")[1].split(",")[0]);
  const secondNum = Number(instruction.split(",")[1].split(")")[0]);
  return firstNum * secondNum;
};
assert(runMultiplicationInstruction("mul(2,4)") === 8);
assert(runMultiplicationInstruction("mul(5,5)") === 25);
assert(runMultiplicationInstruction("mul(11,8)") === 88);
assert(runMultiplicationInstruction("mul(8,5)") === 40);

const runProgram = (instructions: string[]) => {
  let result = 0;
  let instructionApplies = true;
  instructions.forEach((instruction) => {
    if (instruction.startsWith("do(")) {
      instructionApplies = true;
      return;
    }
    if (instruction.startsWith("don't")) {
      instructionApplies = false;
      return;
    }
    if (!instructionApplies) return;
    result += runMultiplicationInstruction(instruction);
  });

  return result;
};

const sumUncorruptedMemory = (
  memory: string[],
  conditionsEnabled: boolean = false,
) => {
  const instructions = memory.flatMap((section) =>
    findUncorrptedMemory(section, conditionsEnabled),
  );
  return runProgram(instructions);
};

const TEST_INPUT =
  "xmul(2,4)%&mul[3,7]!@^do_not_mul(5,5)+mul(32,64]then(mul(11,8)mul(8,5))";
const testMemory = parseInput(TEST_INPUT);
assert(sumUncorruptedMemory(testMemory) === 161);

const TEST_INPUT_PART2 =
  "xmul(2,4)&mul[3,7]!^don't()_mul(5,5)+mul(32,64](mul(11,8)undo()?mul(8,5))";
const testMemoryPart2 = parseInput(TEST_INPUT_PART2);
assert(sumUncorruptedMemory(testMemoryPart2, true) === 48);

const puzzleInput = fs.readFileSync("data/day03_input.txt").toString();
const puzzleMemory = parseInput(puzzleInput);
console.log("Part 1:", sumUncorruptedMemory(puzzleMemory));
console.log("Part 2:", sumUncorruptedMemory(puzzleMemory, true));
