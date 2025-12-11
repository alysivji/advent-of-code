import assert from "node:assert";
import fs from "node:fs";
import os from "node:os";
import { Heap } from "heap-js";

// const TEST_INPUT = `[.##.] (3) (1,3) (2) (2,3) (0,2) (0,1) {3,5,4,7}`;
const TEST_INPUT = `[.##.] (3) (1,3) (2) (2,3) (0,2) (0,1) {3,5,4,7}
[...#.] (0,2,3,4) (2,3) (0,4) (0,1,2) (1,2,3,4) {7,5,12,7,2}
[.###.#] (0,1,2,3,4) (0,3,4) (0,1,2,4,5) (1,2) {10,11,11,5,10,5}`;

type Machine = {
  indicatorLights: boolean[];
  buttonWireSchematics: number[][];
  joltageRequirements: number[];
};

const parseInput = (input: string): Machine[] => {
  const re = new RegExp(
    /^(?<pattern>\[[.#]+\])\s+(?<groups>(?:\(\d+(?:,\d+)*\)\s+)+)\s*(?<final>\{(?:\d+,)*\d+\})$/,
  );

  return input
    .trim()
    .split(os.EOL)
    .map((line) => {
      const match = line.match(re);

      return {
        indicatorLights: match!
          .groups!.pattern!.slice(1, -1)
          .split("")
          .map((value) => value === "#"),
        buttonWireSchematics: match!
          .groups!.groups!.trim()
          .split(" ")
          .map((group) => group.slice(1, -1).split(",").map(Number)),
        joltageRequirements: match!
          .groups!.final!.slice(1, -1)
          .split(",")
          .map(Number),
      };
    });
};

function boolsToMask(arr: boolean[]) {
  return arr.reduce((mask, bit) => (mask << 1) | (bit ? 1 : 0), 0);
}

function hammingDistance(a: number, b: number): number {
  let x = a ^ b; // XOR → bits that differ
  let count = 0;
  while (x) {
    x &= x - 1; // remove lowest set bit
    count++;
  }
  return count;
}

type MachineState = {
  numButtonPresses: number;
  lights: number;
  distance: number;
};

const part1 = (machines: Machine[]): number => {
  return machines
    .map((machine) => {
      const patternToMatch = boolsToMask(machine.indicatorLights);

      // transform list of light numbers each button turns on
      // to list of togglePatterns each button turns on so we can xor
      // {1, 3} => [false, true, false, true] if 4 lights
      const togglePatterns: number[] = [];
      for (const buttonWiring of machine.buttonWireSchematics) {
        const togglePattern = Array(machine.indicatorLights.length)
          .fill(0)
          .map((_, index) => index)
          .map((value) => buttonWiring.indexOf(value) >= 0);
        togglePatterns.push(boolsToMask(togglePattern));
      }

      const startMachine = {
        numButtonPresses: 0,
        lights: 0,
        distance: hammingDistance(0, patternToMatch),
      };

      const hammingDistanceComparator = (a: MachineState, b: MachineState) => {
        if (a.numButtonPresses !== b.numButtonPresses) {
          return a.numButtonPresses - b.numButtonPresses;
        }

        return a.distance - b.distance;
      };
      const machineHeap = new Heap(hammingDistanceComparator);
      machineHeap.init();
      machineHeap.push(startMachine);

      while (true) {
        const machineState = machineHeap.pop()!;
        if (machineState.distance === 0) {
          return machineState.numButtonPresses;
        }

        for (const togglePattern of togglePatterns) {
          // XOR to toggle
          const updatedLights = machineState.lights ^ togglePattern;

          const updatedNumButtonPresses = machineState.numButtonPresses + 1;
          const distance = hammingDistance(updatedLights, patternToMatch);

          machineHeap.push({
            numButtonPresses: updatedNumButtonPresses,
            lights: updatedLights,
            distance,
          });
        }
      }
    })
    .reduce((acc, value) => acc + value);
};

const testMachines = parseInput(TEST_INPUT);

const puzzleInput = fs.readFileSync("data/day10_input.txt").toString();
const machines = parseInput(puzzleInput);

// assert(part1(testMachines) === 7, "part 1 is incorrect");
console.log("part1:", part1(machines));

// const myBinary = 0b1111;
// console.log("value", myBinary);
// console.log("type", typeof myBinary);

// const myBinary2 = 0b0001;

// const difference = countBits(myBinary ^ myBinary2);
// console.log("value", difference);
// console.log("type", typeof difference);
