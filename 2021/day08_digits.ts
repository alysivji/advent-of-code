import fs from "fs";
import assert from "assert";
import _ from "lodash";

const sortString = (input: string) => {
  return input.split("").sort().join("");
};

const parseInput = (inputString: string): [string[][], string[][]] => {
  let signalPatterns: string[][] = [];
  let digits: string[][] = [];
  inputString.split("\n").forEach((line) => {
    const [_signals, _digits] = line.split(" | ");
    signalPatterns.push(_signals.split(" ").map((value) => sortString(value)));
    digits.push(_digits.split(" ").map((value) => sortString(value)));
  });
  return [signalPatterns, digits];
};

const digits = fs.readFileSync("2021/data/day08_input.txt").toString().trim();

const partA = (puzzleInput: string) => {
  const [_, digits] = parseInput(puzzleInput);
  let count = 0;
  for (const digitPattern of digits) {
    count += digitPattern
      .map((value) => value.length)
      .filter(
        (value) => value == 2 || value == 3 || value == 4 || value == 7,
      ).length;
  }
  return count;
};
console.time("part A");
console.log(partA(digits));
console.timeEnd("part A");

const stringDifference = (main: string, toSubtract: string) => {
  // only works if characters are not repeated
  return main
    .split("")
    .filter((value) => !toSubtract.split("").includes(value))
    .join("");
};

assert(stringDifference("abde", "abe") === "d");

const deduceDigitMapping = (digitSignal: string[]): Map<string, number> => {
  const digitArr: string[] = new Array(10).fill("");
  let segmentCount = _.groupBy(digitSignal, (x) => x.length);
  digitArr[1] = segmentCount[2][0];
  digitArr[4] = segmentCount[4][0];
  digitArr[7] = segmentCount[3][0];
  digitArr[8] = segmentCount[7][0];

  let stringDiffArray = segmentCount[6]
    .map((value) => {
      const intermediateDiff = stringDifference(value, digitArr[7]);
      return stringDifference(intermediateDiff, digitArr[4]);
    })
    .map((value) => value.length);
  digitArr[9] = segmentCount[6][stringDiffArray.indexOf(1)];

  stringDiffArray = segmentCount[6]
    .map((value) => stringDifference(digitArr[1], value))
    .map((value) => value.length);
  digitArr[6] = segmentCount[6][stringDiffArray.indexOf(1)];

  digitArr[0] = segmentCount[6].filter((value) => !digitArr.includes(value))[0];

  const bottomLeftChar = stringDifference(digitArr[8], digitArr[9]);
  stringDiffArray = segmentCount[5].map((value) =>
    value.includes(bottomLeftChar) ? 1 : 0,
  );
  digitArr[2] = segmentCount[5][stringDiffArray.indexOf(1)];

  stringDiffArray = segmentCount[5]
    .map((value) => stringDifference(digitArr[1], value))
    .map((value) => value.length);
  digitArr[3] = segmentCount[5][stringDiffArray.indexOf(0)];

  digitArr[5] = segmentCount[5].filter((value) => !digitArr.includes(value))[0];

  return digitArr.reduce((acc, value, idx) => acc.set(value, idx), new Map());
};

const partB = (puzzleInput: string) => {
  const [signalPatterns, digits] = parseInput(puzzleInput);

  return digits.reduce((sum, value, idx) => {
    const digitMap = deduceDigitMapping(signalPatterns[idx]);
    return sum += parseInt(value.map((digit) => digitMap.get(digit)).join(""));
  }, 0)
};

const TEST_DATA = `be cfbegad cbdgef fgaecd cgeb fdcge agebfd fecdb fabcd edb | fdgacbe cefdb cefbgd gcbe
edbfga begcd cbg gc gcadebf fbgde acbgfd abcde gfcbed gfec | fcgedb cgb dgebacf gc
fgaebd cg bdaec gdafb agbcfd gdcbef bgcad gfac gcb cdgabef | cg cg fdcagb cbg
fbegcd cbd adcefb dageb afcb bc aefdc ecdab fgdeca fcdbega | efabcd cedba gadfec cb
aecbfdg fbg gf bafeg dbefa fcge gcbea fcaegb dgceab fcbdga | gecf egdcabf bgf bfgea
fgeab ca afcebg bdacfeg cfaedg gcfdb baec bfadeg bafgc acf | gebdcfa ecba ca fadegcb
dbcfg fgd bdegcaf fgec aegbdf ecdfab fbedc dacgb gdcebf gf | cefg dcbef fcge gbcadfe
bdfegc cbegaf gecbf dfcage bdacg ed bedf ced adcbefg gebcd | ed bcgafe cdgba cbgef
egadfb cdbfeg cegd fecab cgb gbdefca cg fgcdab egfdb bfceg | gbdfcae bgc cg cgb
gcafb gcf dcaebfg ecagb gf abcdeg gaef cafbge fdbac fegbdc | fgae cfgab fg bagce`;
assert(partB(TEST_DATA) == 61229);

console.time("part B");
console.log(partB(digits));
console.timeEnd("part B");
