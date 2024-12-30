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

const fileDefragmentation = (diskLayout: number[]) => {
  const findFreespaceStart = (arr: number[], end: number, length: number) => {
    // return index if found, else -1
    let current = 0;
    let freeSpaceLength = 0;
    while (current < end) {
      if (arr[current] === null) {
        freeSpaceLength++;
      } else {
        // reset free space length
        freeSpaceLength = 0;
      }

      if (freeSpaceLength >= length) return current - freeSpaceLength + 1;

      current++;
    }
    return -1;
  };

  // This time, attempt to move whole files to the leftmost span of free space
  // blocks that could fit the file. Attempt to move each file exactly once in
  // order of decreasing file ID number starting with the file with the highest
  // file ID number. If there is no span of free space to the left of a file
  // that is large enough to fit the file, the file does not move.
  const fileIdToDisk: Map<number, number[]> = new Map();
  diskLayout.forEach((element, index) => {
    if (element === null) return;
    if (!fileIdToDisk.has(element)) {
      fileIdToDisk.set(element, [index]);
    } else {
      fileIdToDisk.get(element)!.push(index);
    }
  });

  const diskLayoutDefragged = [...diskLayout];

  const maxFileId = [...fileIdToDisk.keys()].length - 1;
  for (let i = maxFileId; i >= 0; i--) {
    const currentFileId = i;
    const fileBlocks = fileIdToDisk.get(currentFileId)!;

    const freeSpaceStart = findFreespaceStart(
      diskLayoutDefragged,
      fileBlocks[0],
      fileBlocks.length,
    );
    if (freeSpaceStart < 0) continue;

    // swap elements
    for (let j = 0; j < fileBlocks.length; j++) {
      [
        diskLayoutDefragged[freeSpaceStart + j],
        diskLayoutDefragged[fileBlocks[j]],
      ] = [
          diskLayoutDefragged[fileBlocks[j]],
          diskLayoutDefragged[freeSpaceStart + j],
        ];
    }
  }

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
assert(
  calculateChecksum(testDiskLayoutAfterDiskFragmentation) === 1928,
  "part 1 test failed",
);
const testDiskLayoutAfterFileDefragmentation = fileDefragmentation(testDiskLayout);
assert(
  calculateChecksum(testDiskLayoutAfterFileDefragmentation) === 2858,
  "part 2 test failed",
);

const puzzleInput = fs.readFileSync("data/day09_input.txt").toString();
const diskLayout = parseInput(puzzleInput);
const diskLayoutAfterDiskFragmentation = diskDefragmentation(diskLayout);
console.log("Part 1:", calculateChecksum(diskLayoutAfterDiskFragmentation));
const diskLayoutAfterFileFragmentation = fileDefragmentation(diskLayout);
console.log("Part 2:", calculateChecksum(diskLayoutAfterFileFragmentation));
