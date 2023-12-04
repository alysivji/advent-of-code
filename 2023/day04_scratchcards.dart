import 'dart:convert';
import 'dart:core';
import 'dart:io';
import 'dart:math';

void main() {
  String sampleInput = File('2023/data/day04_sample.txt').readAsStringSync();
  String puzzleInput = File('2023/data/day04_input.txt').readAsStringSync();

  // part 1
  Game gameSampleData = Game(sampleInput);
  assert(gameSampleData.score() == 13);

  final stopwatchPart1 = Stopwatch()..start();
  Game game = Game(puzzleInput);
  print("part 1: ${game.score()}");
  stopwatchPart1.stop();
  print("Elapsed time: ${stopwatchPart1.elapsed}");

  // // part 2
  assert(gameSampleData.totalNumberOfScratchersPlayed() == 30);

  final stopwatchPart2 = Stopwatch()..start();
  print("part 2: ${game.totalNumberOfScratchersPlayed()}");
  stopwatchPart2.stop();
  print("Elapsed time: ${stopwatchPart2.elapsed}");
}

class Game {
  Map<int, ScratchCard> scratchCards = {};

  num score() {
    // Part 1
    num totalScore = 0;
    scratchCards.values.forEach((card) {
      totalScore += card.score();
    });
    return totalScore;
  }

  int totalNumberOfScratchersPlayed() {
    // Part 2
    Map<int, int> cardCounts = {};

    // start with 1 scratcher of each
    for (var i = 0; i < scratchCards.keys.length; i++) {
      int cardId = i + 1;
      cardCounts[cardId] = 1;
    }

    // scratch
    for (var i = 0; i < scratchCards.keys.length; i++) {
      int cardId = i + 1;
      int numCards = cardCounts[cardId]!;

      int scratchersWon = scratchCards[cardId]!.numMatch();

      for (var j = cardId + 1; j <= cardId + scratchersWon; j++) {
        cardCounts[j] = cardCounts[j]! + numCards;
      }
    }

    return cardCounts.values.reduce((value, element) => value + element);
  }

  Game(String input) {
    LineSplitter ls = new LineSplitter();
    List<String> lines = ls.convert(input);

    for (final (index, line) in lines.indexed) {
      int cardId = index + 1;
      scratchCards[cardId] = ScratchCard(index + 1, line);
    }
  }
}

class ScratchCard {
  late int cardId;
  late Set<int> winningNumbers = {};
  late Set<int> myNumbers = {};

  int numMatch() {
    return myNumbers.intersection(winningNumbers).length;
  }

  num score() {
    if (numMatch() == 0) return 0;

    return pow(2, numMatch() - 1);
  }

  ScratchCard(int cardId, String line) {
    this.cardId = cardId;

    List<String> parts = line.split(": ");
    List<String> numberParts = parts[1].split(" | ");

    numberParts[0].split(" ").forEach((element) {
      if (isInt(element)) {
        winningNumbers.add(int.parse(element));
      }
    });
    numberParts[1].split(" ").forEach((element) {
      if (isInt(element)) {
        myNumbers.add(int.parse(element));
      }
    });
  }
}

// https://stackoverflow.com/questions/24085385/checking-if-string-is-numeric-in-dart
isInt(string) => int.tryParse(string) != null;
