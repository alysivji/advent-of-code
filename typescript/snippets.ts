// reading a file
import fs from "fs";
const depths = fs
  .readFileSync("2021/data/day01_input.txt")
  .toString()
  .trim()
  .split("\n")
  .map(Number);
console.log(depths);

// formatting a string
const world = "world";
export function hello(world: string = "world"): string {
  return `Hello ${world}! `;
}
console.log(hello());

// making assertions
import assert from "assert";
assert(2 == 3);
