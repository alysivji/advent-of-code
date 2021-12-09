import fs from "fs";
import assert from "assert";

type PointDict = Map<string, number>;

class Point {
  x: number;
  y: number;

  constructor(x: number, y: number) {
    this.x = x;
    this.y = y;
  }

  toString() {
    return `${this.x},${this.y}`;
  }
}

const parseInput = (puzzleInput: string): PointDict => {
  const heightmap = new Map();

  puzzleInput.split("\n").map((line, rowIdx) => {
    return line.split("").forEach((value, colIdx) => {
      const p = new Point(rowIdx, colIdx);
      heightmap.set(p.toString(), parseInt(value));
    });
  });
  return heightmap;
};

const TEST_INPUT = `2199943210
3987894921
9856789892
8767896789
9899965678`;
const puzzleInput = fs
  .readFileSync("2021/data/day09_input.txt")
  .toString()
  .trim();

const SEARCH_DIRECTIONS = [
  [1, 0],
  [-1, 0],
  [0, 1],
  [0, -1],
];

// part 1
const findLowpoints = (puzzleInput: string): [PointDict, Point[]] => {
  const heightmap = parseInput(puzzleInput);

  const lowpoints = [];
  for (const [key, height] of heightmap.entries()) {
    const [x, y] = key.split(",").map(Number);
    const p = new Point(x, y);
    let lowestPoint = true;
    for (const [xDiff, yDiff] of SEARCH_DIRECTIONS) {
      const newPoint = new Point(p.x + xDiff, p.y + yDiff);
      const newPointHeight = heightmap.has(newPoint.toString())
        ? heightmap.get(newPoint.toString())!
        : 10;
      if (height >= newPointHeight) {
        lowestPoint = false;
      }
    }
    if (lowestPoint) lowpoints.push(p);
  }
  return [heightmap, lowpoints];
};

const part1 = (puzzleInput: string) => {
  const [heightmap, lowpoints] = findLowpoints(puzzleInput);
  const riskLevel = lowpoints
    .map((point) => heightmap.get(point.toString())!)
    .map((x) => x + 1);
  return riskLevel.reduce((sum, x) => sum + x, 0);
};
assert(part1(TEST_INPUT) == 15);
console.time("part 1");
console.log(part1(puzzleInput));
console.timeEnd("part 1");

// part 2
const findLocalBasin = (heightmap: PointDict, lowpoint: Point): string[] => {
  const seen: Set<string> = new Set();
  const toProcess: string[] = [lowpoint.toString()];
  while (toProcess.length != 0) {
    const [x, y] = toProcess.shift()!.split(",").map(Number);
    const p = new Point(x, y);
    seen.add(p.toString());
    for (const [xDiff, yDiff] of SEARCH_DIRECTIONS) {
      const newPoint = new Point(p.x + xDiff, p.y + yDiff);
      if (
        heightmap.has(newPoint.toString()) &&
        !seen.has(newPoint.toString()) &&
        toProcess.indexOf(newPoint.toString()) == -1
      ) {
        if (heightmap.get(newPoint.toString())! < 9) {
          toProcess.push(newPoint.toString());
        }
      }
    }
  }
  return [...seen];
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
