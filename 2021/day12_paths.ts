import fs from "fs";
import assert from "assert";
import _ from "lodash";

const parseInput = (puzzleInput: string): Map<string, string[]> => {
  const caveSystemGraph = new Map();
  puzzleInput.split("\n").forEach((line) => {
    const [start, end] = line.split("-");
    if (!caveSystemGraph.has(start)) {
      caveSystemGraph.set(start, [end]);
    } else {
      const neighbours: string[] = caveSystemGraph.get(start);
      neighbours.push(end);
      caveSystemGraph.set(start, neighbours);
    }

    if (!caveSystemGraph.has(end)) {
      caveSystemGraph.set(end, [start]);
    } else {
      const neighbours: string[] = caveSystemGraph.get(end);
      neighbours.push(start);
      caveSystemGraph.set(end, neighbours);
    }
  });
  return caveSystemGraph;
};

const puzzleInput = fs
  .readFileSync("2021/data/day12_input.txt")
  .toString()
  .trim();

const TEST_INPUT1 = `start-A
start-b
A-c
A-b
b-d
A-end
b-end`;

const TEST_INPUT2 = `dc-end
HN-start
start-kj
dc-start
dc-HN
LN-dc
HN-end
kj-sa
kj-HN
kj-dc`;

const TEST_INPUT3 = `fs-end
he-DX
fs-he
start-DX
pj-DX
end-zg
zg-sl
zg-pj
pj-he
RW-he
fs-DX
pj-RW
zg-RW
start-pj
he-WI
zg-he
pj-fs
start-RW`;

type Path = {
  nodeToVisit: string;
  path: string[];
};

// part 1
const findAllPaths = (caveSystemGraph: Map<string, string[]>) => {
  `Find all paths

  Can only go into small caves once
  `;
  const startingPosition: Path = {
    nodeToVisit: "start",
    path: [],
  };
  const toVisit = [startingPosition];
  const allValidPaths: string[][] = [];

  while (toVisit.length != 0) {
    const currentCave: Path = toVisit.shift()!;
    const currentPath = currentCave.path.slice();
    currentPath.push(currentCave.nodeToVisit);

    // found a valid path through the caves!
    if (currentCave!.nodeToVisit == "end") {
      allValidPaths.push(currentPath);
      continue;
    }

    // can only visit lowercase caves once
    const neighbouringCaves =
      caveSystemGraph.get(currentCave.nodeToVisit) || [];
    for (let neighbour of neighbouringCaves) {
      if (neighbour === "start") continue;

      const isLowerCaseCave = neighbour === neighbour.toLowerCase();
      if (isLowerCaseCave && currentPath.includes(neighbour)) continue;

      const nextPath: Path = {
        nodeToVisit: neighbour,
        path: currentPath,
      };
      toVisit.push(nextPath);
    }
  }

  return allValidPaths;
};

const part1 = (puzzleInput: string) => {
  const caveSystemGraph = parseInput(puzzleInput);
  return findAllPaths(caveSystemGraph).length;
};
assert(part1(TEST_INPUT1) == 10);
assert(part1(TEST_INPUT2) == 19);
assert(part1(TEST_INPUT3) == 226);
console.time("part 1");
console.log(part1(puzzleInput));
console.timeEnd("part 1");

// part 2
const findAllPathsV2 = (caveSystemGraph: Map<string, string[]>) => {
  `Find all paths

  Can only go into small caves once
  `;
  const startingPosition: Path = {
    nodeToVisit: "start",
    path: [],
  };
  const toVisit = [startingPosition];
  const allValidPaths: string[][] = [];

  while (toVisit.length != 0) {
    const currentCave: Path = toVisit.shift()!;
    const currentPath = currentCave.path.slice();
    currentPath.push(currentCave.nodeToVisit);

    // found a valid path through the caves!
    if (currentCave!.nodeToVisit == "end") {
      allValidPaths.push(currentPath);
      continue;
    }

    // can only visit lowercase caves once
    const neighbouringCaves =
      caveSystemGraph.get(currentCave.nodeToVisit) || [];
    for (let neighbour of neighbouringCaves) {
      if (neighbour === "start") continue;

      // get all smallCavesInPath
      const smallCavesInPath = currentPath.filter((node) => {
        if (node === "start" || node === "end") return false;
        return node === node.toLowerCase();
      });
      // add neighbour to see if candidate should be included
      smallCavesInPath.push(neighbour);
      // count number of occurennces of each cave in path
      const countNumberOfVisits = smallCavesInPath.reduce((counter, node) => {
        counter.has(node)
          ? counter.set(node, counter.get(node) + 1)
          : counter.set(node, 1);
        return counter;
      }, new Map());

      const sortedCounter = [...countNumberOfVisits.values()].sort(
        (a, b) => b - a,
      );
      let canVisitNeighbour = true;
      if (sortedCounter.length >= 2) {
        if (sortedCounter[0] > 2) canVisitNeighbour = false;
        if (sortedCounter[1] > 1) canVisitNeighbour = false;
      }

      if (!canVisitNeighbour) {
        continue;
      }

      const nextPath: Path = {
        nodeToVisit: neighbour,
        path: currentPath.slice(),
      };
      toVisit.push(nextPath);
    }
  }

  return allValidPaths;
};
const part2 = (puzzleInput: string) => {
  const caveSystemGraph = parseInput(puzzleInput);
  return findAllPathsV2(caveSystemGraph).length;
};
assert(part2(TEST_INPUT1) == 36);
console.time("part 2");
console.log(part2(puzzleInput));
console.timeEnd("part 2");
