import fs from "fs";
import assert from "assert";
import _ from "lodash";

// ##########
// Read input
// ##########
const parseInput = (puzzleInput: string): [string, Map<string, string[]>] => {
  const [templatePolymer, _rules] = puzzleInput.split("\n\n");
  const expansionMap = _rules.split("\n").reduce((acc, rule) => {
    const [pair, middleChar] = rule.split(" -> ");

    const realizedPairs = [pair[0] + middleChar, middleChar + pair[1]];
    acc.set(pair, realizedPairs);
    return acc;
  }, new Map());

  return [templatePolymer, expansionMap];
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

// ########
// Solution
// ########
type PairCount = {
  pair: string;
  count: number;
};

type ExpansionMap = Map<string, string[]>;

class Polymer {
  pairCount: PairCount[];
  expansionMap: ExpansionMap;
  lastLetter: string;
  numStep: number;

  constructor(templateString: string, expansionMap: ExpansionMap) {
    this.lastLetter = templateString.charAt(templateString.length - 1);
    this.expansionMap = expansionMap;
    this.numStep = 0;
    this.pairCount = templateString
      .split("")
      .map((char, index, arr) => char + arr[index + 1])
      .slice(0, -1)
      .map((pair) => {
        return { pair: pair, count: 1 };
      });
  }

  step() {
    const newPairCount = this.pairCount.flatMap((pair) => {
      const expandedPairs = this.expansionMap.get(pair.pair)!;
      return expandedPairs.map((nextPair) => {
        return { pair: nextPair, count: pair.count };
      });
    });

    const countsByPair = _.groupBy(newPairCount, "pair");
    this.pairCount = Object.entries(countsByPair).map(([pair, entries]) => {
      return {
        pair: pair,
        count: _.sumBy(entries, "count"),
      };
    });
    this.numStep += 1;
  }

  getLetterCount() {
    return this.pairCount.reduce((counts, pair) => {
      const firstLetter = pair.pair[0];
      if (!counts.has(firstLetter)) counts.set(firstLetter, pair.count);
      else counts.set(firstLetter, counts.get(firstLetter)! + pair.count);
      return counts;
    }, new Map([[this.lastLetter, 1]]));
  }
}

const getDiffBetweenCounts = (puzzleInput: string, numSteps: number) => {
  let [polymerTemplate, expansionMap] = parseInput(puzzleInput);

  const polymer = new Polymer(polymerTemplate, expansionMap);
  while (polymer.numStep < numSteps) {
    polymer.step();
  }

  const countsMap = polymer.getLetterCount();
  const counts = [...countsMap.values()].sort((a, b) => b - a);
  return counts[0] - counts[counts.length - 1];
};

// part 1
const part1 = (puzzleInput: string) => getDiffBetweenCounts(puzzleInput, 10);
assert(part1(TEST_INPUT) == 1588);
console.time("part 1");
console.log(part1(puzzleInput));
console.timeEnd("part 1");

// part 2
const part2 = (puzzleInput: string) => getDiffBetweenCounts(puzzleInput, 40);
assert(part2(TEST_INPUT) == 2188189693529);
console.time("part 2");
console.log(part2(puzzleInput));
console.timeEnd("part 2");
