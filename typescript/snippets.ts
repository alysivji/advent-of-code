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
assert(false, "not matching");

// printing grid
const printGrid = (points: Point[]) => {
  const maxX = Math.max(...points.map((point) => point.x));
  const maxY = Math.max(...points.map((point) => point.y));

  const redTiles = new GridSet();
  points.forEach((point) => redTiles.add(point));

  const lines: string[][] = [];
  for (let y = 0; y <= maxY + 1; y++) {
    const line: string[] = [];
    for (let x = 0; x <= maxX + 2; x++) {
      const isRedTile = redTiles.has(new Point(x, y));
      if (isRedTile) {
        line.push("#");
      } else {
        line.push(".");
      }
    }

    lines.push(line);
  }

  const output = lines.map((line) => line.join("")).join("\n");
  console.log(output);
  // fs.writeFileSync("example.txt", output);
};
