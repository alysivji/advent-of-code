import 'dart:collection';
import 'dart:core';
import 'dart:io';

import '../aoc/utilities.dart';

void main() {
  // Sample data
  String sampleInput = File('data/day10_sample.txt').readAsStringSync();
  Grid sampleGrid = Grid.fromPuzzleInput(sampleInput);
  assert(sampleGrid.part1() == 4);

  sampleInput = File('data/day10_sample2.txt').readAsStringSync();
  sampleGrid = Grid.fromPuzzleInput(sampleInput);
  assert(sampleGrid.part1() == 8);

  String puzzleInput = File('data/day10_input.txt').readAsStringSync();

  // part 1
  final stopwatchPart1 = Stopwatch()..start();
  Grid grid = Grid.fromPuzzleInput(puzzleInput);
  print("part 1: ${grid.part1()}");
  stopwatchPart1.stop();
  print("Elapsed time: ${stopwatchPart1.elapsed}");
}

class Grid {
  Map<Point, Set<Point>> pipeMap;
  Point start;

  Grid(this.pipeMap, this.start);

  int part1() {
    return findLoopSize() ~/ 2;
  }

  int findLoopSize() {
    Set<Point> visited = {};
    Queue<Point> toVisit = Queue<Point>();

    int step = 0;
    visited.add(start);
    toVisit.add(pipeMap[start]!.first);
    while (toVisit.length != 0) {
      var currPoint = toVisit.removeFirst();
      visited.add(currPoint);
      step++;
      toVisit.addAll(pipeMap[currPoint]!
          .toList()
          .where((point) => !visited.contains(point)));
    }

    return step + 1;
  }

  factory Grid.fromPuzzleInput(String input) {
    Map<Point, Set<Point>> pipeMap = {};
    Point start = Point(-1, -1);

    input
        .split("\n")
        .where((line) => line.length != 0)
        .toList()
        .asMap()
        .entries
        .forEach((entry) {
      var y = entry.key;
      var line = entry.value;

      line.split("").asMap().entries.forEach((entry) {
        var x = entry.key;
        Point p = Point(x, y);

        switch (entry.value) {
          case '|':
            pipeMap[p] = {p.north(), p.south()};
            break;
          case '-':
            pipeMap[p] = {p.east(), p.west()};
            break;
          case 'L':
            pipeMap[p] = {p.north(), p.east()};
            break;
          case 'J':
            pipeMap[p] = {p.north(), p.west()};
            break;
          case '7':
            pipeMap[p] = {p.south(), p.west()};
            break;
          case 'F':
            pipeMap[p] = {p.south(), p.east()};
            break;
          case 'S':
            start = p;
            break;
        }
      });
    });

    // add start's neighbours to pipe map
    var startNeighbours = pipeMap.entries
        .where((entry) => entry.value.contains(start))
        .map((entry) => entry.key);
    pipeMap[start] = Set.from(startNeighbours);

    return Grid(pipeMap, start);
  }
}
