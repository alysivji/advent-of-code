import assert from "assert";
import { GridSet, Point } from "./utilities/grid";
import fs from "fs";

type Antenna = {
  x: number;
  y: number;
  frequency: string;
};

type AntennaPuzzle = {
  antennas: Antenna[];
  length: number;
};

const parseInput = (input: string) => {
  const antennas = input
    .trim()
    .split("\n")
    .flatMap((row, y) => {
      return row
        .split("")
        .map((frequency, x) => ({ x, y, frequency }) as Antenna);
    })
    .filter((item) => item.frequency !== ".");

  return {
    antennas,
    length: input.trim().split("\n").length,
  } as AntennaPuzzle;
};

const findAntinodes = (antennaPuzzle: AntennaPuzzle, part: "1" | "2" = "1") => {
  const isPointInGrid = (p: Point) => {
    return (
      p.x >= 0 &&
      p.x < antennaPuzzle.length &&
      p.y >= 0 &&
      p.y < antennaPuzzle.length
    );
  };

  const antennaMap: Map<string, Antenna[]> = new Map();
  antennaPuzzle.antennas.forEach((antenna) => {
    if (!antennaMap.has(antenna.frequency)) {
      antennaMap.set(antenna.frequency, [antenna]);
      return;
    }
    antennaMap.get(antenna.frequency)!.push(antenna);
  });

  const antennaPairs = [...antennaMap.values()].flatMap((antennas) => {
    return [...pairwiseCombinations(antennas)].map((antennaPair) =>
      antennaPair.map((antenna) => new Point(antenna.x, antenna.y)),
    );
  }).flatMap(arr => [[arr[0], arr[1]], [arr[1], arr[0]]])

  const antinodes = antennaPairs.flatMap((antennaPair) => {
    const [antenna1, antenna2] = antennaPair;
    if (part == "1") {
      const directionalVector = antenna1.directionalVector(antenna2);
      const possibleAntinode = antenna1.add(directionalVector.multiply(2));
      if (!isPointInGrid(possibleAntinode)) return []
      return [possibleAntinode]
    }

    let keepLooking = true;
    let multiplier = 1;
    const antinodesFound = []
    const directionalVector = antenna1.directionalVector(antenna2);
    while (keepLooking) {
      const possibleAntinode = antenna1.add(directionalVector.multiply(multiplier));
      if (!isPointInGrid(possibleAntinode)) {
        keepLooking = false;
      } else {
        antinodesFound.push(possibleAntinode)
      }
      multiplier--;
    }
    return antinodesFound
  })

  const uniqueAntinodes = new GridSet(antinodes)

  return [...uniqueAntinodes.values()];
};

function* pairwiseCombinations<T>(arr: T[]): Generator<T[]> {
  for (let i = 0; i < arr.length - 1; i++) {
    for (let j = i + 1; j < arr.length; j++) {
      yield [arr[i], arr[j]];
    }
  }
}

const TEST_INPUT = `............
........0...
.....0......
.......0....
....0.......
......A.....
............
............
........A...
.........A..
............
............
`;

const testAntennaData = parseInput(TEST_INPUT);
const testAntinodes = findAntinodes(testAntennaData);
assert(testAntinodes.length === 14, "part 1 test failed");

const testAntinodesPart2 = findAntinodes(testAntennaData, "2");
assert(testAntinodesPart2.length === 34, "part 2 test failed");


const puzzleInput = fs.readFileSync("data/day08_input.txt").toString();
const antennaData = parseInput(puzzleInput);
const anitNodes = findAntinodes(antennaData);
console.log("Part 1:", anitNodes.length);

const anitNodesPart2 = findAntinodes(antennaData, "2");
console.log("Part 2:", anitNodesPart2.length);
