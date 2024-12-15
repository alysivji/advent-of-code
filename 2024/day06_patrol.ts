import assert from "node:assert";
import fs from "fs";

import { GridSet, Point, Vector } from "./utilities/grid";

type MapInfo = {
  initialGuardPosition: Point;
  obstructions: GridSet;
  // observation -- this is a square so is our actual input
  boxSize: number;
};

const rightTurnLookup = (direction: string) => {
  switch (direction) {
    case "U":
      return "R";
    case "R":
      return "D";
    case "D":
      return "L";
    case "L":
      return "U";
  }
};

const parseInput = (input: string): MapInfo => {
  const obstructions = new GridSet();
  let initialPosition: Point;
  let boxSize: number;

  input
    .trim()
    .split("\n")
    .forEach((line, y) =>
      line.split("").forEach((value, x) => {
        const point = new Point(x, y);
        if (value === "#") obstructions.add(point);
        if (value === "^") initialPosition = point;
      }),
    );

  return {
    initialGuardPosition: initialPosition!,
    obstructions,
    boxSize: input.trim().split("\n").length,
  };
};

const simulateGuardMovement = (mapInfo: MapInfo) => {
  // calculate how many positions the guard visits before leaving the box
  const { initialGuardPosition, obstructions, boxSize } = mapInfo;

  const isOnMap = (point: Point) => {
    if (point.x >= boxSize || point.x < 0 || point.y < 0 || point.y >= boxSize)
      return false;
    return true;
  };

  let guardDirection = "U";
  let guardPosition = initialGuardPosition;
  let positionsVisited = new GridSet();
  let step = 0;
  let foundCycle = false;
  while (isOnMap(guardPosition)) {
    step++;
    if (step >= boxSize ** 2) {
      foundCycle = true;
      break;
    }

    positionsVisited.add(guardPosition);

    let newGuardPosition: Point;
    switch (guardDirection) {
      case "U":
        newGuardPosition = guardPosition.add(new Vector(0, -1));
        break;
      case "R":
        newGuardPosition = guardPosition.add(new Vector(1, 0));
        break;
      case "D":
        newGuardPosition = guardPosition.add(new Vector(0, 1));
        break;
      case "L":
        newGuardPosition = guardPosition.add(new Vector(-1, 0));
        break;
    }

    if (obstructions.has(newGuardPosition!)) {
      guardDirection = rightTurnLookup(guardDirection)!;
      newGuardPosition = guardPosition;
    }

    guardPosition = newGuardPosition!;
  }

  return {
    positionsVisited,
    foundCycle,
  };
};

const findNewObstructionsThatCreateCycle = (mapInfo: MapInfo) => {
  const { initialGuardPosition, obstructions, boxSize } = mapInfo;

  let counter = 0;
  for (let x = 0; x < boxSize; x++) {
    for (let y = 0; y < boxSize; y++) {
      const newObstruction = new Point(x, y);
      if (obstructions.has(newObstruction)) continue;
      if (newObstruction.equals(initialGuardPosition)) continue;

      // create new map info
      const updatedObstructions = new GridSet(
        [...obstructions.values()].map((pointStr) =>
          Point.fromString(pointStr),
        ),
      );
      updatedObstructions.add(newObstruction);
      const newMapInfo = {
        initialGuardPosition,
        boxSize,
        obstructions: updatedObstructions,
      };

      const result = simulateGuardMovement(newMapInfo);
      if (result.foundCycle === true) {
        // console.log("Obstruction:", newObstruction);
        counter++;
      }
    }
  }
  return counter;
};

const TEST_INPUT = `....#.....
.........#
..........
..#.......
.......#..
..........
.#..^.....
........#.
#.........
......#...
`;
const testMapInfo = parseInput(TEST_INPUT);
assert(
  simulateGuardMovement(testMapInfo).positionsVisited.size === 41,
  "part 1 test failed",
);
assert(
  !simulateGuardMovement(testMapInfo).foundCycle,
  "part 1 test failed -- found cycle",
);
assert(
  findNewObstructionsThatCreateCycle(testMapInfo) === 6,
  "part 2 test failed",
);

const puzzleInput = fs.readFileSync("data/day06_input.txt").toString();
const mapInfo = parseInput(puzzleInput);
console.log("Part 1:", simulateGuardMovement(mapInfo).positionsVisited.size);

console.time("part 2");
console.log("Part 2:", findNewObstructionsThatCreateCycle(mapInfo));
console.timeEnd("part 2");
