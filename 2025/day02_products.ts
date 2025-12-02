import assert from "node:assert";
import fs from "node:fs";

// const TEST_INPUT = `95-115`;
const TEST_INPUT = `11-22,95-115,998-1012,1188511880-1188511890,222220-222224,1698522-1698528,446443-446449,38593856-38593862,565653-565659,824824821-824824827,2121212118-2121212124`;

type ProductIdRange = {
  start: number;
  end: number;
};

const parseInput = (inputText: string): ProductIdRange[] => {
  return inputText.split(",").map((range) => {
    const parts = range.split("-");
    return {
      start: Number(parts[0]),
      end: Number(parts[1]),
    };
  });
};

const part1 = (productIdsRanges: ProductIdRange[]): number => {
  // sum of invalid ids which are ids made of a twice repeating pattern

  const invalidIds = [];

  for (const productIdRange of productIdsRanges) {
    // pattern can't repeat if number's digit length is odd
    if (
      productIdRange.start.toString().length % 2 !== 0 &&
      productIdRange.end.toString().length % 2 !== 0
    ) {
      continue;
    }

    for (
      let productIdToCheck = productIdRange.start;
      productIdToCheck <= productIdRange.end;
      productIdToCheck++
    ) {
      const productId = productIdToCheck.toString();
      const firstHalf = productId.substring(0, productId.length / 2);
      const secondHalf = productId.substring(productId.length / 2);

      if (firstHalf === secondHalf) {
        invalidIds.push(productIdToCheck);
      }
    }
  }

  return invalidIds.reduce((acc, currValue) => acc + currValue);
};

const part2 = (productIdsRanges: ProductIdRange[]): number => {
  // sum of invalid ids which are ids nade up of only repeating pattern x times

  const invalidIds = new Set<number>();

  for (const productIdRange of productIdsRanges) {
    for (
      let productIdToCheck = productIdRange.start;
      productIdToCheck <= productIdRange.end;
      productIdToCheck++
    ) {
      // console.log("productId", productIdToCheck);
      const productId = productIdToCheck.toString();

      for (
        let numRepeatingDigits = 1;
        numRepeatingDigits <= productId.length / 2;
        numRepeatingDigits++
      ) {
        // how to split array into lengths of number of repeating digits
        const size = numRepeatingDigits;

        const chunks: string[] = [];
        for (
          let chunkNum = 0;
          chunkNum < Math.floor(productId.length / size);
          chunkNum++
        ) {
          chunks.push(productId.slice(chunkNum * size, chunkNum * size + size));
        }

        const chunksRepeat = chunks.every((val) => val === chunks[0]);
        const chunksCombined = chunks.reduce((acc, val) => acc.concat(val));

        if (chunksRepeat && chunksCombined === productId) {
          invalidIds.add(productIdToCheck);
        }
      }
    }
  }

  return [...invalidIds].reduce((acc, currValue) => acc + currValue, 0);
};

const testProductIdRanges = parseInput(TEST_INPUT);

const puzzleInput = fs.readFileSync("data/day02_input.txt").toString();
const puzzleProductIdRanges = parseInput(puzzleInput);

assert(part1(testProductIdRanges) === 1227775554, "part 1 test failed");
console.log("part 1:", part1(testProductIdRanges));

assert(part2(testProductIdRanges) === 4174379265, "part 2 test failed");

console.time("part 2");
console.log("part 2:", part2(puzzleProductIdRanges));
console.timeEnd("part 2");
