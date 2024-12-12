import assert from "node:assert";
import fs from "fs";

type PageOrderRule = {
  before: number;
  after: number;
};

type PrinterUpdateData = {
  updates: number[][];
  pageOrderRules: PageOrderRule[];
};

const parseInput = (input: string): PrinterUpdateData => {
  const parts = input.trim().split("\n\n");

  const pageOrderRules: PageOrderRule[] = parts[0]
    .split("\n")
    .map((line) => line.split("|").map(Number))
    .map((nums) => {
      return {
        before: nums[0],
        after: nums[1],
      };
    });

  const updates = parts[1]
    .split("\n")
    .map((line) => line.split(",").map(Number));

  return {
    updates,
    pageOrderRules,
  };
};

const findValidUpdates = (printerData: PrinterUpdateData) => {
  const { updates, pageOrderRules } = printerData;

  return updates.filter((update) => {
    return update
      .map((value, idx) => {
        return pageOrderRules
          .filter((rule) => rule.before === value || rule.after === value)
          .map((rule) => {
            if (rule.before === value) {
              if (update.indexOf(rule.after) === -1) return true;
              return update.indexOf(rule.after) > idx;
            }
            if (update.indexOf(rule.before) === -1) return true;
            return update.indexOf(rule.before) < idx;
          })
          .reduce((a, b) => a && b);
      })
      .reduce((a, b) => a && b);
  });
};

const sumMiddlePageInUpdate = (updates: number[][]) => {
  return updates
    .map((update) => update.at(Math.floor(update.length / 2))!)
    .reduce((a, b) => a + b);
};

const TEST_INPUT = `47|53
97|13
97|61
97|47
75|29
61|13
75|53
29|13
97|29
53|29
61|53
97|53
61|29
47|13
75|47
97|75
47|61
75|61
47|29
75|13
53|13

75,47,61,53,29
97,61,53,29,13
75,29,13
75,97,47,61,53
61,13,29
97,13,75,29,47
`;
let testPrinterData = parseInput(TEST_INPUT);
const testValidUpdates = findValidUpdates(testPrinterData);
assert(
  sumMiddlePageInUpdate(testValidUpdates) === 143,
  "part 1 test input incorrect",
);

const puzzleInput = fs.readFileSync("data/day05_input.txt").toString();
const printerData = parseInput(puzzleInput);
const validUpdates = findValidUpdates(printerData);
console.log("Part 1:", sumMiddlePageInUpdate(validUpdates));
