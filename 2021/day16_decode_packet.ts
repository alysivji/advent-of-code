import fs from "fs";
import assert from "assert";
import _ from "lodash";
import { GridMap, GridSet } from "../aoc/utilities";

// ###############
// STRUCTURE INPUT
// ###############
const parseInput = (puzzleInput: string) => {
  // convert hex to binary
  // https://stackoverflow.com/a/68315766/4326704
  return puzzleInput
    .split("")
    .map((i) => parseInt(i, 16).toString(2).padStart(4, "0"))
    .join("");
};

// ########
// SOLUTION
// ########
interface Packet {
  version: number;
  typeId: number;

  sumVersions(): number;
}

class Literal implements Packet {
  version: number;
  typeId: number;
  literal: number;

  constructor(version: number, typeId: number, literal: number) {
    this.version = version;
    this.typeId = typeId;
    this.literal = literal;
  }

  sumVersions(): number {
    return this.version;
  }
}

class Operator implements Packet {
  version: number;
  typeId: number;
  lengthTypeId: number;
  subpackets: Array<Operator | Literal>;

  constructor(version: number, typeId: number, lengthTypeId: number) {
    this.version = version;
    this.typeId = typeId;
    this.lengthTypeId = lengthTypeId;
    this.subpackets = [];
  }

  sumVersions(): number {
    return (
      this.version +
      this.subpackets.reduce((acc, b) => acc + b.sumVersions(), 0)
    );
  }
}

const parsePacket = (packet: string): [Literal | Operator, number] => {
  // todo need to change?
  const packetDetails: Array<Literal | Operator> = [];
  let position = 0;

  // decode header
  const version = binaryToDecimal(packet.substring(position, position + 3));
  const typeId = binaryToDecimal(packet.substring(position + 3, position + 6));
  position += 6;

  if (typeId == 4) {
    // literal packet
    let literalBinary = "";
    while (true) {
      // read next 5 bits
      const leadingChar = packet.substring(position, position + 1);
      literalBinary += packet.substring(position + 1, position + 5);
      position += 5;

      if (leadingChar === "0") break;
    }
    const literal = new Literal(
      version,
      typeId,
      binaryToDecimal(literalBinary),
    );
    return [literal, position];
  } else {
    // operator packet
    const lengthTypeId = parseInt(packet.substring(position, position + 1));
    const operator = new Operator(version, typeId, lengthTypeId);
    position++;
    if (lengthTypeId === 0) {
      // next 15 bits define how many bits are in the next packet
      const numBitsInSubpacket = binaryToDecimal(
        packet.substring(position, position + 15),
      );
      position += 15;

      const packetEnd = position + numBitsInSubpacket;
      while (position < packetEnd) {
        const [parsedSubpacket, bitsConsumed] = parsePacket(
          packet.substring(position),
        );
        operator.subpackets.push(parsedSubpacket);
        position += bitsConsumed;
      }
    } else if (lengthTypeId === 1) {
      // first 11 bits tells you how many packes to expect
      // then parse packets
      const numSubpackets = binaryToDecimal(
        packet.substring(position, position + 11),
      );
      position += 11;

      for (let i = 0; i < numSubpackets; i++) {
        const [parsedSubpacket, bitsConsumed] = parsePacket(
          packet.substring(position),
        );
        operator.subpackets.push(parsedSubpacket);
        position += bitsConsumed;
      }
    }
    return [operator, position];
  }
};

const binaryToDecimal = (bin: string) => {
  const result = bin.split("").reduceRight((acc, value, index) => {
    return acc + parseInt(value) * 2 ** (bin.length - 1 - index);
  }, 0);
  return result;
};

const puzzleInput = fs
  .readFileSync("2021/data/day16_input.txt")
  .toString()
  .trim();

// part 1
const part1 = (puzzleInput: string) => {
  const packet = parseInput(puzzleInput);
  const [structuredPacket, _] = parsePacket(packet);
  return structuredPacket.sumVersions();
};
assert(part1("8A004A801A8002F478") === 16);
assert(part1("620080001611562C8802118E34") === 12);
assert(part1("C0015000016115A2E0802F182340") === 23);
assert(part1("A0016C880162017C3686B18A3D4780") === 31);
console.time("part 1");
console.log(part1(puzzleInput));
console.timeEnd("part 1");

// part 2
// const part2 = (puzzleInput: string) => {
//   const tbd = parseInput(puzzleInput);
// };
// console.log(part2(TEST_INPUT));
// assert(part2(TEST_INPUT) === );
// console.time("part 2");
// console.log(part2(puzzleInput));
// console.timeEnd("part 2");
