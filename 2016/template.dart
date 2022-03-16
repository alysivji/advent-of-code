import 'dart:io';
import 'dart:math';

// ########
// SOLUTION
// ########
List<String> parseInput(String puzzleInput) {
  return puzzleInput.split("\n").map((item) => item.trim()).toList();
}

int part1(puzzleInput) {
  var data = parseInput(puzzleInput);
  return 0;
}

int part2(puzzleInput) {
  var data = parseInput(puzzleInput);
  return 0;
}

// ###########
// RUN PROGRAM
// ###########
void main() {
  String puzzleInput = File('data/dayXX_input.txt').readAsStringSync();
  const TEST_INPUT = "";

  // part 1
  assert(part1(TEST_INPUT) == 5);

  // final stopwatchPart1 = Stopwatch()..start();
  // print("part 1: ${part1(puzzleInput)}");
  // stopwatchPart1.stop();
  // print("Elapsed time: ${stopwatchPart1.elapsed}");

  // part 2
  // assert(part2(TEST_INPUT) == 4);

  // final stopwatchPart2 = Stopwatch()..start();
  // print("part 2: ${part2(puzzleInput)}");
  // stopwatchPart2.stop();
  // print("Elapsed time: ${stopwatchPart2.elapsed}");
}
