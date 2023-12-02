import 'dart:core';
import 'dart:convert';
import 'dart:io';

const String part1SampleData = """1abc2
pqr3stu8vwx
a1b2c3d4e5f
treb7uchet
""";

const String part2SampleData = """two1nine
eightwothree
abcone2threexyz
xtwone3four
4nineeightseven2
zoneight234
7pqrstsixteen
""";

void main() {
  String puzzleInput = File('2023/data/day01_input.txt').readAsStringSync();

  // part 1
  assert(part1(part1SampleData) == 142);

  final stopwatchPart1 = Stopwatch()..start();
  print("part 1: ${part1(puzzleInput)}");
  stopwatchPart1.stop();
  print("Elapsed time: ${stopwatchPart1.elapsed}");

  // part 2
  assert(part2(part2SampleData) == 281);

  final stopwatchPart2 = Stopwatch()..start();
  print("part 2: ${part2(puzzleInput)}");
  stopwatchPart2.stop();
  print("Elapsed time: ${stopwatchPart2.elapsed}");
}

int? part1(String input) {
  int sum = 0;

  LineSplitter ls = new LineSplitter();
  List<String> lines = ls.convert(input);

  lines.forEach((line) {
    int? combinedNumber = 10 * findNumber(line, true) + findNumber(line, false);
    sum += combinedNumber;
  });

  return sum;
}

int part2(String input) {
  int sum = 0;

  LineSplitter ls = new LineSplitter();
  List<String> lines = ls.convert(input);

  lines.forEach((line) {
    int? combinedNumber =
        10 * findNumberPart2(line, true) + findNumberPart2(line, false);
    sum += combinedNumber;
  });

  return sum;
}

// https://stackoverflow.com/questions/24085385/checking-if-string-is-numeric-in-dart
isInt(string) => int.tryParse(string) != null;

int findNumber(String line, bool fromFront) {
  if (fromFront == true) {
    for (var i = 0; i < line.length; i++) {
      if (isInt(line[i])) {
        return int.parse(line[i]);
      }
    }
  } else {
    for (var i = line.length - 1; i >= 0; i--) {
      if (isInt(line[i])) {
        return int.parse(line[i]);
      }
    }
  }

  return 0;
}

int findNumberPart2(String line, bool fromFront) {
  if (fromFront == true) {
    for (var i = 0; i < line.length; i++) {
      if (isInt(line[i])) {
        return int.parse(line[i]);
      }
      String rest = line.substring(i);
      if (rest.startsWith("one")) return 1;
      if (rest.startsWith("two")) return 2;
      if (rest.startsWith("three")) return 3;
      if (rest.startsWith("four")) return 4;
      if (rest.startsWith("five")) return 5;
      if (rest.startsWith("six")) return 6;
      if (rest.startsWith("seven")) return 7;
      if (rest.startsWith("eight")) return 8;
      if (rest.startsWith("nine")) return 9;
    }
  } else {
    for (var i = line.length - 1; i >= 0; i--) {
      if (isInt(line[i])) {
        return int.parse(line[i]);
      }
      String rest = line.substring(0, i + 1);
      if (rest.endsWith("one")) return 1;
      if (rest.endsWith("two")) return 2;
      if (rest.endsWith("three")) return 3;
      if (rest.endsWith("four")) return 4;
      if (rest.endsWith("five")) return 5;
      if (rest.endsWith("six")) return 6;
      if (rest.endsWith("seven")) return 7;
      if (rest.endsWith("eight")) return 8;
      if (rest.endsWith("nine")) return 9;
    }
  }

  return 0;
}
