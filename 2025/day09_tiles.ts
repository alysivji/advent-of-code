import assert from "node:assert";
import fs from "node:fs";
import os from "node:os";
import { Point } from "../2024/utilities/grid";

const TEST_INPUT = `7,1
11,1
11,7
9,7
9,5
2,5
2,3
7,3`;

const parseInput = (input: string): Point[] => {
  return input
    .trim()
    .split(os.EOL)
    .map((line) => {
      const parts = line.split(",").map(Number);
      return new Point(parts[0]!, parts[1]!);
    });
};

const calculateArea = (p1: Point, p2: Point) => {
  return Math.abs(p1.x - p2.x + 1) * Math.abs(p1.y - p2.y + 1);
};

const part1 = (points: Point[]): number => {
  let maxArea = 0;
  for (let i = 0; i < points.length; i++) {
    for (let j = i + 1; j < points.length; j++) {
      const area = calculateArea(points[i]!, points[j]!);
      if (area > maxArea) {
        maxArea = area;
      }
    }
  }
  return maxArea;
};

const testTiles = parseInput(TEST_INPUT);

const puzzleInput = fs.readFileSync("data/day09_input.txt").toString();
const tiles = parseInput(puzzleInput);

assert(part1(testTiles) === 50, "part 1 is incorrect");
console.log("part 1:", part1(tiles));
