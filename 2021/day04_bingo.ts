import assert from "assert";
import fs from "fs";

const TEST_INPUT =
  `7,4,9,5,11,17,23,2,0,14,21,24,10,16,13,6,15,25,12,22,18,20,8,19,3,26,1

22 13 17 11  0
 8  2 23  4 24
21  9 14 16  7
 6 10  3 18  5
 1 12 20 15 19

 3 15  0  2 22
 9 18 13 17  5
19  8  7 25 23
20 11 10 24  4
14 21 16 12  6

14 21 17 24  4
10 16 15  9 19
18  8 23 26 20
22 11 13  6  5
 2  0 12  3  7
 `.trim();

const parseInput = (text: string): [number[], string[]] => {
  const [_calledNumbers, ...boards] = text.split("\n\n");

  const calledNumbers: number[] = _calledNumbers.split(",").map(Number);

  return [calledNumbers, boards];
};

class BingoBoard {
  board: number[][];
  allValues: Set<number>;

  constructor(boardData: string) {
    const rows = boardData.split("\n");
    this.board = [];
    this.allValues = new Set();
    rows.forEach((row) => {
      const parsedRow = row
        .split(" ")
        .filter((value) => value != "")
        .map(Number);
      parsedRow.forEach((value) => this.allValues.add(value));
      this.board.push(parsedRow);
    });
  }

  drawNumber(num: number) {
    if (!this.allValues.has(num)) {
      return -1;
    }

    for (let rowIdx = 0; rowIdx < this.board.length; rowIdx++) {
      for (let colIdx = 0; colIdx < this.board[rowIdx].length; colIdx++) {
        if (this.board[rowIdx][colIdx] == num) {
          this.board[rowIdx][colIdx] = -1;
          return num;
        }
      }
    }
  }

  isWinner(): boolean {
    // check rows
    if (
      this.board
        .map((row) => row.every((element) => element === -1))
        .includes(true)
    ) {
      return true;
    }

    // check columns
    for (let colIdx = 0; colIdx < this.board[0].length; colIdx++) {
      let columnElements: number[] = [];
      for (let rowIdx = 0; rowIdx < this.board.length; rowIdx++) {
        columnElements.push(this.board[rowIdx][colIdx]);
      }
      if (columnElements.every((element) => element === -1)) {
        return true;
      }
    }

    return false;
  }

  calculateScore(lastNumCalled: number): number {
    let score = 0;

    for (let rowIdx = 0; rowIdx < this.board.length; rowIdx++) {
      for (let colIdx = 0; colIdx < this.board[rowIdx].length; colIdx++) {
        if (this.board[rowIdx][colIdx] !== -1) {
          score += this.board[rowIdx][colIdx];
        }
      }
    }

    return score * lastNumCalled;
  }
}

// part 1
const playBingo = (boards: BingoBoard[], calledNumbers: number[]): number => {
  for (const calledNumber of calledNumbers) {
    for (const board of boards) {
      board.drawNumber(calledNumber);
      if (board.isWinner()) {
        return board.calculateScore(calledNumber);
      }
    }
  }
  return -1;
};

// test case
let [calledNumbersTest, boardsTest] = parseInput(TEST_INPUT);
let bingoBoardsTest = boardsTest.map((board) => new BingoBoard(board));
assert(playBingo(bingoBoardsTest, calledNumbersTest) == 4512);

const bingoInput = fs
  .readFileSync("2021/data/day04_input.txt")
  .toString()
  .trim();

let [calledNumbers, boards] = parseInput(bingoInput);
let bingoBoards = boards.map((board) => new BingoBoard(board));
console.log(playBingo(bingoBoards, calledNumbers));

// part 2
const playBingoToLose = (
  boards: BingoBoard[],
  calledNumbers: number[],
): number => {
  let winningBoards: Set<number> = new Set();

  for (const calledNumber of calledNumbers) {
    for (const [boardIdx, board] of boards.entries()) {
      board.drawNumber(calledNumber);
      if (board.isWinner()) {
        winningBoards.add(boardIdx);
        if (winningBoards.size == boards.length)
          return board.calculateScore(calledNumber);
      }
    }
  }
  return -1;
};

assert(playBingoToLose(bingoBoardsTest, calledNumbersTest) == 1924);
console.log(playBingoToLose(bingoBoards, calledNumbers));
