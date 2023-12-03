import 'dart:core';
import 'dart:convert';
import 'dart:io';

const String sampleData =
    """Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green
Game 2: 1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue
Game 3: 8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red
Game 4: 1 green, 3 red, 6 blue; 3 green, 6 red; 3 green, 15 blue, 14 red
Game 5: 6 red, 1 blue, 3 green; 2 blue, 1 red, 2 green
""";

void main() {
  String puzzleInput = File('2023/data/day02_input.txt').readAsStringSync();

  // part 1
  CubeGame sampleGame = CubeGame(sampleData);
  assert(sampleGame.part1() == 8);

  final stopwatchPart1 = Stopwatch()..start();
  CubeGame game = CubeGame(puzzleInput);
  print("part 1: ${game.part1()}");
  stopwatchPart1.stop();
  print("Elapsed time: ${stopwatchPart1.elapsed}");

  // part 2
  assert(sampleGame.part2() == 2286);

  final stopwatchPart2 = Stopwatch()..start();
  print("part 2: ${game.part2()}");
  stopwatchPart2.stop();
  print("Elapsed time: ${stopwatchPart2.elapsed}");
}

class CubeGame {
  late List<GameLog> gameResults;

  CubeGame(String gameInput) {
    LineSplitter ls = new LineSplitter();
    List<String> lines = ls.convert(gameInput);

    this.gameResults = [];
    lines.forEach((line) {
      GameLog game = GameLog(line);
      this.gameResults.add(game);
    });
  }

  int part1() {
    const int maxRed = 12;
    const int maxGreen = 13;
    const int maxBlue = 14;

    List<GameLog> possibleGames = [];
    this.gameResults.forEach((game) {
      bool isPossible = true;
      game.pulls.forEach((pull) {
        if ((pull.numRed > maxRed) |
            (pull.numGreen > maxGreen) |
            (pull.numBlue > maxBlue)) {
          isPossible = false;
        }
      });

      if (isPossible) {
        possibleGames.add(game);
      }
    });

    int possibleSum = 0;
    possibleGames.forEach((element) {
      possibleSum += element.id;
    });

    return possibleSum;
  }

  int part2() {
    int cubePowerSum = 0;
    this.gameResults.forEach((game) {
      int maxRed = 0;
      int maxGreen = 0;
      int maxBlue = 0;

      game.pulls.forEach((pull) {
        if (pull.numRed > maxRed) {
          maxRed = pull.numRed;
        }
        if (pull.numBlue > maxBlue) {
          maxBlue = pull.numBlue;
        }
        if (pull.numGreen > maxGreen) {
          maxGreen = pull.numGreen;
        }
      });

      int cubePower = maxBlue * maxGreen * maxRed;
      cubePowerSum += cubePower;
    });

    return cubePowerSum;
  }
}

class GameLog {
  late int id;
  late List<CubesPulled> pulls;

  GameLog(String line) {
    List<String> parts = line.split(": ");

    List<String> gameParts = parts[0].split(" ");
    this.id = int.parse(gameParts[1]);

    List<String> cubePulls = parts[1].split("; ");

    this.pulls = [];
    cubePulls.forEach((cubePull) {
      List<String> cubes = cubePull.split(", ");

      int numRed = 0;
      int numGreen = 0;
      int numBlue = 0;

      cubes.forEach((element) {
        if (element.endsWith("green")) {
          List<String> result = element.split(" ");
          numGreen = int.parse(result[0]);
        }

        if (element.endsWith("blue")) {
          List<String> result = element.split(" ");
          numBlue = int.parse(result[0]);
        }

        if (element.endsWith("red")) {
          List<String> result = element.split(" ");
          numRed = int.parse(result[0]);
        }
      });

      CubesPulled item = CubesPulled(numRed, numGreen, numBlue);
      this.pulls.add(item);
    });
  }
}

class CubesPulled {
  int numRed;
  int numGreen;
  int numBlue;

  CubesPulled(this.numRed, this.numGreen, this.numBlue);
}
