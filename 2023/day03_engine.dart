import 'dart:core';
import 'dart:convert';
import 'dart:io';

void main() {
  String sampleInput = File('2023/data/day03_sample.txt').readAsStringSync();
  String puzzleInput = File('2023/data/day03_input.txt').readAsStringSync();

  // part 1
  Engine engineSampleData = Engine(sampleInput);
  assert(engineSampleData.part1() == 4361);

  final stopwatchPart1 = Stopwatch()..start();
  Engine engine = Engine(puzzleInput);
  print("part 1: ${engine.part1()}");
  stopwatchPart1.stop();
  print("Elapsed time: ${stopwatchPart1.elapsed}");

  // part 2
  assert(engineSampleData.part2() == 467835);

  final stopwatchPart2 = Stopwatch()..start();
  print("part 2: ${engine.part2()}");
  stopwatchPart2.stop();
  print("Elapsed time: ${stopwatchPart2.elapsed}");
}

// https://stackoverflow.com/questions/24085385/checking-if-string-is-numeric-in-dart
isInt(string) => int.tryParse(string) != null;

class Engine {
  late Map<Point, String> symbolLocations = {};
  late Map<Point, int> pointToClusterId = {};
  late Map<int, int> clusterInformation = {};

  int part1() {
    Set<int> clustersFound = {};

    symbolLocations.keys.forEach((symbolLocation) {
      symbolLocation.adjacent8().forEach((pointToCheck) {
        if (pointToClusterId.containsKey(pointToCheck)) {
          clustersFound.add(pointToClusterId[pointToCheck]!);
        }
      });
    });

    int sumPartNumbers = 0;
    clustersFound.forEach((element) {
      sumPartNumbers = sumPartNumbers + clusterInformation[element]!;
    });
    return sumPartNumbers;
  }

  int part2() {
    Map<Point, Set<int>> gearClusters = {};
    symbolLocations.entries.forEach((symbolLocation) {
      if (symbolLocation.value == "*") {
        symbolLocation.key.adjacent8().forEach((pointToCheck) {
          if (pointToClusterId.containsKey(pointToCheck)) {
            if (!gearClusters.containsKey(symbolLocation.key)) {
              gearClusters[symbolLocation.key] = {};
            }
            gearClusters[symbolLocation.key]!
                .add(pointToClusterId[pointToCheck]!);
          }
        });
      }
    });

    gearClusters.removeWhere((key, value) => value.length != 2);

    int sumGearRatios = 0;
    gearClusters.forEach((key, value) {
      int gearRatio = 1;
      value.forEach((element) {
        gearRatio = gearRatio * clusterInformation[element]!;
      });
      sumGearRatios += gearRatio;
    });

    return sumGearRatios;
  }

  Engine(String input) {
    LineSplitter ls = new LineSplitter();
    List<String> lines = ls.convert(input);
    int clusterCounter = 1;

    for (final (y, line) in lines.indexed) {
      bool parsingNumber = false;
      String currentNumber = "";
      int startX = 0;

      for (final (x, value) in line.split("").indexed) {
        // check if number
        if (isInt(value)) {
          currentNumber += value;
          if (!parsingNumber) {
            parsingNumber = true;
            startX = x;
          }

          if (!(x == line.length - 1)) continue;
        }

        // if we are parsing number, check more things
        if (parsingNumber) {
          int partNumber = int.parse(currentNumber);
          for (var newX = startX; newX < x; newX++) {
            pointToClusterId[Point(newX, y)] = clusterCounter;
          }
          if (x == line.length - 1) {
            pointToClusterId[Point(x, y)] = clusterCounter;
          }
          clusterInformation[clusterCounter] = partNumber;
          currentNumber = "";
          clusterCounter += 1;
          parsingNumber = false;
        }

        // handle symbols
        if ((value != ".") & !isInt(value)) {
          symbolLocations[Point(x, y)] = value;
        }
      }
    }
  }
}

class Point {
  int x;
  int y;

  Iterable<Point> adjacent8() {
    List<Vector> vectors = [
      Vector(-1, 0),
      Vector(1, 0),
      Vector(0, 1),
      Vector(0, -1),
      Vector(1, 1),
      Vector(1, -1),
      Vector(-1, 1),
      Vector(-1, -1),
    ];

    return vectors.map((vector) => this + vector);
  }

  Point operator +(Vector vector) {
    return Point(x + vector.xDiff, y + vector.yDiff);
  }

  @override
  bool operator ==(Object other) {
    if (other is! Point) return false;
    if (x != other.x) return false;
    if (y != other.y) return false;
    return true;
  }

  @override
  int get hashCode => Object.hash(x, y);

  @override
  String toString() {
    return "$x, $y";
  }

  Point(this.x, this.y);
}

class Vector {
  int xDiff;
  int yDiff;

  Vector(this.xDiff, this.yDiff);
}
