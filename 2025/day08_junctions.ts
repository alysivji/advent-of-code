import assert from "node:assert";
import fs from "node:fs";
import os from "node:os";

export class Point3D {
  constructor(public x: number, public y: number, public z: number) {}

  toString() {
    return `${this.x},${this.y},${this.z}`;
  }

  static fromString(pointStr: string) {
    const parts = pointStr.split(",").map(Number);
    return new Point3D(parts[0], parts[1], parts[2]);
  }

  distance(other: Point3D) {
    return (
      Math.abs(this.x - other.x) ** 2 +
      Math.abs(this.y - other.y) ** 2 +
      Math.abs(this.z - other.z) ** 2
    );
  }
}

const TEST_INPUT = `162,817,812
57,618,57
906,360,560
592,479,940
352,342,300
466,668,158
542,29,236
431,825,988
739,650,466
52,470,668
216,146,977
819,987,18
117,168,530
805,96,715
346,949,466
970,615,88
941,993,340
862,61,35
984,92,344
425,690,689`;

const parseInput = (input: string): Point3D[] => {
  return input
    .trim()
    .split(os.EOL)
    .map((pointStr) => Point3D.fromString(pointStr));
};

type Distance = {
  value: number;
  pairs: Point3D[];
};

const part1 = (junctionBoxes: Point3D[], numConnectionsToMake: number) => {
  const allDistances: Distance[] = [];

  for (let i = 0; i < junctionBoxes.length; i++) {
    for (let j = i + 1; j < junctionBoxes.length; j++) {
      const item = {
        value: junctionBoxes[i].distance(junctionBoxes[j]),
        pairs: [junctionBoxes[i], junctionBoxes[j]],
      };
      allDistances.push(item);
    }
  }

  allDistances.sort((a, b) => a.value - b.value);

  const uniqueCircuits = new Set<string>();
  const shortestConnections = allDistances
    .slice(0, numConnectionsToMake)
    .map((d) => {
      uniqueCircuits.add(d.pairs[0].toString());
      uniqueCircuits.add(d.pairs[1].toString());
      return d.pairs;
    });

  let circuits: Set<string>[] = [];
  for (const [value, _] of Array.from(uniqueCircuits.entries())) {
    const newCircuit = new Set<string>();
    newCircuit.add(value);
    circuits.push(newCircuit);
  }

  for (const boxes of shortestConnections) {
    const connectionSet = new Set(boxes.map((p) => p.toString()));

    for (const circuit of circuits) {
      if (circuit.intersection(connectionSet).size > 0) {
        for (const junctionBox of boxes) {
          circuit.add(junctionBox.toString());
        }
      }
    }
  }

  let numCircuits;
  do {
    numCircuits = circuits.length;
    for (let i = 0; i < numCircuits; i++) {
      for (let j = i + 1; j < numCircuits; j++) {
        const set1 = circuits[i];
        const set2 = circuits[j];

        if (set1.intersection(set2).size > 0) {
          for (const [entry, _] of Array.from(set2.entries())) {
            set1.add(entry);
            set2.delete(entry);
          }
        }
      }
    }

    circuits = circuits.filter((set) => set.size > 0);
  } while (numCircuits !== circuits.length);

  circuits.sort((a, b) => b.size - a.size);

  return circuits
    .slice(0, 3)
    .map((circuit) => circuit.size)
    .reduce((acc, value) => acc * value, 1);
};

const testJunctionBoxes = parseInput(TEST_INPUT);

const puzzleInput = fs.readFileSync("data/day08_input.txt").toString();
const junctionBoxes = parseInput(puzzleInput);

assert(part1(testJunctionBoxes, 10) === 40, "part 1 is incorrect");
console.log("part 1:", part1(junctionBoxes, 1000));
