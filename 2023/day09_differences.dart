import 'dart:core';
import 'dart:io';

void main() {
  // Sample data
  String sampleInput = File('data/day09_sample.txt').readAsStringSync();
  String puzzleInput = File('data/day09_input.txt').readAsStringSync();

  OasisSensor sampleOasisSensor = OasisSensor.fromPuzzleInputPart1(sampleInput);
  assert(sampleOasisSensor.sumExtrapolatedValues() == 114);

  sampleOasisSensor = OasisSensor.fromPuzzleInputPart2(sampleInput);
  assert(sampleOasisSensor.sumExtrapolatedValues() == 2);

  // part 1
  final stopwatchPart1 = Stopwatch()..start();
  OasisSensor oasisSensor = OasisSensor.fromPuzzleInputPart1(puzzleInput);
  print("part 1: ${oasisSensor.sumExtrapolatedValues()}");
  stopwatchPart1.stop();
  print("Elapsed time: ${stopwatchPart1.elapsed}");

  // part 2
  final stopwatchPart2 = Stopwatch()..start();
  oasisSensor = OasisSensor.fromPuzzleInputPart2(puzzleInput);
  print("part 2: ${oasisSensor.sumExtrapolatedValues()}");
  stopwatchPart2.stop();
  print("Elapsed time: ${stopwatchPart2.elapsed}");
}

class OasisSensor {
  List<List<int>> valueHistories;

  OasisSensor(this.valueHistories);

  int sumExtrapolatedValues() {
    return valueHistories
        .map((valueHistory) => extrapolateValue(valueHistory))
        .reduce((value, element) => value + element);
  }

  static int extrapolateValue(List<int> numbers) {
    // reduce until the differences are 0 and then bubble value back up

    List<int> differences = numbers
        .asMap()
        .entries
        .map((entry) {
          int index = entry.key;
          if (index == 0) return null;
          return entry.value - numbers[index - 1];
        })
        .where((step) => step != null)
        // TIL -- you can cast
        .cast<int>()
        .toList();

    // TIL -- every
    if (differences.every((step) => step == 0)) {
      return numbers[numbers.length - 1];
    }

    return numbers[numbers.length - 1] + extrapolateValue(differences);
  }

  factory OasisSensor.fromPuzzleInputPart1(String input) {
    var valueHistories = input
        .split("\n")
        .where((line) => line.length != 0)
        .map((line) => line.split(" ").map((e) => int.parse(e)).toList())
        .toList();

    return OasisSensor(valueHistories);
  }

  factory OasisSensor.fromPuzzleInputPart2(String input) {
    var valueHistories = input
        .split("\n")
        .where((line) => line.length != 0)
        .map((line) =>
            line.split(" ").map((e) => int.parse(e)).toList().reversed.toList())
        .toList();

    return OasisSensor(valueHistories);
  }
}
