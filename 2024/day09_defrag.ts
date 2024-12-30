import { assert } from "node:console";
import fs from "fs";

const parseInput = (input: string) => {
  // evens are disk
  // odds are freespace

  return input
    .trim()
    .split("")
    .map(Number)
    .flatMap((digit, index) => {
      const isDiskSpace = index % 2 === 0;
      const idNumber = Math.floor(index / 2);

      return Array(digit).fill(isDiskSpace ? idNumber : null);
    });
};

const diskDefragmentation = (diskLayout: number[]) => {
  const freeSpaceBlocks = diskLayout
    .map((value, index) => ({ value, index }))
    .filter((item) => item.value === null)
    .map((item) => item.index);

  const filledBlocks = diskLayout
    .map((value, index) => ({ value, index }))
    .filter((item) => item.value !== null)
    .map((item) => item.index)
    .reverse();

  const diskLayoutDefragged = [...diskLayout];
  freeSpaceBlocks.forEach((value, index) => {
    if (value > filledBlocks[index]) return;

    [diskLayoutDefragged[value], diskLayoutDefragged[filledBlocks[index]]] = [
      diskLayoutDefragged[filledBlocks[index]],
      diskLayoutDefragged[value],
    ];
  });

  return diskLayoutDefragged;
};

const calculateChecksum = (diskLayout: number[]) => {
  return diskLayout
    .map((value, index) => (value === null ? 0 : value * index))
    .reduce((a, b) => a + b);
};

const TEST_INPUT = "2333133121414131402";
const testDiskLayout = parseInput(TEST_INPUT);
const testDiskLayoutAfterDiskFragmentation =
  diskDefragmentation(testDiskLayout);
assert(calculateChecksum(testDiskLayoutAfterDiskFragmentation) === 1928, "part 1 test failed");

const puzzleInput = fs.readFileSync("data/day09_input.txt").toString();
const diskLayout = parseInput(puzzleInput);
const diskLayoutAfterDiskFragmentation = diskDefragmentation(diskLayout);
console.log("Part 1:", calculateChecksum(diskLayoutAfterDiskFragmentation));
