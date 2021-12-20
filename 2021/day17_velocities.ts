import fs from "fs";
import assert from "assert";
import _, { min } from "lodash";
import { GridSet } from "../aoc/utilities";

// #####
// INPUT
// #####
const parseInput = (puzzleInput: string): number[][] => {
  // const [[xMin, xMax], [yMin, yMax]] = puzzleInput
  return puzzleInput
    .split("target area: ")
    .slice(-1)[0]
    .split(", ")
    .map((value) => {
      const range = value.split("=").slice(-1)[0];
      const [min, max] = range.split("..").map(Number);
      return [min, max];
    });
};

const TEST_INPUT = `target area: x=20..30, y=-10..-5`;

const puzzleInput = fs
  .readFileSync("2021/data/day17_input.txt")
  .toString()
  .trim();

// ########
// SOLUTION
// ########
// part 1
const part1 = (puzzleInput: string) => {
  const [[xMin, xMax], [yMin, yMax]] = parseInput(puzzleInput);

  const possibleStartVelocities: number[][] = [];
  for (let x = 0; x <= 100; x++) {
    for (let y = 0; y <= 500; y++) {
      possibleStartVelocities.push([x, y]);
    }
  }
  const highestElevation = possibleStartVelocities.map(
    ([xVelocity, yVelocity]) => {
      let [x, y] = [0, 0];
      let [currXVelocity, currYVelocity] = [xVelocity, yVelocity];
      let hitTarget = false;
      let highestY = 0;
      while (true) {
        [x, y] = [x + currXVelocity, y + currYVelocity];
        if (y > highestY) highestY = y;

        // did we hit the target or overshoot it?
        if (x >= xMin && x <= xMax && y >= yMin && y <= yMax) {
          hitTarget = true;
        }
        if (x > xMax || y < yMax) break;

        // update velocity
        if (currXVelocity < 0) currXVelocity += 1;
        else if (currXVelocity == 0) currXVelocity += 0;
        else currXVelocity -= 1;
        currYVelocity -= 1;
      }
      return hitTarget ? highestY : -1;
    },
  );

  return Math.max(...highestElevation);
};
assert(part1(TEST_INPUT) === 45);
console.time("part 1");
console.log(part1(puzzleInput));
console.timeEnd("part 1");

// part 2
const part2 = (puzzleInput: string) => {
  const [[xMin, xMax], [yMin, yMax]] = parseInput(puzzleInput);
  const allInitialVelocities = new GridSet();

  // const possibleStartVelocities: number[][] = [[29, -10]];
  const possibleStartVelocities: number[][] = [];
  for (let x = -100; x <= 700; x++) {
    for (let y = -1000; y <= 750; y++) {
      possibleStartVelocities.push([x, y]);
    }
  }
  possibleStartVelocities.forEach(([xVelocity, yVelocity]) => {
    let [x, y] = [0, 0];
    let [currXVelocity, currYVelocity] = [xVelocity, yVelocity];
    let hitTarget = false;
    while (true) {
      [x, y] = [x + currXVelocity, y + currYVelocity];

      // did we hit the target or overshoot it?
      if (x >= xMin && x <= xMax && y >= yMin && y <= yMax) {
        hitTarget = true;
      }
      if (x > xMax || y < yMin) break;

      // update velocity
      if (currXVelocity < 0) currXVelocity += 1;
      else if (currXVelocity == 0) currXVelocity += 0;
      else currXVelocity -= 1;
      currYVelocity -= 1;
    }
    if (hitTarget) {
      allInitialVelocities.add([xVelocity, yVelocity]);
    }
  });
  return allInitialVelocities.size;
};
console.log(part2(TEST_INPUT));
assert(part2(TEST_INPUT) === 112);
console.time("part 2");
console.log(part2(puzzleInput));
console.timeEnd("part 2");
