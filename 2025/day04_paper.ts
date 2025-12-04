import assert from "node:assert";
import fs from "node:fs";
import os from "node:os";

import { ALL_DIRECTIONS, GridMap, Point, Vector } from "../2024/utilities/grid";

const TEST_INPUT = `..@@.@@@@.
@@@.@.@.@@
@@@@@.@.@@
@.@@@@..@.
@@.@@@@.@@
.@@@@@@@.@
.@.@.@.@@@
@.@@@.@@@@
.@@@@@@@@.
@.@.@@@.@.`;

const parseInput = (input: string) => {
  // top left will be 0,0
  const grid = new GridMap();

  input
    .trimEnd()
    .split(os.EOL)
    .forEach((row, x) => {
      row.split("").forEach((value, y) => {
        const point = new Point(y, x);
        grid.set(point, value);
      });
    });

  return grid;
};

const part1 = (grid: GridMap) => {
  // check each roll of paper (value = '@') to find how many adjacent rolls
  // count if less than four

  return [...grid.entries()]
    .filter(([_, value]) => value === "@")
    .filter(([pointStr, _]) => {
      const point = Point.fromString(pointStr);
      return (
        point
          .eightDirections()
          .map((adjacentPoint: Point) => grid.get(adjacentPoint))
          .filter((value) => value === "@").length < 4
      );
    }).length;
};

const part2 = (grid: GridMap) => {
  // keep removing rolls until its not possible to remove any more rolls

  let currentGrid = [...grid.entries()];

  let updatedGrid;
  let numEntries;

  do {
    const currentGridMap = new GridMap();
    currentGrid.forEach(([pointStr, value]) => {
      const point = Point.fromString(pointStr);
      currentGridMap.set(point, value);
    });

    numEntries = currentGrid.length;

    updatedGrid = currentGrid
      .filter(([_, value]) => value === "@")
      .filter(([pointStr, _]) => {
        const point = Point.fromString(pointStr);
        return (
          point
            .eightDirections()
            .map((adjacentPoint: Point) => currentGridMap.get(adjacentPoint))
            .filter((value) => value === "@").length >= 4
        );
      });

    currentGrid = updatedGrid;
  } while (numEntries !== updatedGrid.length);

  // how many total rolls were removed
  return (
    [...grid.entries()].filter(([_, value]) => value === "@").length -
    numEntries
  );
};

const testGrid = parseInput(TEST_INPUT);

const puzzleInput = fs.readFileSync("data/day04_input.txt").toString();
const grid = parseInput(puzzleInput);

assert(part1(testGrid) === 13, "part 1 test failed");
console.log("part1", part1(grid));

assert(part2(testGrid) === 43, "part 2 test failed");
console.log("part2", part2(grid));
