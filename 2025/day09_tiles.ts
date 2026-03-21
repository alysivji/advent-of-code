import assert from "node:assert";
import fs from "node:fs";
import os from "node:os";
import { GridSet, Point, Vector } from "../2024/utilities/grid";

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

const part2 = (points: Point[]): number => {
  const getBorder = () => {
    const pointsToConnect: Point[] = [...points, points[0]!];

    const border: Point[] = [];
    border.push(pointsToConnect.pop()!);

    while (pointsToConnect.length > 0) {
      const nextPointToConnect = pointsToConnect.pop()!;
      const lastPointConnected = border.pop()!;

      const diff = lastPointConnected.directionalVector(nextPointToConnect);

      // can only move in 4 directions so 1 of the differences will be 0
      let unitDirectionVector: Vector;
      if (diff.xDiff === 0) {
        unitDirectionVector = new Vector(0, diff.yDiff / Math.abs(diff.yDiff));
      } else if (diff.yDiff === 0) {
        unitDirectionVector = new Vector(diff.xDiff / Math.abs(diff.xDiff), 0);
      } else {
        throw new Error("should not get here");
      }

      let pointToAdd: Point = lastPointConnected;
      while (true) {
        border.push(pointToAdd);
        if (pointToAdd.equals(nextPointToConnect)) break;

        pointToAdd = pointToAdd.add(unitDirectionVector);
      }
    }

    return {
      border: new GridSet(border),
      minX: Math.min(...border.map((point) => point.x)),
      maxX: Math.max(...border.map((point) => point.x)),
      minY: Math.min(...border.map((point) => point.y)),
      maxY: Math.max(...border.map((point) => point.y)),
    };
  };

  const { border, minX, maxX, minY, maxY } = getBorder();

  // pick a point inside the border (how do i know it's inside the border)
  // check up, down, left, and right. has to hit all of them
  // then the point is inside. from there build out an frontier
  // once our frontier == the border, those points are part of the inside

  // then for each pair, we'd need to do a set intersection

  // this still seems inefficient, anything we can do to improve?

  return 0;
};

const testTiles = parseInput(TEST_INPUT);

const puzzleInput = fs.readFileSync("data/day09_input.txt").toString();
const tiles = parseInput(puzzleInput);

// assert(part1(testTiles) === 50, "part 1 is incorrect");
// console.log("part 1:", part1(tiles));

// part2(testTiles);
part2(tiles);
