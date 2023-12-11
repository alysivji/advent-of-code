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

const CARD_RANK_WITH_WILDCARD = [
  "J",
  "2",
  "3",
  "4",
  "5",
  "6",
  "7",
  "8",
  "9",
  "T",
  "Q",
  "K",
  "A"
];

void main() {
  // Sample data
  String sampleInput = File('data/day07_sample.txt').readAsStringSync();
  CamelCardsGame sampleDataGame =
      CamelCardsGame.fromPuzzleInput(sampleInput, false);
  assert(sampleDataGame.getTotalWinnings() == 6440);
  sampleDataGame = CamelCardsGame.fromPuzzleInput(sampleInput, true);
  assert(sampleDataGame.getTotalWinnings() == 5905);

  String puzzleInput = File('data/day07_input.txt').readAsStringSync();

  // part 1
  final stopwatchPart1 = Stopwatch()..start();
  CamelCardsGame game = CamelCardsGame.fromPuzzleInput(puzzleInput, false);
  print("part 1: ${game.getTotalWinnings()}");
  stopwatchPart1.stop();
  print("Elapsed time: ${stopwatchPart1.elapsed}");

  // part 2
  final stopwatchPart2 = Stopwatch()..start();
  game = CamelCardsGame.fromPuzzleInput(puzzleInput, true);
  print("part 2: ${game.getTotalWinnings()}");
  stopwatchPart2.stop();
  print("Elapsed time: ${stopwatchPart2.elapsed}");
}

class CamelCardsGame {
  List<Hand> hands;

  int getTotalWinnings() {
    hands.sort();

    return hands
        .asMap()
        .entries
        .map((entry) => entry.value.bid * (entry.key + 1))
        .reduce((a, b) => a + b);
  }

  CamelCardsGame(this.hands);

  factory CamelCardsGame.fromPuzzleInput(String input, bool jacksAreWild) {
    LineSplitter ls = new LineSplitter();
    List<String> lines = ls.convert(input);

    List<Hand> allHands = lines
        .where((line) => line.length > 0)
        .map((line) => Hand.fromLine(line, jacksAreWild))
        .toList();

    return CamelCardsGame(allHands);
  }
}

class Hand implements Comparable<Hand> {
  String cards;
  int bid;
  bool jacksAreWild = false;

  Hand(this.cards, this.bid, this.jacksAreWild);

  int get type => _type();
  int _type() {
    Map<String, int> counts = {};

    for (String card in cards.split("")) {
      counts[card] = (counts[card] ?? 0) + 1;
    }

    if ((jacksAreWild) && (counts.keys.contains("J"))) {
      int numWildCards = counts["J"] ?? 0;
      counts["J"] = 0;

      var sortedCardByCount = counts.entries.toList();
      sortedCardByCount.sort((a, b) {
        int valueComparison = b.value.compareTo(a.value);
        if (valueComparison != 0) {
          return valueComparison;
        }
        return CARD_RANK_WITH_WILDCARD
            .indexOf(a.key)
            .compareTo(CARD_RANK_WITH_WILDCARD.indexOf(b.key));
      });

      var entry = sortedCardByCount[0];
      counts[entry.key] = (counts[entry.key] ?? 0) + numWildCards;
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
      if (this.cards[i] == other.cards[i]) continue;

      if (jacksAreWild) {
        return CARD_RANK_WITH_WILDCARD.indexOf(this.cards[i]) -
            CARD_RANK_WITH_WILDCARD.indexOf(other.cards[i]);
      }

      return CARD_RANK.indexOf(this.cards[i]) -
          CARD_RANK.indexOf(other.cards[i]);
    }

    // should not get here
    throw Error();
  }

  factory Hand.fromLine(String line, bool jacksAreWild) {
    List<String> parts = line.split(" ");
    return Hand(parts[0], int.tryParse(parts[1])!, jacksAreWild);
  }

  @override
  String toString() {
    return "cards=$cards, bid=$bid";
  }
}
