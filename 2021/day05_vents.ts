import assert from "assert";
import fs from "fs";

type Point = {
  x: number;
  y: number;
};

type Vector = Point;

type LineSegment = {
  p1: Point;
  p2: Point;
};

const TEST_INPUT = `0,9 -> 5,9
8,0 -> 0,8
9,4 -> 3,4
2,2 -> 2,1
7,0 -> 7,4
6,4 -> 2,0
0,9 -> 2,9
3,4 -> 1,4
0,0 -> 8,8
5,5 -> 8,2
 `.trim();

const parseInput = (text: string): LineSegment[] => {
  return text
    .split("\n")
    .map((line) => line.split(" -> "))
    .map(([p1, p2]) => {
      const [x1, y1] = p1.split(",").map(Number);
      const [x2, y2] = p2.split(",").map(Number);
      return { p1: { x: x1, y: y1 }, p2: { x: x2, y: y2 } };
    });
};

const findDirectionVector = (lineSegment: LineSegment): Vector => {
  let x_diff = lineSegment.p2.x - lineSegment.p1.x;
  let y_diff = lineSegment.p2.y - lineSegment.p1.y;

  if (x_diff !== 0) x_diff = x_diff / Math.abs(x_diff);
  if (y_diff !== 0) y_diff = y_diff / Math.abs(y_diff);

  return { x: x_diff, y: y_diff };
};

const buildVentMap = (lineSegments: LineSegment[]) => {
  const ventMap: Map<string, number> = new Map();

  lineSegments.forEach((lineSegment) => {
    const directionVectors = findDirectionVector(lineSegment);
    let newX = lineSegment.p1.x;
    let newY = lineSegment.p1.y;
    const numPipes = ventMap.get(`${newX},${newY}`) || 0;
    ventMap.set(`${newX},${newY}`, numPipes + 1);

    while (newX != lineSegment.p2.x || newY != lineSegment.p2.y) {
      newX += directionVectors.x;
      newY += directionVectors.y;
      const numPipes = ventMap.get(`${newX},${newY}`) || 0;
      ventMap.set(`${newX},${newY}`, numPipes + 1);
    }
  });

  return ventMap;
};

const countNumOverlap = (ventMap: Map<string, number>): number => {
  return Array.from(ventMap.entries()).filter(([key, val]) => val > 1).length;
};

const part1 = (input_string: string) => {
  // only horizontal and vertical lines
  const lineSegments = parseInput(input_string).filter(
    (lineSegment) =>
      lineSegment.p1.x == lineSegment.p2.x ||
      lineSegment.p1.y == lineSegment.p2.y,
  );
  const ventMap = buildVentMap(lineSegments);
  const numOverlap = countNumOverlap(ventMap);
  return numOverlap;
};

const part2 = (input_string: string) => {
  const lineSegments = parseInput(input_string);
  const ventMap = buildVentMap(lineSegments);
  const numOverlap = countNumOverlap(ventMap);
  return numOverlap;
};

assert(part1(TEST_INPUT) == 5);

const hydroThermalVents = fs
  .readFileSync("2021/data/day05_input.txt")
  .toString()
  .trim();
console.log(part1(hydroThermalVents));

assert(part2(TEST_INPUT) == 12);
console.log(part2(hydroThermalVents));
