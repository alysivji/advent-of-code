import fs from "fs";
import assert from "assert";
import _ from "lodash";

const TEST_INPUT = `6,10
0,14
9,10
0,3
10,4
4,11
6,0
6,12
4,1
0,13
10,12
3,4
3,0
8,4
1,10
2,14
8,10
9,0

fold along y=7
fold along x=5`;

const parseInput = (puzzleInput: string): [Set<string>, string[]] => {
  const [_dots, _folds] = puzzleInput.split("\n\n");

  const dots: Set<string> = new Set();
  _dots
    .trim()
    .split("\n")
    .forEach((value) => dots.add(value));

  const folds: string[] = [];
  _folds
    .trim()
    .split("\n")
    .forEach((value) => {
      const fold_info = value.split("fold along ");
      folds.push(fold_info[1]);
    });

  return [dots, folds];
};

const puzzleInput = fs
  .readFileSync("2021/data/day13_input.txt")
  .toString()
  .trim();

const foldPage = (dots: Set<string>, foldLine: number, foldIndex: 1 | 0) => {
  // y means fold up; foldIndex == 1
  // x means fold left, foldIndex == 0
  const nums = [...dots].map((key) => key.split(",").map(Number)[foldIndex]);
  const numMin = Math.min(...nums);
  const numMax = Math.max(...nums);

  const originHasChanged = numMax - foldLine > foldLine - numMin;
  const transformAmount = Math.abs(2 * foldLine - numMax);
  let updatedDots = [...dots].map((key) => {
    const value = key.split(",").map(Number);

    // point has not changed
    if (value[foldIndex] < foldLine) return key;

    let newCoordinate = 2 * foldLine - value[foldIndex];
    if (originHasChanged) {
      newCoordinate += transformAmount;
    }
    if (foldIndex == 1) return `${value[0]},${newCoordinate}`;
    return `${newCoordinate},${value[1]}`;
  });
  return new Set(updatedDots);
};

// part 1
const part1 = (puzzleInput: string) => {
  let [dots, folds] = parseInput(puzzleInput);
  const fold = folds.slice(0)[0];
  const foldLine = parseInt(fold.split("=")[1]);

  if (fold.split("=")[0] == "x") {
    dots = foldPage(dots, foldLine, 0);
  } else {
    dots = foldPage(dots, foldLine, 1);
  }
  return dots.size;
};
console.log(part1(TEST_INPUT));
console.time("part 1");
console.log(part1(puzzleInput));
console.timeEnd("part 1");

// part 2
const drawDots = (dots: Set<string>) => {
  const xs = [...dots].map((key) => key.split(",").map(Number)[0]);
  const xMax = Math.max(...xs);
  const ys = [...dots].map((key) => key.split(",").map(Number)[0]);
  const yMax = Math.max(...ys);

  const grid = new Array(yMax + 1)
    .fill(".")
    .map((value) => new Array(xMax + 1).fill("."));
  for (const dot of dots) {
    const [x, y] = dot.split(",").map(Number);
    grid[y][x] = "#";
  }

  let printString = "";
  grid.forEach((row) => {
    printString += row.join("") + "\n";
  });
  console.log(printString);
};

const part2 = (puzzleInput: string) => {
  let [dots, folds] = parseInput(puzzleInput);
  for (const fold of folds) {
    const foldLine = parseInt(fold.split("=")[1]);

    if (fold.split("=")[0] == "x") {
      dots = foldPage(dots, foldLine, 0);
    } else {
      dots = foldPage(dots, foldLine, 1);
    }
  }

  return drawDots(dots);
};
console.time("part 2");
part2(puzzleInput);
console.timeEnd("part 2");
