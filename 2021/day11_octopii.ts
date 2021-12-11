import fs from "fs";
import assert from "assert";
import _, { update } from "lodash";

type Octopus = {
  energyLevel: number;
  hasFlashed: boolean;
};

const parseInput = (puzzleInput: string): Octopus[][] => {
  return puzzleInput.split("\n").map((line) =>
    line.split("").map((value) => {
      return { energyLevel: parseInt(value), hasFlashed: false };
    }),
  );
};

const TEST_INPUT = `5483143223
2745854711
5264556173
6141336146
6357385478
4167524645
2176841721
6882881134
4846848554
5283751526`;
const puzzleInput = fs
  .readFileSync("2021/data/day11_input.txt")
  .toString()
  .trim();

const ALL_DIRECTIONS = [
  [-1, -1],
  [-1, 0],
  [-1, 1],
  [0, -1],
  [0, 1],
  [1, -1],
  [1, 0],
  [1, 1],
];

const step = (grid: Octopus[][]): [Octopus[][], number] => {
  let nextGrid = _.cloneDeep(grid);
  for (let y = 0; y < nextGrid.length; y++) {
    for (let x = 0; x < nextGrid[0].length; x++) {
      nextGrid[y][x].energyLevel += 1;
    }
  }

  while (coordinatesToFlash(nextGrid).length !== 0) {
    let [y, x] = coordinatesToFlash(nextGrid);
    nextGrid = flashOctopus(nextGrid, coordinatesToFlash(nextGrid));
  }

  let numFlashes = 0;
  for (let y = 0; y < nextGrid.length; y++) {
    for (let x = 0; x < nextGrid[0].length; x++) {
      if (nextGrid[y][x].hasFlashed) {
        nextGrid[y][x].energyLevel = 0;
        nextGrid[y][x].hasFlashed = false;
        numFlashes += 1;
      }
    }
  }
  return [nextGrid, numFlashes];
};

const coordinatesToFlash = (grid: Octopus[][]) => {
  for (let y = 0; y < grid.length; y++) {
    for (let x = 0; x < grid[0].length; x++) {
      if (grid[y][x].energyLevel > 9 && !grid[y][x].hasFlashed) {
        return [y, x];
      }
    }
  }
  return [];
};

const flashOctopus = (
  ocotopusGrid: Octopus[][],
  coordinateToFlash: number[],
): Octopus[][] => {
  const updatedGrid = _.cloneDeep(ocotopusGrid);
  const [y, x] = coordinateToFlash;
  for (const [xDiff, yDiff] of ALL_DIRECTIONS) {
    if (x + xDiff < 0 || x + xDiff >= updatedGrid[0].length) continue;
    if (y + yDiff < 0 || y + yDiff >= updatedGrid.length) continue;
    updatedGrid[y + yDiff][x + xDiff].energyLevel += 1;
  }
  updatedGrid[y][x].hasFlashed = true;
  return updatedGrid;
};

// part 1
const part1 = (puzzleInput: string) => {
  let grid = parseInput(puzzleInput);
  let totalFlashes = 0;
  for (let i = 0; i < 100; i++) {
    const result = step(grid);
    grid = result[0];
    totalFlashes += result[1];
  }
  return totalFlashes;
};
assert(part1(TEST_INPUT) == 1656);
console.time("part 1");
console.log(part1(puzzleInput));
console.timeEnd("part 1");

// part 2
const part2 = (puzzleInput: string) => {
  let grid = parseInput(puzzleInput);
  let counter = 0;
  while (true) {
    counter += 1;
    const result = step(grid);
    grid = result[0];

    if (result[1] == 100) {
      return counter;
    }
  }
};
assert(part2(TEST_INPUT) === 195);
console.time("part 2");
console.log(part2(puzzleInput));
console.timeEnd("part 2");
