import { assert } from "node:console";
import fs from "fs";

const TEST_INPUT = `7 6 4 2 1
1 2 7 8 9
9 7 6 2 1
1 3 2 4 5
8 6 4 4 1
1 3 6 7 9
`;

const parseInput = (inputString: string) => {
  return inputString
    .trim()
    .split("\n")
    .map((report) => {
      return report.split(" ").map(Number);
    });
};

const isReportSafe = (report: number[]) => {
  const shifted = report.slice(1);
  const diff = report.slice(0, -1).map((level, idx) => shifted[idx] - level);

  // need to be all increasing or all decreasing
  if (!(diff.every((value) => value > 0) || diff.every((value) => value < 0))) {
    return false;
  }

  // level is between 1 and 3
  if (
    diff
      .map((level) => Math.abs(level))
      .filter((level) => level < 1 || level > 3).length > 0
  ) {
    return false;
  }

  return true;
};

const findSafeReports = (reports: number[][]) => {
  return reports
    .map((report) => isReportSafe(report))
    .filter((value) => value === true).length;
};

const findSafeReportsWithProblemDampener = (reports: number[][]) => {
  return reports
    .map((report) => {
      if (isReportSafe(report)) return true;

      // remove one element and try it again
      for (let i = 0; i < report.length; i++) {
        const reportCopy = [...report];
        reportCopy.splice(i, 1);
        if (isReportSafe(reportCopy)) return true;
      }

      return false;
    })
    .filter((value) => value === true).length;
};

const testReports = parseInput(TEST_INPUT);
assert(findSafeReports(testReports) === 2, "part 1 test input failed");
assert(
  findSafeReportsWithProblemDampener(testReports) === 4,
  "part 2 test input failed",
);

const puzzleInput = fs.readFileSync("data/day02_input.txt").toString();
const reports = parseInput(puzzleInput);
console.log("Part 1:", findSafeReports(reports));
console.log("Part 2:", findSafeReportsWithProblemDampener(reports));
