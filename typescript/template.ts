import fs from "fs";
import assert from "assert";
import _ from "lodash";
const { Map } = require("immutable");

const parseInput = (puzzleInput: string) => {
  return puzzleInput
  .split("\n")
  .map(Number)
}

const puzzleInput = fs
  .readFileSync("2021/data/day01_input.txt")
  .toString()
  .trim();

const partA = (puzzleInput: string) => {
  puzzleInput
}
assert(2 == 2);
console.time("part A");
console.log(partA(puzzleInput));
console.timeEnd("part A");

const partB = (puzzleInput: string) => {
  puzzleInput
}
assert(2 == 2);
console.time("part B");
console.log(partB(puzzleInput));
console.timeEnd("part B");
