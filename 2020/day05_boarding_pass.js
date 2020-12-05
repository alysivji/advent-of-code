assert = require('assert');
fs = require('fs');

function binarySearch(info, initialMin, initialMax) {
  let min = initialMin;
  let max = initialMax;

  for (const char of info) {
    if ((char == "F") | (char == "L")) {
      min = min;
      max = max - Math.ceil((max - min) / 2);
    } else {
      min = min + Math.ceil((max - min) / 2);
      max = max;
    }
  }

  return max;
}

function calculateSeatID(boardingPass) {
  let rowInfo = boardingPass.slice(0, 7);
  let seatInfo = boardingPass.slice(-3);

  const row = binarySearch(rowInfo, 0, 127);
  const col = binarySearch(seatInfo, 0, 7);
  return row * 8 + col;
}

// Tests
assert(calculateSeatID("FBFBBFFRLR") == 357);
assert(calculateSeatID("BFFFBBFRRR") == 567);
assert(calculateSeatID("FFFBBBFRRR") == 119);
assert(calculateSeatID("BBFFBBFRLL") == 820);


var boardingPasses = fs.readFileSync("data/day05_input.txt", "utf8").trim().split("\n");

// Part 1
let highestId = 0;
for (const boardingPass of boardingPasses) {
  let seatId = calculateSeatID(boardingPass.trim());
  if (seatId > highestId) {
    highestId = seatId;
  }
}
console.log("Part 1 answer is", highestId);

// Part 2
let seatedPassengers = [];
for (const boardingPass of boardingPasses) {
  let seatId = calculateSeatID(boardingPass.trim());
  seatedPassengers.push(seatId);
}
const passengerManifest = seatedPassengers.sort((a, b) => { return a - b; });

for (idx = 1; idx < passengerManifest.length - 1; idx++) {
  if (passengerManifest[idx] - passengerManifest[idx - 1] > 1) {
    console.log("Missing seat between", passengerManifest[idx - 1], passengerManifest[idx]);
  }
}
