import 'dart:io';

// ########
// SOLUTION
// ########
List<String> parseInput(String puzzleInput) {
  return puzzleInput.trim().split("\n").map((item) => item.trim()).toList();
}

List<Map<String, int>> countInstancesPerPosition(List<String> messages) {
  var positionCounters = messages[0].split("").map((item) {
    Map<String, int> counter = {};
    return counter;
  }).toList();

  // count instances of each letter for each position
  for (final message in messages) {
    final letters = message.split("");
    for (var i = 0; i < letters.length; i++) {
      final counter = positionCounters[i];
      final letter = letters[i];
      int currentCount = counter.putIfAbsent(letter, () => 0);
      counter[letter] = currentCount + 1;
    }
  }

  return positionCounters;
}

String part1(puzzleInput) {
  var messages = parseInput(puzzleInput);
  var positionCounters = countInstancesPerPosition(messages);

  // decrypt
  var decodedWord = "";
  for (final counter in positionCounters) {
    var sortedCount = counter.entries.toList()
      ..sort((a, b) => b.value.compareTo(a.value));
    decodedWord += sortedCount[0].key;
  }
  return decodedWord;
}

String part2(puzzleInput) {
  var messages = parseInput(puzzleInput);
  var positionCounters = countInstancesPerPosition(messages);

  // decrypt
  var decodedWord = "";
  for (final counter in positionCounters) {
    var sortedCount = counter.entries.toList()
      ..sort((a, b) => a.value.compareTo(b.value));
    decodedWord += sortedCount[0].key;
  }
  return decodedWord;
}

// ###########
// RUN PROGRAM
// ###########
const TEST_INPUT = """eedadn
drvtee
eandsr
raavrd
atevrs
tsrnev
sdttsa
rasrtv
nssdts
ntnada
svetve
tesnvt
vntsnd
vrdear
dvrsen
enarar\n""";

void main() {
  String puzzleInput = File('data/day06_input.txt').readAsStringSync();

  // part 1
  assert(part1(TEST_INPUT) == "easter");

  final stopwatchPart1 = Stopwatch()..start();
  print("part 1: ${part1(puzzleInput)}");
  stopwatchPart1.stop();
  print("Elapsed time: ${stopwatchPart1.elapsed}");

  // part 2
  assert(part2(TEST_INPUT) == "advent");

  final stopwatchPart2 = Stopwatch()..start();
  print("part 2: ${part2(puzzleInput)}");
  stopwatchPart2.stop();
  print("Elapsed time: ${stopwatchPart2.elapsed}");
}
