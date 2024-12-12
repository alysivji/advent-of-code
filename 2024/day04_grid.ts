import assert from "node:assert";
import fs from "fs";

import {
  ALL_DIRECTIONS,
  DIAGONALS,
  GridMap,
  Point,
  Vector,
} from "./utilities/grid";

const parseInput = (input: string) => {
  // top left will be 0,0
  const grid = new GridMap();

  input
    .trim()
    .split("\n")
    .forEach((row, x) => {
      row.split("").forEach((value, y) => {
        const point = new Point(y, x);
        grid.set(point, value);
      });
    });

  return grid;
};

const getWordVectors = (vector: Vector, word: string) => {
  const sequentialArray = Array.from({ length: word.length }, (_, i) => i);
  return sequentialArray.map((scaler) => vector.multiply(scaler));
};

const countStraightWords = (grid: GridMap, wordToFind = "XMAS") => {
  const wordVectors = ALL_DIRECTIONS.map((v) => getWordVectors(v, wordToFind));

  const allXs = [...grid.entries()]
    .filter(([_, value]) => value == wordToFind[0])
    .map(([key, _]) => Point.fromString(key));

  return allXs
    .flatMap((point) => {
      return wordVectors.map((wordVector) =>
        wordVector.map((v) => point.add(v)),
      );
    })
    .map((wordPoints) => wordPoints.map((p) => grid.get(p) ?? "").join(""))
    .filter((word) => word === wordToFind).length;
};

const countMasDiagonalsWithOverlappingAs = (
  grid: GridMap,
  wordToFind = "MAS",
) => {
  const wordVectors = DIAGONALS.map((v) => getWordVectors(v, wordToFind));

  const allMs = [...grid.entries()]
    .filter(([_, value]) => value == wordToFind[0])
    .map(([key, _]) => Point.fromString(key));

  const diagonalAsInMas = allMs
    .flatMap((point) => {
      return wordVectors.map((wordVector) =>
        wordVector.map((v) => point.add(v)),
      );
    })
    .filter((wordPoints) => !wordPoints.map((p) => grid.has(p)).includes(false))
    .filter(
      (wordPoints) =>
        wordPoints.map((p) => grid.get(p)).join("") === wordToFind,
    )
    .map((wordPoints) => wordPoints[1]);

  const uniqueAs = new Set(diagonalAsInMas.map((p) => p.toString()));
  return diagonalAsInMas.length - [...uniqueAs].length;
};

const TEST_INPUT = `MMMSXXMASM
MSAMXMSMSA
AMXSXMAAMM
MSAMASMSMX
XMASAMXAMM
XXAMMXXAMA
SMSMSASXSS
SAXAMASAAA
MAMMMXMMMM
MXMXAXMASX
`;
const testGrid = parseInput(TEST_INPUT);
assert(countStraightWords(testGrid) === 18, "part 1 test input incorrect");
assert(
  countMasDiagonalsWithOverlappingAs(testGrid) === 9,
  "part 2 test input incorrect",
);

const puzzleInput = fs.readFileSync("data/day04_input.txt").toString();
const grid = parseInput(puzzleInput);
console.log("Part 1:", countStraightWords(grid));
console.log("Part 2:", countMasDiagonalsWithOverlappingAs(grid));
