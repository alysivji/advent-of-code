import fs from "fs";
import assert from "assert";
import Collections = require("typescript-collections");

type TupleDict = Collections.Dictionary<number[], number>;
type TupleSet = Collections.Set<number[]>;

const parseInput = (puzzleInput: string) => {
  const heightmap: TupleDict = new Collections.Dictionary();

  puzzleInput.split("\n").map((line, rowIdx) => {
    return line
      .split("")
      .forEach((value, colIdx) =>
        heightmap.setValue([rowIdx, colIdx], parseInt(value)),
      );
  });
  return heightmap;
};

const MAX_HEIGHT = 10;
const TEST_INPUT = `2199943210
3987894921
9856789892
8767896789
9899965678`;
const puzzleInput = fs
  .readFileSync("2021/data/day09_input.txt")
  .toString()
  .trim();

// part 1
const findLowpoints = (puzzleInput: string): [TupleDict, number[][]] => {
  const heightmap = parseInput(puzzleInput);

  const lowpoints = [];
  for (const [rowIdx, colIdx] of heightmap.keys()) {
    const height = heightmap.getValue([rowIdx, colIdx])!;
    const north = heightmap.containsKey([rowIdx - 1, colIdx])
      ? heightmap.getValue([rowIdx - 1, colIdx])!
      : MAX_HEIGHT;
    const south = heightmap.containsKey([rowIdx + 1, colIdx])
      ? heightmap.getValue([rowIdx + 1, colIdx])!
      : MAX_HEIGHT;
    const east = heightmap.containsKey([rowIdx, colIdx - 1])
      ? heightmap.getValue([rowIdx, colIdx - 1])!
      : MAX_HEIGHT;
    const west = heightmap.containsKey([rowIdx, colIdx + 1])
      ? heightmap.getValue([rowIdx, colIdx + 1])!
      : MAX_HEIGHT;
    if (height < north && height < south && height < east && height < west) {
      lowpoints.push([rowIdx, colIdx]);
    }
  }
  return [heightmap, lowpoints];
};

const part1 = (puzzleInput: string) => {
  const [heightmap, lowpoints] = findLowpoints(puzzleInput);
  const riskLevel = lowpoints
    .map((point) => heightmap.getValue([point[0], point[1]])!)
    .map((x) => x + 1);
  return riskLevel.reduce((sum, x) => sum + x, 0);
};
assert(part1(TEST_INPUT) == 15);
console.time("part 1");
console.log(part1(puzzleInput));
console.timeEnd("part 1");

// part 2
const SEARCH_DIRECTIONS = [
  [1, 0],
  [-1, 0],
  [0, 1],
  [0, -1],
];
const findLocalBasin = (
  heightmap: TupleDict,
  lowpoint: number[],
): number[][] => {
  const seen: TupleSet = new Collections.Set();
  const toProcess: string[] = [`${lowpoint[0]},${lowpoint[1]}`];
  while (toProcess.length != 0) {
    const [x, y] = toProcess.shift()!.split(",").map(Number);
    seen.add([x, y]);
    for (const [xDiff, yDiff] of SEARCH_DIRECTIONS) {
      const newPoint = [x + xDiff, y + yDiff];
      const coordinateString = `${newPoint[0]},${newPoint[1]}`;
      if (
        heightmap.containsKey(newPoint) &&
        !seen.contains(newPoint) &&
        toProcess.indexOf(coordinateString) == -1
      ) {
        if (heightmap.getValue(newPoint)! < 9) {
          toProcess.push(coordinateString);
        }
      }
    }
  }
  return seen.toArray();
};

const part2 = (puzzleInput: string) => {
  const [heightmap, lowpoints] = findLowpoints(puzzleInput);
  return lowpoints
    .map((lowpoint) => findLocalBasin(heightmap, lowpoint))
    .map((x) => x.length)
    .sort((a, b) => b - a)
    .slice(0, 3)
    .reduce((product, x) => product * x);
};
assert(part2(TEST_INPUT) == 1134);
console.time("part 2");
console.log(part2(puzzleInput));
console.timeEnd("part 2");
