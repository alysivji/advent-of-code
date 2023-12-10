import 'dart:convert';
import 'dart:core';
import 'dart:io';

const CARD_RANK = [
  "2",
  "3",
  "4",
  "5",
  "6",
  "7",
  "8",
  "9",
  "T",
  "J",
  "Q",
  "K",
  "A"
];

void main() {
  // Sample data
  // String sampleInput = File('data/day07_sample.txt').readAsStringSync();
  // CamelCardsGame sampleDataGame = CamelCardsGame.fromPuzzleInput(sampleInput);
  // assert(sampleDataGame.part1() == 6440);

  String puzzleInput = File('data/day07_input.txt').readAsStringSync();

  // part 1
  final stopwatchPart1 = Stopwatch()..start();
  CamelCardsGame game = CamelCardsGame.fromPuzzleInput(puzzleInput);
  print("part 1: ${game.part1()}");
  stopwatchPart1.stop();
  print("Elapsed time: ${stopwatchPart1.elapsed}");

  // // part 2
  // assert(part2(sampleInput) == 71503);
  // final stopwatchPart2 = Stopwatch()..start();
  // print("part 2: ${part2(puzzleInput)}");
  // stopwatchPart2.stop();
  // print("Elapsed time: ${stopwatchPart2.elapsed}");
}

class CamelCardsGame {
  List<Hand> hands;

  int part1() {
    hands.sort();
    int totalWinnings = 0;

    for (final (index, hand) in hands.indexed) {
      totalWinnings += hand.bid * (index + 1);
    }

    return totalWinnings;
  }

  CamelCardsGame(this.hands);

  factory CamelCardsGame.fromPuzzleInput(String input) {
    LineSplitter ls = new LineSplitter();
    List<String> lines = ls.convert(input);

    List<Hand> allHands = lines
        .where((line) => line.length > 0)
        .map((line) => Hand.fromLine(line))
        .toList();

    return CamelCardsGame(allHands);
  }
}

class Hand implements Comparable<Hand> {
  String cards;
  int bid;

  Hand(this.cards, this.bid);

  int get type => _type();
  int _type() {
    Map<String, int> counts = {};

    for (String card in cards.split("")) {
      counts[card] = (counts[card] ?? 0) + 1;
    }

    if (counts.values.contains(5)) return 6;
    if (counts.values.contains(4)) return 5;
    if (counts.values.contains(3) & counts.values.contains(2)) return 4;
    if (counts.values.contains(3)) return 3;
    if (counts.values.where((count) => count == 2).length == 2) return 2;
    if (counts.values.contains(2)) return 1;
    return 0;
  }

  @override
  int compareTo(Hand other) {
    if (this.type != other.type) {
      return this.type - other.type;
    }

    for (int i = 0; i < this.cards.length; i++) {
      if (CARD_RANK.indexOf(this.cards[i]) == CARD_RANK.indexOf(other.cards[i]))
        continue;

      return CARD_RANK.indexOf(this.cards[i]) -
          CARD_RANK.indexOf(other.cards[i]);
    }

    // should not get here
    throw Error();
  }

  factory Hand.fromLine(String line) {
    List<String> parts = line.split(" ");
    return Hand(parts[0], int.tryParse(parts[1])!);
  }

  @override
  String toString() {
    return "cards=$cards, bid=$bid";
  }
}
