import fs from "fs";
import assert from "assert";
import _ from "lodash";

const parseInput = (puzzleInput: string) => {
  return puzzleInput.split("\n");
};

const TEST_INPUT = `[({(<(())[]>[[{[]{<()<>>
[(()[<>])]({[<{<<[]>>(
{([(<{}[<>[]}>{[]{[(<()>
(((({<>}<{<{<>}{[]{[]{}
[[<[([]))<([[{}[[()]]]
[{[{({}]{}}([{[{{{}}([]
{<[[]]>}<{[{[{[]{()[[[]
[<(<(<(<{}))><([]([]()
<{([([[(<>()){}]>(<<{{
<{([{{}}[<[[[<>{}]]]>[]]`;
const puzzleInput = fs
  .readFileSync("2021/data/day10_input.txt")
  .toString()
  .trim();

const BRACKET_MAPPING: Map<string, string> = new Map();
BRACKET_MAPPING.set("(", ")");
BRACKET_MAPPING.set("[", "]");
BRACKET_MAPPING.set("{", "}");
BRACKET_MAPPING.set("<", ">");

const ILLEGAL_CHARACTER_VALUES: Map<string, number> = new Map();
ILLEGAL_CHARACTER_VALUES.set(")", 3);
ILLEGAL_CHARACTER_VALUES.set("]", 57);
ILLEGAL_CHARACTER_VALUES.set("}", 1197);
ILLEGAL_CHARACTER_VALUES.set(">", 25137);

const INCOMPLETE_CHARACTER_VALUES: Map<string, number> = new Map();
INCOMPLETE_CHARACTER_VALUES.set(")", 1);
INCOMPLETE_CHARACTER_VALUES.set("]", 2);
INCOMPLETE_CHARACTER_VALUES.set("}", 3);
INCOMPLETE_CHARACTER_VALUES.set(">", 4);

// part 1
const findIllegalClosingBracket = (line: string) => {
  const stack: string[] = [];
  for (let char of line.split("")) {
    if ([...BRACKET_MAPPING.keys()].includes(char)) {
      stack.push(char);
      continue;
    }

    const lastOpenChar = stack.pop();
    if (lastOpenChar == "undefined") return char;

    if (BRACKET_MAPPING.get(lastOpenChar!) !== char) {
      return char;
    }
  }
  return "";
};

const part1 = (puzzleInput: string) => {
  return parseInput(puzzleInput)
    .map((line) => findIllegalClosingBracket(line))
    .map((char) => ILLEGAL_CHARACTER_VALUES.get(char) || 0)
    .reduce((a, b) => a + b);
};
assert(part1(TEST_INPUT) == 26397);
console.time("part 1");
console.log(part1(puzzleInput));
console.timeEnd("part 1");

// part 2
const completeLine = (line: string) => {
  // all of these have matching pairs
  const stack: string[] = [];
  for (let char of line.split("")) {
    if ([...BRACKET_MAPPING.keys()].includes(char)) {
      stack.push(char);
      continue;
    }
    stack.pop();
  }
  return stack
    .reverse()
    .map((char) => BRACKET_MAPPING.get(char))
    .join("");
};

const part2 = (puzzleInput: string) => {
  const incompleteLine = parseInput(puzzleInput).filter(
    (line) => findIllegalClosingBracket(line) === "",
  );

  const incompleteScores = incompleteLine
    .map((line) => completeLine(line))
    .map((completionString) => {
      let score = 0;
      for (let char of completionString) {
        score *= 5;
        score += INCOMPLETE_CHARACTER_VALUES.get(char)!;
      }
      return score;
    })
    .sort((a, b) => b - a);

  return incompleteScores[Math.floor(incompleteScores.length / 2)];
};
assert(part2(TEST_INPUT) == 288957);
console.time("part 2");
console.log(part2(puzzleInput));
console.timeEnd("part 2");
