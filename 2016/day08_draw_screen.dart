import 'dart:io';
import 'dart:math';

// ########
// SOLUTION
// ########
class Screen {
  int rows;
  int columns;
  late Map<Point, String> _grid;

  Screen(this.columns, this.rows) {
    this._grid = {};
    for (int x = 0; x < this.columns; x++) {
      for (int y = 0; y < this.rows; y++) {
        this._grid[Point(x, y)] = " ";
      }
    }
  }

  Map<Point, String> get grid {
    return this._grid;
  }

  bool draw(int x, int y, String value) {
    try {
      this._grid[Point(x, y)] = value;
    } catch (RangeError) {
      return false;
    }

    return true;
  }

  int countLitPixels() {
    int counter = 0;
    for (int y = 0; y < this.rows; y++) {
      String output = "";
      for (int x = 0; x < this.columns; x++) {
        if (this._grid[Point(x, y)]! == "#") counter++;
      }
    }
    return counter;
  }

  void writeToScreen() {
    for (int y = 0; y < this.rows; y++) {
      String output = "";
      for (int x = 0; x < this.columns; x++) {
        output += this._grid[Point(x, y)]!;
      }
      print(output);
    }
    print("");
  }
}

abstract class Command {
  void draw(Screen screen) {}
}

class RectangleCommand extends Command {
  int rows;
  int columns;

  RectangleCommand(this.columns, this.rows);

  void draw(Screen screen) {
    for (int x = 0; x < this.columns; x++) {
      for (int y = 0; y < this.rows; y++) {
        screen.draw(x, y, "#");
      }
    }
  }
}

class RotationCommand extends Command {
  String type;
  int axisValueToRotate;
  int rotationDistance;

  RotationCommand(this.type, this.axisValueToRotate, this.rotationDistance);

  void draw(screen) {
    // get points on screen
    List<String> pixels = [];
    if (this.type == "column") {
      for (int y = 0; y < screen.rows; y++) {
        pixels.add(screen.grid[Point(this.axisValueToRotate, y)]!);
      }
    } else {
      for (int x = 0; x < screen.columns; x++) {
        pixels.add(screen.grid[Point(x, this.axisValueToRotate)]!);
      }
    }

    // rotate
    var updatedPixels = List.from(pixels);
    for (int i = 0; i < pixels.length; i++) {
      var indexToUpdate = (i + this.rotationDistance) % pixels.length;
      updatedPixels[indexToUpdate] = pixels[i];
    }

    // place back on screen
    if (this.type == "column") {
      for (int y = 0; y < pixels.length; y++) {
        screen.draw(this.axisValueToRotate, y, updatedPixels[y]);
      }
    } else {
      for (int x = 0; x < pixels.length; x++) {
        screen.draw(x, this.axisValueToRotate, updatedPixels[x]);
      }
    }
  }
}

List<Command> parseInput(String puzzleInput) {
  return puzzleInput.trim().split("\n").map((line) {
    var parts = line.split(" ");
    if (parts[0] == "rect") {
      var dimension = parts[1].split("x");
      return RectangleCommand(int.parse(dimension[0]), int.parse(dimension[1]));
    }

    var stepSize = parts[2].split("=");
    return RotationCommand(
      parts[1],
      int.parse(stepSize[1]),
      int.parse(parts[4]),
    );
  }).toList();
}

int solveProblem(puzzleInput) {
  var commands = parseInput(puzzleInput);
  var screen = new Screen(50, 6);
  for (final command in commands) {
    command.draw(screen);
  }
  screen.writeToScreen();
  return screen.countLitPixels();
}

// ###########
// RUN PROGRAM
// ###########
void main() {
  String puzzleInput = File('data/day08_input.txt').readAsStringSync();
  String TEST_INPUT = File('data/day08_test.txt').readAsStringSync();

  // part 1
  assert(solveProblem(TEST_INPUT) == 6);

  final stopwatchPart1 = Stopwatch()..start();
  print("part 1: ${solveProblem(puzzleInput)}");
  stopwatchPart1.stop();
  print("Elapsed time: ${stopwatchPart1.elapsed}");

  // part 2 is drawn to the screen
}
