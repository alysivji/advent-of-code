import assert from "assert";
import fs from "fs";

const TEST_INPUT = `3   4
4   3
2   5
1   3
3   9
3   3
`

const parseInput = (input: string) => {
  const list1: number[] = []
  const list2: number[] = [];
  input.trim().split("\n").forEach(item => {
    const parts = item.split("   ");
    list1.push(Number(parts[0]));
    list2.push(Number(parts[1]));
  })
  return [list1, list2]
}

const distanceBetweenLocations = (list1: number[], list2: number[]) => {
  const sortedList1 = list1.sort();
  const sortedList2 = list2.sort();

  return sortedList1.map((value, idx) => Math.abs(value - sortedList2[idx])).reduce((a, b) => a + b)
}

const [a, b] = parseInput(TEST_INPUT)
assert(distanceBetweenLocations(a, b) === 11)

const input = fs.readFileSync("data/day01_input.txt").toString();
const [locationId1, locationId2] = parseInput(input);
console.log("Part 1: ", distanceBetweenLocations(locationId1, locationId2))

const similartyScore = (list1: number[], list2: number[]) => {
  const counts = new Map();
  list2.forEach(item => {
    if (counts.has(item)) {
      counts.set(item, counts.get(item) + 1)
    } else {
      counts.set(item, 1)
    }
  })

  return list1.map(item => {
    if (!counts.has(item)) return 0
    return item * counts.get(item)
  }).reduce((a, b) => a + b)
}

assert(similartyScore(a, b) === 31)
console.log("Part 2: ", similartyScore(locationId1, locationId2))
