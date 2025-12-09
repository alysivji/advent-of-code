import assert from "node:assert";
import fs from "node:fs";
import os from "node:os";
import { GridSet, Point } from "../2024/utilities/grid";

const TEST_INPUT = `.......S.......
...............
.......^.......
...............
......^.^......
...............
.....^.^.^.....
...............
....^.^...^....
...............
...^.^...^.^...
...............
..^...^.....^..
...............
.^.^.^.^.^...^.
...............`;

const parseInput = (input: string): string[][] => {
  return input
    .trim()
    .split(os.EOL)
    .map((line) => line.split("").map((value) => value));
};

const part1 = (diagram: string[][]) => {
  let beamsIndex: number[] = [];
  let splittersUsed = 0;
  for (let index = 0; index < diagram.length; index += 2) {
    if (index === 0) {
      const entranceIndex = diagram[index]!.indexOf("S");
      beamsIndex = [entranceIndex];
      continue;
    }
    const newBeamsIndex = new Set<number>([...beamsIndex]);
    diagram[index]!.forEach((value, i) => {
      const isSplitter = value === "^";
      if (!isSplitter) {
        return;
      }

      const isUsed = beamsIndex.indexOf(i);
      if (isUsed >= 0) {
        splittersUsed++;
        newBeamsIndex.delete(i);
        newBeamsIndex.add(i - 1);
        newBeamsIndex.add(i + 1);
      }
    });

    beamsIndex = [...newBeamsIndex.entries()].map(([value, _]) => value);
  }

  return splittersUsed;
};

const part2 = (diagram: string[][]) => {
  const splitters = new GridSet();
  diagram.forEach((line, row) =>
    line.forEach((value, col) => {
      if (value !== "^") {
        return;
      }

      const point = new Point(col, row);
      splitters.add(point);
    }),
  );

  const entranceIndex = diagram[0]!.indexOf("S");
  const beamStack = [new Point(entranceIndex, 0)];

  let numPaths = 0;
  while (beamStack.length > 0) {
    const currBeam = beamStack.pop()!;
    const newBeamLocation = new Point(currBeam.x, currBeam.y + 2);

    if (newBeamLocation.y > diagram.length) {
      numPaths++;
    } else {
      if (!splitters.has(newBeamLocation)) {
        beamStack.push(newBeamLocation);
      } else {
        beamStack.push(new Point(newBeamLocation.x - 1, newBeamLocation.y));
        beamStack.push(new Point(newBeamLocation.x + 1, newBeamLocation.y));
      }
    }
  }

  return numPaths;
};

const puzzleInput = fs.readFileSync("data/day07_input.txt").toString();
const manifoldDiagram = parseInput(puzzleInput);

const testManifoldDiagram = parseInput(TEST_INPUT);

assert(part1(testManifoldDiagram) === 21, "part 1 is incorrect");
console.log("part 1:", part1(manifoldDiagram));

assert(part2(testManifoldDiagram) === 40, "part 2 is incorrect");
console.log("part 2:", part2(manifoldDiagram));
