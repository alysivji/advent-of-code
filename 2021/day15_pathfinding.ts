import fs from "fs";
import assert from "assert";
import Heap from "heap";
import { GridMap, GridSet } from "../aoc/utilities";

// #####
// INPUT
// #####
type GridDetail = {
  x: number;
  y: number;
  riskLevel: number;
};

const parseInput = (puzzleInput: string) => {
  const riskMap = puzzleInput
    .split("\n")
    .flatMap((row, y) => {
      return row
        .split("")
        .map(Number)
        .map((riskLevel, x) => {
          return {
            x: x,
            y: y,
            riskLevel: riskLevel,
          };
        });
    })
    .reduce((gridMap, gridPoint) => {
      gridMap.set([gridPoint.x, gridPoint.y], gridPoint.riskLevel);
      return gridMap;
    }, new GridMap());

  const startPosition = [0, 0];
  const gridSize = puzzleInput.split("\n").length - 1;
  const endPosition = [gridSize, gridSize];
  return {
    map: riskMap,
    start: startPosition,
    end: endPosition,
  };
};

const parseInputPart2 = (puzzleInput: string) => {
  const riskMap = puzzleInput
    .split("\n")
    .flatMap((row, y) => {
      return row
        .split("")
        .map(Number)
        .map((riskLevel, x) => {
          return {
            x: x,
            y: y,
            riskLevel: riskLevel,
          };
        });
    })
    .reduce((gridMap, gridPoint) => {
      gridMap.set([gridPoint.x, gridPoint.y], gridPoint.riskLevel);
      return gridMap;
    }, new GridMap());
  const originalGridSize = puzzleInput.split("\n").length;

  // extend riskMap for extended cave
  const riskLevelsToAdd: GridDetail[] = [];
  for (let i = 0; i < 5; i++) {
    for (let j = 0; j < 5; j++) {
      if (i === 0 && j === 0) continue; // skip grid we already have

      const totalOffset = i + j;
      [...riskMap.entries()].forEach(([coordinate, riskLevel]) => {
        const [x, y] = coordinate.split(",").map(Number);
        const newX = x + originalGridSize * i;
        const newY = y + originalGridSize * j;
        let newriskLevel =
          (riskLevel + totalOffset) % 9 == 0
            ? 9
            : (riskLevel + totalOffset) % 9;

        riskLevelsToAdd.push({ x: newX, y: newY, riskLevel: newriskLevel });
      });
    }
  }
  riskLevelsToAdd.forEach((item) => {
    riskMap.set([item.x, item.y], item.riskLevel);
  });

  const startPosition = [0, 0];
  const gridSize = puzzleInput.split("\n").length * 5;
  const endPosition = [gridSize - 1, gridSize - 1];
  return {
    map: riskMap,
    start: startPosition,
    end: endPosition,
  };
};

const TEST_INPUT = `1163751742
1381373672
2136511328
3694931569
7463417111
1319128137
1359912421
3125421639
1293138521
2311944581`;

const puzzleInput = fs
  .readFileSync("2021/data/day15_input.txt")
  .toString()
  .trim();

// ########
// SOLUTION
// ########
const DIRECTIONS_TO_CHECK = [
  [1, 0],
  [-1, 0],
  [0, 1],
  [0, -1],
];

type ToVisitDetails = {
  coordinate: number[];
  distance: number;
};

const findShortestPath = (riskMap: GridMap, start: number[], end: number[]) => {
  const toVisit: Heap<ToVisitDetails> = new Heap(
    (a, b) => a.distance - b.distance,
  );
  toVisit.push({ coordinate: start, distance: 0 });
  const visited = new GridSet();

  while (toVisit.size() > 0) {
    const curr = toVisit.pop()!;

    if (curr.coordinate.toString() == end.toString()) return curr.distance;
    if (visited.has(curr.coordinate)) continue;
    visited.add(curr.coordinate);

    const unvisitedNeighbours: number[][] = DIRECTIONS_TO_CHECK.reduce(
      (acc, [x_, y_]) => {
        const nextPoint = [curr.coordinate[0] + x_, curr.coordinate[1] + y_];
        if (visited.has(nextPoint)) return acc;
        if (!riskMap.has(nextPoint)) return acc;
        acc.push(nextPoint);
        return acc;
      },
      new Array(),
    );
    unvisitedNeighbours.forEach((coordinate) => {
      const riskLevel = riskMap.get(coordinate)!;
      const totalDistance = curr.distance + riskLevel;
      toVisit.push({ coordinate: coordinate, distance: totalDistance });
    });
  }
};

// part 1
const part1 = (puzzleInput: string) => {
  const data = parseInput(puzzleInput);
  return findShortestPath(data.map, data.start, data.end);
};
assert(part1(TEST_INPUT) === 40);
console.time("part 1");
console.log(part1(puzzleInput));
console.timeEnd("part 1");

// part 2
const part2 = (puzzleInput: string) => {
  const data = parseInputPart2(puzzleInput);
  return findShortestPath(data.map, data.start, data.end);
};
assert(part2(TEST_INPUT) == 315);
console.time("part 2");
console.log(part2(puzzleInput));
console.timeEnd("part 2");
