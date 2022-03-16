import 'dart:io';

final triangleRegex = RegExp(r'(\d+)\s+(\d+)\s+(\d+)$');

// ########
// SOLUTION
// ########
List<List<int>> parseInputByRow(String puzzleInput) {
  return puzzleInput.trim().split("\n").map((line) {
    var match = triangleRegex.firstMatch(line)!;
    List<int> sides = [];
    sides.add(int.parse(match.group(1)!));
    sides.add(int.parse(match.group(2)!));
    sides.add(int.parse(match.group(3)!));
    return sides;
  }).toList();
}

List<List<int>> parseInputVerticalGroupsOfThree(String puzzleInput) {
  List<List<int>> triangles = [];
  int sideCounter = 0;
  var test = puzzleInput.trim().split("\n");

  List<List<int>> allTriangles = [];
  List<int> triangle1 = [];
  List<int> triangle2 = [];
  List<int> triangle3 = [];
  for (final line in test) {
    sideCounter += 1;
    var match = triangleRegex.firstMatch(line)!;
    triangle1.add(int.parse(match.group(1)!));
    triangle2.add(int.parse(match.group(2)!));
    triangle3.add(int.parse(match.group(3)!));

    if (sideCounter % 3 == 0) {
      allTriangles.add(triangle1);
      allTriangles.add(triangle2);
      allTriangles.add(triangle3);

      triangle1 = [];
      triangle2 = [];
      triangle3 = [];
    }
  }

  return allTriangles;
}

bool isValidTriangle(List<int> sides) {
  num longestSide = sides.reduce((a, b) => (b > a) ? b : a);
  num sumRemainingSides = sides.reduce((a, b) => a + b) - longestSide;
  return sumRemainingSides > longestSide;
}

int numValidTriangles(List<List<int>> triangleData) {
  var numValidTriangles = 0;
  for (final triangle in triangleData) {
    if (isValidTriangle(triangle)) numValidTriangles += 1;
  }
  return numValidTriangles;
}

int part1(puzzleInput) {
  var triangleData = parseInputByRow(puzzleInput);
  return numValidTriangles(triangleData);
}

int part2(puzzleInput) {
  var triangleData = parseInputVerticalGroupsOfThree(puzzleInput);
  return numValidTriangles(triangleData);
}

// ###########
// RUN PROGRAM
// ###########
const TEST_INPUT1 = "5 10 25\n";
const TEST_INPUT2 = """101 301 501
102 302 502
103 303 503
201 401 601
202 402 602
203 403 603\n""";

void main() {
  String puzzleInput = File('data/day03_input.txt').readAsStringSync();

  // part 1
  print(part1(TEST_INPUT1));
  assert(part1(TEST_INPUT1) == 0);

  final stopwatchPart1 = Stopwatch()..start();
  print("part 1: ${part1(puzzleInput)}");
  stopwatchPart1.stop();
  print("Elapsed time: ${stopwatchPart1.elapsed}");

  // part 2
  assert(part2(TEST_INPUT2) == 6);

  final stopwatchPart2 = Stopwatch()..start();
  print("part 2: ${part2(puzzleInput)}");
  stopwatchPart2.stop();
  print("Elapsed time: ${stopwatchPart2.elapsed}");
}
