import 'dart:core';
import 'dart:io';

import 'package:collection/collection.dart';

void main() {
  String sampleInput = File('2023/data/day06_sample.txt').readAsStringSync();
  String puzzleInput = File('2023/data/day06_input.txt').readAsStringSync();

  // part 1
  assert(part1(sampleInput) == 288);
  final stopwatchPart1 = Stopwatch()..start();
  print("part 1: ${part1(puzzleInput)}");
  stopwatchPart1.stop();
  print("Elapsed time: ${stopwatchPart1.elapsed}");

  // part 2
  assert(part2(sampleInput) == 71503);
  final stopwatchPart2 = Stopwatch()..start();
  print("part 2: ${part2(puzzleInput)}");
  stopwatchPart2.stop();
  print("Elapsed time: ${stopwatchPart2.elapsed}");
}

int part1(input) {
  List<String> times = input.split("\n").first.split(":").last.split(" ");
  times.removeWhere((element) => element == "");

  List<String> distance = input.split("\n")[1].split(":").last.split(" ");
  distance.removeWhere((element) => element == "");

  return IterableZip([times, distance])
      .map((pair) => Race.fromStringPair(pair[0], pair[1]))
      .toList()
      .map((race) => race.numberOfWaysToWin())
      .reduce((value, element) => value * element);
}

int part2(input) {
  List<String> times = input.split("\n").first.split(":").last.split(" ");
  times.removeWhere((element) => element == "");
  String time = times.reduce((value, element) => value + element);

  List<String> distances = input.split("\n")[1].split(":").last.split(" ");
  distances.removeWhere((element) => element == "");
  String distance = distances.reduce((value, element) => value + element);

  Race race = Race.fromStringPair(time, distance);
  return race.numberOfWaysToWin();
}

class Race {
  int time;
  int distance;

  Race(this.time, this.distance);

  factory Race.fromStringPair(String timeStr, String distanceStr) {
    return Race(int.tryParse(timeStr)!, int.tryParse(distanceStr)!);
  }

  @override
  String toString() {
    return "Race(time=$time, distance=$distance)";
  }

  int numberOfWaysToWin() {
    List<int> boats = List.generate(time + 1, (index) => index);
    return boats
        .map((speed) => speed * (time - speed))
        .where((d) => d > distance)
        .length;
  }
}
