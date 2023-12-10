import 'dart:collection';
import 'dart:core';
import 'dart:io';
import 'dart:math';

import 'package:collection/collection.dart';

void main() {
  String sampleInput = File('data/day05_sample.txt').readAsStringSync();
  String puzzleInput = File('data/day05_input.txt').readAsStringSync();

  Almanac sampleDataAlmanac = Almanac.fromPuzzleInput(sampleInput);

  // part 1
  assert(sampleDataAlmanac.part1() == 35);
  final stopwatchPart1 = Stopwatch()..start();
  Almanac almanac = Almanac.fromPuzzleInput(puzzleInput);
  print("part 1: ${almanac.part1()}");
  stopwatchPart1.stop();
  print("Elapsed time: ${stopwatchPart1.elapsed}");

  // part 2
  assert(sampleDataAlmanac.part2() == 46);
  final stopwatchPart2 = Stopwatch()..start();
  print("part 2: ${almanac.part2()}");
  stopwatchPart2.stop();
  print("Elapsed time: ${stopwatchPart2.elapsed}");
}

class Almanac {
  List<int> seeds;
  List<AlmanacMap> seedToSoil;
  List<AlmanacMap> soilToFertilizer;
  List<AlmanacMap> fertilizerToWater;
  List<AlmanacMap> waterToLight;
  List<AlmanacMap> lightToTemperature;
  List<AlmanacMap> temperatureToHumidity;
  List<AlmanacMap> humidityToLocation;

  int part1() {
    return seeds
        .map((seed) => applyMap(seedToSoil, seed))
        .map((soil) => applyMap(soilToFertilizer, soil))
        .map((fertilizer) => applyMap(fertilizerToWater, fertilizer))
        .map((water) => applyMap(waterToLight, water))
        .map((light) => applyMap(lightToTemperature, light))
        .map((temperature) => applyMap(temperatureToHumidity, temperature))
        .map((humidity) => applyMap(humidityToLocation, humidity))
        .min;
  }

  static int applyMap(List<AlmanacMap> lookupTable, int valueToLookup) {
    for (var element in lookupTable) {
      if (element.sourceRange.contains(valueToLookup)) {
        int difference = valueToLookup - element.sourceRange.start;
        return element.destimationStart + difference;
      }
    }

    return valueToLookup;
  }

  int part2() {
    List<Range> seedRanges = [];
    for (var i = 0; i < seeds.length; i = i + 2) {
      var item = Range.fromStartAndLength(seeds[i], seeds[i + 1]);
      seedRanges.add(item);
    }

    return seedRanges
        .map((seed) => applyMapToRange(seedToSoil, seed))
        .expand((element) => element)
        .map((soil) => applyMapToRange(soilToFertilizer, soil))
        .expand((element) => element)
        .map((fertilizer) => applyMapToRange(fertilizerToWater, fertilizer))
        .expand((element) => element)
        .map((water) => applyMapToRange(waterToLight, water))
        .expand((element) => element)
        .map((light) => applyMapToRange(lightToTemperature, light))
        .expand((element) => element)
        .map((temperature) =>
            applyMapToRange(temperatureToHumidity, temperature))
        .expand((element) => element)
        .map((humidity) => applyMapToRange(humidityToLocation, humidity))
        .expand((element) => element)
        .map((range) => range.start)
        .min;
  }

  static List<Range> applyMapToRange(
      List<AlmanacMap> lookupTable, Range range) {
    Queue<Range> rangesToTransitionQueue = Queue<Range>();
    rangesToTransitionQueue.add(range);

    List<Range> appliedTransitionRanges = [];
    while (rangesToTransitionQueue.length != 0) {
      var currentRange = rangesToTransitionQueue.removeFirst();
      bool applied = false;
      for (var mapping in lookupTable) {
        if (currentRange.intersectsWith(mapping.sourceRange)) {
          final intersectingRange =
              currentRange.intersection(mapping.sourceRange);
          int difference = mapping.destimationStart - mapping.sourceRange.start;

          Range transitionedRange = Range(intersectingRange.start + difference,
              intersectingRange.end + difference);
          appliedTransitionRanges.add(transitionedRange);

          final unappliedRanges =
              currentRange.intersectionCompliment(mapping.sourceRange);
          rangesToTransitionQueue.addAll(unappliedRanges);
          applied = true;
          break;
        }
      }
      if (!applied) {
        appliedTransitionRanges.add(currentRange);
      }
    }

    return appliedTransitionRanges;
  }

  Almanac(
      this.seeds,
      this.seedToSoil,
      this.soilToFertilizer,
      this.fertilizerToWater,
      this.waterToLight,
      this.lightToTemperature,
      this.temperatureToHumidity,
      this.humidityToLocation);

  factory Almanac.fromPuzzleInput(String input) {
    List<String> groups = input.split("\n\n");

    List<int> seeds = groups[0]
        .split(": ")
        .last
        .split(" ")
        .map((seed) => int.parse(seed))
        .toList();

    var seedToSoil = groups[1]
        .split(":\n")
        .last
        .split("\n")
        .map((line) => AlmanacMap.fromLine(line))
        .toList();

    var soilToFertilizer = groups[2]
        .split(":\n")
        .last
        .split("\n")
        .map((line) => AlmanacMap.fromLine(line))
        .toList();

    var fertilizerToWater = groups[3]
        .split(":\n")
        .last
        .split("\n")
        .map((line) => AlmanacMap.fromLine(line))
        .toList();

    var waterToLight = groups[4]
        .split(":\n")
        .last
        .split("\n")
        .map((line) => AlmanacMap.fromLine(line))
        .toList();

    var lightToTemperature = groups[5]
        .split(":\n")
        .last
        .split("\n")
        .map((line) => AlmanacMap.fromLine(line))
        .toList();

    var temperatureToHumidity = groups[6]
        .split(":\n")
        .last
        .split("\n")
        .map((line) => AlmanacMap.fromLine(line))
        .toList();

    var humidityToLocation = groups[7]
        .split(":\n")
        .last
        .split("\n")
        .where((element) => element != "")
        .map((line) => AlmanacMap.fromLine(line))
        .toList();

    return Almanac(
        seeds,
        seedToSoil,
        soilToFertilizer,
        fertilizerToWater,
        waterToLight,
        lightToTemperature,
        temperatureToHumidity,
        humidityToLocation);
  }

  @override
  String toString() {
    return "seeds=$seeds";
  }
}

class AlmanacMap {
  Range sourceRange;
  int destimationStart;

  AlmanacMap(this.sourceRange, this.destimationStart);

  factory AlmanacMap.fromLine(String line) {
    List<int> parts = line.split(" ").map((value) => int.parse(value)).toList();
    Range sourceRange = Range.fromStartAndLength(parts[1], parts[2]);
    return AlmanacMap(sourceRange, parts[0]);
  }

  @override
  String toString() {
    return "sourceRange=$sourceRange, destimationStart=$destimationStart";
  }
}

class Range {
  int start;
  int end;

  Range(this.start, this.end);

  bool contains(int value) {
    return (start <= value) & (value < end);
  }

  bool intersectsWith(Range other) {
    if (start >= other.start) {
      return (other.start <= start) && (start < other.end);
    }
    return (start <= other.end) && (other.end < end);
  }

  Range intersection(Range other) {
    if (start >= other.start) {
      return Range(min(start, other.end), min(end, other.end));
    }
    return Range(min(other.start, end), min(end, other.end));
  }

  List<Range> intersectionCompliment(Range other) {
    // part of the instance range that is not covered by the intersection
    if (!this.intersectsWith(other)) {
      throw Error();
    }

    if ((other.start <= start) && (end <= other.end)) return [];

    if (start >= other.start) {
      return [Range(max(start, other.end), end)];
    }
    return [Range(start, min(end, other.start))];
  }

  factory Range.fromStartAndLength(int start, int length) {
    return Range(start, start + length);
  }

  @override
  String toString() {
    return "start=$start, end=$end";
  }
}
