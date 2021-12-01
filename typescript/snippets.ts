// reading a file
import * as fs from "fs";
const boardingPasses = fs
  .readFileSync("2021/data/day01_input.txt")
  .toString()
  .trim()
  .split("\n");
console.log(boardingPasses);

// formatting a string
const world = "world";
export function hello(world: string = "world"): string {
  return `Hello ${world}! `;
}
console.log(hello());

// making assertions
import assert from "assert";
assert(2 == 3);
