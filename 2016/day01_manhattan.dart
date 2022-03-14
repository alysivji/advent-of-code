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

void main() {
  String contents = File('data/day01_input.txt').readAsStringSync();
  List<String> path = contents.split(",").map((item) => item.trim()).toList();

  print(calculateManhattanDistance(resultingDistance(path), [0, 0]));
  print(calculateManhattanDistance(firstLocationVisitedTwice(path), [0, 0]));
}
