import 'dart:io';
import 'dart:math';

// down is positive
// right is positive
Map<Point, String> NUMBER_PAD = {
  Point(0, 0): "1",
  Point(1, 0): "2",
  Point(2, 0): "3",
  Point(0, 1): "4",
  Point(1, 1): "5",
  Point(2, 1): "6",
  Point(0, 2): "7",
  Point(1, 2): "8",
  Point(2, 2): "9",
};

// down is positive
// right is positive
Map<Point, String> DIAMOND_NUMBER_PAD = {
  // first row
  Point(0, -2): "1",
  // second row
  Point(-1, -1): "2",
  Point(0, -1): "3",
  Point(1, -1): "4",
  // third row
  Point(-2, 0): "5",
  Point(-1, 0): "6",
  Point(0, 0): "7",
  Point(1, 0): "8",
  Point(2, 0): "9",
  // fourth row
  Point(-1, 1): "A",
  Point(0, 1): "B",
  Point(1, 1): "C",
  // fifth row
  Point(0, 2): "D",
};

// ########
// SOLUTION
// ########
String useNumPad(
  List<String> directions,
  Map<Point, String> numPad,
  Point<int> startPosition,
) {
  var currentPosition = startPosition;
  Point<int> possiblePosition;

  String dialedNumber = "";
  for (final direction in directions) {
    for (final nextMove in direction.split("")) {
      switch (nextMove) {
        case 'U':
          possiblePosition = Point(currentPosition.x, currentPosition.y - 1);
          break;
        case 'D':
          possiblePosition = Point(currentPosition.x, currentPosition.y + 1);
          break;
        case 'L':
          possiblePosition = Point(currentPosition.x - 1, currentPosition.y);
          break;
        case 'R':
          possiblePosition = Point(currentPosition.x + 1, currentPosition.y);
          break;
        default:
          throw Exception("should not get here");
      }
      if (numPad.containsKey(possiblePosition))
        currentPosition = possiblePosition;
    }
    dialedNumber += numPad[currentPosition]!;
  }

  return dialedNumber;
}

String part1(puzzleInput) {
  var directions = parseInput(puzzleInput);
  return useNumPad(directions, NUMBER_PAD, Point(1, 1));
}

String part2(puzzleInput) {
  var directions = parseInput(puzzleInput);
  return useNumPad(directions, DIAMOND_NUMBER_PAD, Point(-2, 0));
}

// ###########
// RUN PROGRAM
// ###########
List<String> parseInput(String puzzleInput) {
  return puzzleInput.trim().split("\n").map((item) => item.trim()).toList();
}

const TEST_INPUT = """ULL
RRDDD
LURDL
UUUUD
""";
String puzzleInput = File('data/day02_input.txt').readAsStringSync();

void main() {
  // part 1
  assert(part1(TEST_INPUT) == "1985");

  final stopwatchPart1 = Stopwatch()..start();
  print("part 1: ${part1(puzzleInput)}");
  stopwatchPart1.stop();
  print("Elapsed time: ${stopwatchPart1.elapsed}");

  // part 2
  assert(part2(TEST_INPUT) == "5DB3");

  final stopwatchPart2 = Stopwatch()..start();
  print("part 2: ${part2(puzzleInput)}");
  stopwatchPart2.stop();
  print("Elapsed time: ${stopwatchPart2.elapsed}");
}
