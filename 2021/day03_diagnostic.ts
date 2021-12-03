"use strict";

import fs from "fs";
import assert from "assert";

const diagnosticReport: string[] = fs
  .readFileSync("2021/data/day03_input.txt")
  .toString()
  .trim()
  .split("\n");

const TEST_INPUT = `00100
11110
10110
10111
10101
01111
00111
11100
10000
11001
00010
01010
`
  .trim()
  .split("\n");


const calculatePowerConsumption = (diagnosticReport: string[]) => {
  const result: string[] = [];
  const complement: string[] = [];
  for (let i = 0; i < diagnosticReport[0].length; i++) {
    let numOnes = 0;
    for (const report of diagnosticReport) {
      if (report[i] === "1") {
        numOnes += 1;
      }
    };
    if (numOnes > Math.floor(diagnosticReport.length / 2)) {
      result.push("1");
      complement.push("0");
    } else {
      result.push("0");
      complement.push("1");
    }
  };

  return parseInt(result.join(""), 2) * parseInt(complement.join(""), 2);
};

assert(calculatePowerConsumption(TEST_INPUT) == 198);
console.log(calculatePowerConsumption(diagnosticReport))
