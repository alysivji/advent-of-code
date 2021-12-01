"use strict";

import fs from "fs";

// part 1
function countIncreasing(depths: Array<number>) {
  let numIncreasing = 0;
  let lastDepth = depths[0];
  for (const depth of depths.slice(1)) {
    if (depth > lastDepth) {
      numIncreasing += 1;
    }
    lastDepth = depth;
  }
  return numIncreasing;
}

const TEST_INPUT: string = `199
200
208
210
200
207
240
269
260
263
`;
const testDepths = TEST_INPUT.trim()
  .split("\n")
  .map((item) => parseInt(item));
console.log(countIncreasing(testDepths));

const depths = fs
  .readFileSync("2021/data/day01_input.txt")
  .toString()
  .trim()
  .split("\n")
  .map(Number);
console.log("Part 1 answer: ", countIncreasing(depths));

// part 2
function countIncreasingGroupOfThree(depths: Array<number>) {
  let numIncreasing = 0;
  let lastDepth: number = depths[0] + depths[1] + depths[2];
  for (let idx = 1; idx < depths.length - 2; idx++) {
    const depth: number = depths[idx] + depths[idx + 1] + depths[idx + 2];
    if (depth > lastDepth) {
      numIncreasing += 1;
    }
    lastDepth = depth;
  }
  return numIncreasing;
}

console.log(countIncreasingGroupOfThree(testDepths));
console.log("Part 2 answer: ", countIncreasingGroupOfThree(depths));

// After looking at some solutions
let result = testDepths
  .map((item, idx, arr) => arr[idx] + arr[idx + 1] + arr[idx + 2])
  .map((item, idx, arr) => item < arr[idx + 1])
  .reduce((acc, b) => (b ? acc + 1 : acc), 0);
console.log(result);

result = depths
  .map((item, idx, arr) => arr[idx] + arr[idx + 1] + arr[idx + 2])
  .map((item, idx, arr) => item < arr[idx + 1])
  .reduce((acc, b) => (b ? acc + 1 : acc), 0);
console.log(result);
