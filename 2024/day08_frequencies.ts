import assert from "assert";
import { GridSet, Point } from "./utilities/grid";
import fs from 'fs';

type Antenna = {
  x: number;
  y: number;
  frequency: string;
};

type AntennaPuzzle = {
  antennas: Antenna[];
  length: number;
}

const parseInput = (input: string) => {
  const antennas = input
    .trim()
    .split("\n")
    .flatMap((row, y) => {
      return row
        .split("")
        .map((frequency, x) => ({ x, y, frequency }) as Antenna);
    }).filter(item => item.frequency !== ".");

  return {
    antennas,
    length: input.trim().split("\n").length
  } as AntennaPuzzle
};

const findAntinodes = (antennaPuzzle: AntennaPuzzle) => {

  const isPointInGrid = (p: Point) => {
    return (p.x >= 0 && p.x < antennaPuzzle.length && p.y >= 0 && p.y < antennaPuzzle.length)
  }

  const antennaMap: Map<string, Antenna[]> = new Map()
  antennaPuzzle.antennas.forEach(antenna => {
    if (!antennaMap.has(antenna.frequency)) {
      antennaMap.set(antenna.frequency, [antenna])
      return
    } antennaMap.get(antenna.frequency)!.push(antenna)
  })

  const antinodes = new GridSet();

  antennaMap.forEach((antennas, frequency) => {
    [...chooseTwoCombinations(antennas)].forEach((antennaPair) => {
      const [antenna1, antenna2] = antennaPair.map(antenna => new Point(antenna.x, antenna.y))

      const v1 = antenna1.directionalVector(antenna2);
      const possibleAntiNode1 = antenna1.add(v1.multiply(2))
      if (isPointInGrid(possibleAntiNode1)) antinodes.add(possibleAntiNode1)

      const v2 = antenna2.directionalVector(antenna1);
      const possibleAntiNode2 = antenna2.add(v2.multiply(2))
      if (isPointInGrid(possibleAntiNode2)) antinodes.add(possibleAntiNode2)
    })
  })

  return [...antinodes.values()].map(value => Point.fromString(value))
}

function* chooseTwoCombinations<T>(arr: T[]): Generator<T[]> {
  for (let i = 0; i < arr.length - 1; i++) {
    for (let j = i + 1; j < arr.length; j++) {
      yield [arr[i], arr[j]]
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
const testAntinodes = findAntinodes(testAntennaData)
assert(testAntinodes.length === 14, "part 1 test failed")

const puzzleInput = fs.readFileSync("data/day08_input.txt").toString();
const antennaData = parseInput(puzzleInput);
const anitNodes = findAntinodes(antennaData);
console.log("Part 1:", anitNodes.length)
