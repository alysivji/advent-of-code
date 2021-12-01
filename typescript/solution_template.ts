"use strict";

import fs from "fs";
import assert from "assert";

const varName = fs
  .readFileSync("2021/data/day01_input.txt")
  .toString()
  .trim()
  .split("\n")
  .map(Number);

assert(2 == 2);
