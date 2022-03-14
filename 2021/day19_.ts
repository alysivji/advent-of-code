import fs from "fs";
import assert from "assert";
import _ from "lodash";
import { GridMap, GridSet } from "../aoc/utilities";

// ########
// SOLUTION
// ########

// overlap if there are at least 12 beacons in common
// scanner can be each be in any of 24 different orientations: 
// facing positive or negative x, y, or z, * four directions "up" from that facing.


// ###########
// RUN PROGRAM
// ###########
const parseInput = (puzzleInput: string) => {
  return puzzleInput.split("\n").map(Number);
};

const TEST_INPUT = ``;

// const puzzleInput = fs
//   .readFileSync("2021/data/day01_input.txt")
//   .toString()
//   .trim();

// part 1
const part1 = (puzzleInput: string) => {
  const tbd = parseInput(puzzleInput);
};
console.log(part1(TEST_INPUT));
// assert(part1(TEST_INPUT) === );
console.time("part 1");
// console.log(part1(puzzleInput));
// console.timeEnd("part 1");

// part 2
// const part2 = (puzzleInput: string) => {
//   const tbd = parseInput(puzzleInput);
// };
// console.log(part2(TEST_INPUT));
// assert(part2(TEST_INPUT) === );
// console.time("part 2");
// console.log(part2(puzzleInput));
// console.timeEnd("part 2");
