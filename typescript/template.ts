import fs from "fs";
import assert from "assert";
import _ from "lodash";
const { Map } = require("immutable");

const parseInput = (puzzleInput: string) => {
  return puzzleInput.split("\n").map(Number);
};

const puzzleInput = fs
  .readFileSync("2021/data/day01_input.txt")
  .toString()
  .trim();

// part 1
const part1 = (puzzleInput: string) => {
  puzzleInput;
};
assert(2 == 2);
console.time("part 1");
console.log(part1(puzzleInput));
console.timeEnd("part 1");

// part 2
const part2 = (puzzleInput: string) => {
  puzzleInput;
};
assert(2 == 2);
console.time("part 2");
console.log(part2(puzzleInput));
console.timeEnd("part 2");
