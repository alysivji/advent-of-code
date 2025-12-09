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
  let currBeam: number[] = diagram[0]!.map((value) => (value === "S" ? 1 : 0));

  for (let index = 2; index < diagram.length; index += 2) {
    const updatedBeam = new Array(currBeam.length).fill(0);
    diagram[index]!.map((value) => value === "^").forEach(
      (hasSplitter, colIndex) => {
        if (hasSplitter) {
          updatedBeam[colIndex - 1] += currBeam[colIndex];
          updatedBeam[colIndex] = 0;
          updatedBeam[colIndex + 1] += currBeam[colIndex];
        } else {
          updatedBeam[colIndex] += currBeam[colIndex]!;
        }
      },
    );
    currBeam = updatedBeam;
  }
  return currBeam.reduce((a, b) => a + b);
};

const testManifoldDiagram = parseInput(TEST_INPUT);

const puzzleInput = fs.readFileSync("data/day07_input.txt").toString();
const manifoldDiagram = parseInput(puzzleInput);

assert(part1(testManifoldDiagram) === 21, "part 1 is incorrect");
console.log("part 1:", part1(manifoldDiagram));

assert(part2(testManifoldDiagram) === 40, "part 2 is incorrect");
console.log("part 2:", part2(manifoldDiagram));
