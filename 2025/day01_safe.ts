import assert from "node:assert";
import fs from "node:fs";
import os from "node:os";

const TEST_INPUT = `L68
L30
R48
L5
R60
L55
L1
L99
R14
L82`;

const START_NUMBER = 50;
const TOTAL_NUMBERS = 100;

type Move = {
  rotationDirection: string;
  distance: number;
};

const parseInput = (inputText: string): Move[] => {
  return inputText.split(os.EOL).map((line) => {
    const rotationDirection = line.substring(0, 1);
    const distance = Number(line.substring(1));
    return { rotationDirection, distance };
  });
};

const part1 = (moves: Move[]): number => {
  // count the number of times the dial is at zero after each move

  let numTimesAtZero = 0;
  let pointer = START_NUMBER;

  for (const move of moves) {
    const modDistance = move.distance % TOTAL_NUMBERS;
    if (move.rotationDirection === "L") {
      pointer = pointer - modDistance;
    } else {
      pointer = pointer + modDistance;
    }

    if (pointer < 0) {
      pointer = TOTAL_NUMBERS + pointer;
    } else if (pointer >= TOTAL_NUMBERS) {
      pointer = pointer % TOTAL_NUMBERS;
    }

    if (pointer === 0) {
      numTimesAtZero++;
    }
  }

  return numTimesAtZero;
};

const part2 = (moves: Move[]): number => {
  // count the number of times the dial is at zero during each step of the move

  let numTimesAtZero = 0;
  let pointer = START_NUMBER;

  for (const move of moves) {
    const modDistance = move.distance % TOTAL_NUMBERS;

    const sign = move.rotationDirection === "L" ? -1 : 1;

    let newPointer = pointer + sign * modDistance;

    if (newPointer < 0) {
      newPointer = TOTAL_NUMBERS + newPointer;
      numTimesAtZero++;

      // adjustment -- don't double count if old pointer is at 0
      // we've already counted the move in the previous step
      if (pointer === 0) {
        numTimesAtZero--;
      }
    }

    if (newPointer >= TOTAL_NUMBERS) {
      newPointer = newPointer % TOTAL_NUMBERS;
      numTimesAtZero++;

      // adjustment -- don't double count if new pointer is at 0
      // we'll count the move in the next check
      if (newPointer === 0) {
        numTimesAtZero--;
      }
    }

    if (newPointer === 0) {
      numTimesAtZero++;
    }

    // count number of full rotations as those cross 0 integer division times
    const numTimesAtZeroDuringMove = Math.floor(move.distance / TOTAL_NUMBERS);
    numTimesAtZero += numTimesAtZeroDuringMove;

    pointer = newPointer;
  }

  return numTimesAtZero;
};

const testMoves = parseInput(TEST_INPUT);

const puzzleInput = fs.readFileSync("data/day01_input.txt").toString();
const puzzleMoves = parseInput(puzzleInput);

assert(part1(testMoves) === 3, "part 1 test failed");
console.log("part 1:", part1(puzzleMoves));

assert(part2(testMoves) === 6, "part 2 test failed");
console.log("part 2:", part2(puzzleMoves));
