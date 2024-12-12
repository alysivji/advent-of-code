import assert from "node:assert";
import fs from "fs";
import { Counter } from "./utilities/data_structures";

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

const isUpdateValid = (update: number[], pageOrderRules: PageOrderRule[]) => {
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
        .reduce((a, b) => a && b, true);
    })
    .reduce((a, b) => a && b, true);
};

const filterUpdates = (
  printerData: PrinterUpdateData,
  { isValid }: { isValid: boolean },
) => {
  const { updates, pageOrderRules } = printerData;

  return updates.filter((update) => {
    const isListValid = isUpdateValid(update, pageOrderRules);
    return isValid ? isListValid : !isListValid;
  });
};

const sumMiddlePageInUpdate = (updates: number[][]) => {
  return updates
    .map((update) => update.at(Math.floor(update.length / 2))!)
    .reduce((a, b) => a + b);
};

const correctOrderUpdates = (
  updates: number[][],
  pageOrderRules: PageOrderRule[],
) => {
  return updates.map((update) => {
    const relevantRules = pageOrderRules.filter(
      (rule) =>
        update.indexOf(rule.before) > -1 && update.indexOf(rule.after) > -1,
    );

    const beforeValues = relevantRules.map((rule) => rule.before);
    const beforeCount = new Counter(beforeValues);

    const afterValues = relevantRules.map((rule) => rule.after);
    const afterCount = new Counter(afterValues);

    const correctOrder = beforeCount.sorted("desc").map(([value, _]) => value);
    correctOrder.push(afterCount.sorted("desc")[0][0]);

    return correctOrder;
  });
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
const testValidUpdates = filterUpdates(testPrinterData, { isValid: true });
assert(
  sumMiddlePageInUpdate(testValidUpdates) === 143,
  "part 1 test input incorrect",
);
const testInvalidUpdates = filterUpdates(testPrinterData, { isValid: false });
const testFixedUpdates = correctOrderUpdates(
  testInvalidUpdates,
  testPrinterData.pageOrderRules,
);
assert(
  sumMiddlePageInUpdate(testFixedUpdates) === 123,
  "part 2 test input incorrect",
);

const puzzleInput = fs.readFileSync("data/day05_input.txt").toString();
const printerData = parseInput(puzzleInput);
const validUpdates = filterUpdates(printerData, { isValid: true });
console.log("Part 1:", sumMiddlePageInUpdate(validUpdates));

const invalidUpdates = filterUpdates(printerData, { isValid: false });
const fixedUpdates = correctOrderUpdates(
  invalidUpdates,
  printerData.pageOrderRules,
);
console.log("Part 2:", sumMiddlePageInUpdate(fixedUpdates));
