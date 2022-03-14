import 'dart:io';

Map<String, Map<String, String>> directionMap = {
  "N": {
    "L": "W",
    "R": "E",
  },
  "S": {
    "L": "E",
    "R": "W",
  },
  "E": {
    "L": "N",
    "R": "S",
  },
  "W": {
    "L": "S",
    "R": "N",
  }
};

List<String> parseInput(String puzzleInput) {
  return puzzleInput.split(",").map((item) => item.trim()).toList();
}

List<int> resultingDistance(List<String> pathSequence) {
  List<int> currentPosition = [0, 0];
  String currentDirection = "N";

  for (final nextPath in pathSequence) {
    currentDirection =
        directionMap[currentDirection]![nextPath.substring(0, 1)].toString();

    int stepsToWalk = int.parse(nextPath.substring(1));

    if (currentDirection == "N" || currentDirection == "S") {
      currentPosition[1] += stepsToWalk * (currentDirection == "N" ? 1 : -1);
    } else {
      currentPosition[0] += stepsToWalk * (currentDirection == "W" ? 1 : -1);
    }
  }

  return currentPosition;
}

List<int> firstLocationVisitedTwice(List<String> pathSequence) {
  List<int> currentPosition = [0, 0];
  String currentDirection = "N";

  Set<String> visited = {};
  visited.add(currentPosition.toString());
  for (final nextPath in pathSequence) {
    currentDirection =
        directionMap[currentDirection]![nextPath.substring(0, 1)].toString();

    int stepsToWalk = int.parse(nextPath.substring(1));
    for (var stepCounter = 0; stepCounter < stepsToWalk; stepCounter++) {
      if (currentDirection == "N" || currentDirection == "S") {
        currentPosition[1] += (currentDirection == "N" ? 1 : -1);
      } else {
        currentPosition[0] += (currentDirection == "W" ? 1 : -1);
      }

      if (visited.contains(currentPosition.toString())) return currentPosition;
      visited.add(currentPosition.toString());
    }
  }

  throw Exception("Should not get here");
}

int calculateManhattanDistance(List<int> coordinate1, List<int> coordinate2) {
  return (coordinate2[0] - coordinate1[0]).abs() +
      (coordinate2[1] - coordinate1[1]).abs();
}

int part1(puzzleInput) {
  var data = parseInput(puzzleInput);
  var lastPoint = resultingDistance(data);
  return calculateManhattanDistance(lastPoint, [0, 0]);
}

int part2(puzzleInput) {
  var data = parseInput(puzzleInput);
  var visitedTwice = firstLocationVisitedTwice(data);
  return calculateManhattanDistance(visitedTwice, [0, 0]);
}

void main() {
  String puzzleInput = File('data/day01_input.txt').readAsStringSync();

  // part 1
  assert(part1("R2, L3") == 5);
  assert(part1("R2, R2, R2") == 2);
  assert(part1("R5, L5, R5, R3") == 12);

  final stopwatchPart1 = Stopwatch()..start();
  print("part 1: ${part1(puzzleInput)}");
  stopwatchPart1.stop();
  print("Elapsed time: ${stopwatchPart1.elapsed}");

  // part 2
  assert(part2("R8, R4, R4, R8") == 4);

  final stopwatchPart2 = Stopwatch()..start();
  print("part 2: ${part2(puzzleInput)}");
  stopwatchPart2.stop();
  print("Elapsed time: ${stopwatchPart2.elapsed}");
}
