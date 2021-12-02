"use strict";

import fs from "fs";
import assert from "assert";

interface CourseDetail {
  direction: string;
  units: number;
}

const TEST_INPUT: Array<CourseDetail> = `forward 5
down 5
forward 8
up 3
down 8
forward 2
`
  .trim()
  .split("\n")
  .map((value) => {
    const parsed = value.split(" ");
    return {
      direction: parsed[0],
      units: parseInt(parsed[1]),
    };
  });

const plannedCourse: Array<CourseDetail> = fs
  .readFileSync("2021/data/day02_input.txt")
  .toString()
  .trim()
  .split("\n")
  .map((value) => {
    const parsed = value.split(" ");
    return {
      direction: parsed[0],
      units: parseInt(parsed[1]),
    };
  });

// part 1
const followCourse = (course: Array<CourseDetail>) => {
  let horizontalPos = 0;
  let depth = 0;

  course.forEach((element) => {
    if (element.direction == "forward") {
      horizontalPos += element.units;
    } else if (element.direction == "up") {
      depth -= element.units;
    } else if (element.direction == "down") {
      depth += element.units;
    }
  });

  return horizontalPos * depth;
};

assert(followCourse(TEST_INPUT) == 150);
console.log(followCourse(plannedCourse));

// part 2
const followCourseWithAim = (course: Array<CourseDetail>) => {
  let aim = 0;
  let horizontalPos = 0;
  let depth = 0;

  course.forEach((element) => {
    if (element.direction == "forward") {
      horizontalPos += element.units;
      depth += element.units * aim;
    } else if (element.direction == "up") {
      aim -= element.units;
    } else if (element.direction == "down") {
      aim += element.units;
    }
  });

  return horizontalPos * depth;
};

assert(followCourseWithAim(TEST_INPUT) == 900);
console.log(followCourseWithAim(plannedCourse));
