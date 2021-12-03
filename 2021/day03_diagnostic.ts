"use strict";

import fs from "fs";
import assert from "assert";
import _ from "lodash";

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


// part 1
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

// part 2
const calculateO2Rating = (
  diagnosticReport: string[],
  keepValue: number
) => {
  let validReports: string[] = diagnosticReport.slice();

  for (let i = 0; i < diagnosticReport[0].length; i++) {
    let result = _.groupBy(validReports, (x) => x[i])
    if (result[0].length > result[1].length) {
      validReports = result[0];
    } else if (result[0].length < result[1].length) {
      validReports = result[1];
    } else {
      if (keepValue == 1) {
        validReports = result[1];
      } else {
        validReports = result[0];
      }
    }

    if (validReports.length == 1) {
      return parseInt(validReports[0], 2);
    }
  }
}

const calculateCO2Rating = (
  diagnosticReport: string[],
  keepValue: number
) => {
  let validReports: string[] = diagnosticReport.slice();

  for (let i = 0; i < diagnosticReport[0].length; i++) {
    let result = _.groupBy(validReports, (x) => x[i])
    if (result[0].length < result[1].length) {
      validReports = result[0];
    } else if (result[0].length > result[1].length) {
      validReports = result[1];
    } else {
      if (keepValue == 1) {
        validReports = result[1];
      } else {
        validReports = result[0];
      }
    }

    if (validReports.length == 1) {
      return parseInt(validReports[0], 2);
    }
  }
}

const test_o2 = calculateO2Rating(TEST_INPUT, 1);
console.log(test_o2);
const test_co2 = calculateCO2Rating(TEST_INPUT, 0);
console.log(test_co2);

console.log(calculateO2Rating(diagnosticReport, 1))
console.log(calculateCO2Rating(diagnosticReport, 0))
