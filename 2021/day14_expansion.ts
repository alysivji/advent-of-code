import fs from "fs";
import assert from "assert";
import _ from "lodash";

const parseInput = (puzzleInput: string): [string, Map<string, string>] => {
  const [startString, _rules] = puzzleInput.split("\n\n");
  const rules = _rules.split("\n").reduce((acc, rule) => {
    const [pair, insertionString] = rule.split(" -> ");
    acc.set(pair, insertionString);
    return acc;
  }, new Map());

  return [startString, rules];
};

const TEST_INPUT = `NNCB

CH -> B
HH -> N
CB -> H
NH -> C
HB -> C
HC -> B
HN -> C
NN -> C
BH -> H
NC -> B
NB -> B
BN -> B
BB -> N
BC -> B
CC -> N
CN -> C`;

const puzzleInput = fs
  .readFileSync("2021/data/day14_input.txt")
  .toString()
  .trim();

const countInstances = (puzzleInput: string) => {
  return puzzleInput.split("").reduce((acc, value) => {
    if (!acc.has(value)) acc.set(value, 1);
    else acc.set(value, acc.get(value) + 1);
    return acc;
  }, new Map());
};

// part 1
const pairInsertionStep = (
  polymerTemplate: string,
  rules: Map<string, string>,
) => {
  const allPairs = polymerTemplate
    .split("")
    .map((value, index, arr) => value + arr[index + 1])
    .slice(0, -1);

  return (
    allPairs.map((pair) => pair[0] + rules.get(pair)).join("") +
    polymerTemplate.charAt(polymerTemplate.length - 1)
  );
};

const part1 = (puzzleInput: string) => {
  let [polymerTemplate, rules] = parseInput(puzzleInput);
  for (let i = 0; i < 10; i++) {
    polymerTemplate = pairInsertionStep(polymerTemplate, rules);
  }
  const counts = [...countInstances(polymerTemplate).values()].sort(
    (a, b) => b - a,
  );
  return counts[0] - counts[counts.length - 1];
};
assert(part1(TEST_INPUT) == 1588);
console.time("part 1");
console.log(part1(puzzleInput));
console.timeEnd("part 1");

// part 2
const pairInsertionMultipleSteps = (
  polymerTemplate: string,
  rules: Map<string, string>,
  numSteps: number,
) => {
  const allPairs = polymerTemplate
    .split("")
    .map((value, index, arr) => value + arr[index + 1])
    .slice(0, -1);

  // for each pair, simulate it going out 5 steps
  const finalResult = [];
  allPairs.forEach((pair) => {
    let currentPolymer = pair;
    for (let i = 0; i < numSteps; i++) {
      currentPolymer = pairInsertionStep(currentPolymer, rules);
    }
    finalResult.push(currentPolymer);
  });

  return "a";
};

// const part2 = (puzzleInput: string) => {
// };
// console.log(part2(TEST_INPUT));
// console.time("part 2");
// console.log(part2(puzzleInput));
// console.timeEnd("part 2");
