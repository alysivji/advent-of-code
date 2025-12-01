import fs from "fs";
import os from "os";

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
  // count the number of times the dial is at zero during & after each move

  let numTimesAtZero = 0;
  let pointer = START_NUMBER;

  for (const move of moves) {
    const modDistance = move.distance % TOTAL_NUMBERS;

    if (move.rotationDirection === "L") {
      pointer = pointer - modDistance;
    } else {
      pointer = pointer + modDistance;
    }

    // count number of full rotations as those cross 0 integer division times
    const numTimesAtZeroDuringMove = Math.floor(move.distance / TOTAL_NUMBERS);
    numTimesAtZero += numTimesAtZeroDuringMove;

    if (pointer < 0) {
      pointer = (TOTAL_NUMBERS + pointer) % TOTAL_NUMBERS;
      numTimesAtZero++;

      // adjustment -- don't double count if pointer is at 0
      if (pointer === 0) {
        numTimesAtZero--;
      }
    } else if (pointer >= TOTAL_NUMBERS) {
      pointer = pointer % TOTAL_NUMBERS;
      numTimesAtZero++;
    }
  }

  return numTimesAtZero;
};

const testMoves = parseInput(TEST_INPUT);

const puzzleInput = fs.readFileSync("data/day01_input.txt").toString();
const puzzleMoves = parseInput(puzzleInput);

console.log(part1(testMoves));
console.log("part 1:", part1(puzzleMoves));

console.log(part2(testMoves));
console.log("part 2:", part2(puzzleMoves));
