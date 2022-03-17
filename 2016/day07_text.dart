import 'dart:io';

// ########
// SOLUTION
// ########
List<String> parseInput(String puzzleInput) {
  return puzzleInput.trim().split("\n").map((item) => item.trim()).toList();
}

List<List<dynamic>> parseLine(String line) {
  final supernetSequences = [];
  final hypernetSequences = [];
  var currentPosition = 0;
  while (currentPosition < line.length) {
    int startBracketPos = line.substring(currentPosition).indexOf("[");
    int endBracketPos = line.substring(currentPosition).indexOf("]");

    if (startBracketPos > 0 && startBracketPos < endBracketPos) {
      final word =
          line.substring(currentPosition, currentPosition + startBracketPos);
      supernetSequences.add(word);
      currentPosition += startBracketPos + 1;
    } else if (endBracketPos > 0) {
      final word =
          line.substring(currentPosition, currentPosition + endBracketPos);
      hypernetSequences.add(word);
      currentPosition += endBracketPos + 1;
    } else if (startBracketPos < 0 && endBracketPos < 0) {
      final word = line.substring(currentPosition);
      supernetSequences.add(word);
      currentPosition = line.length;
    }
  }

  return [supernetSequences, hypernetSequences];
}

bool containsFourLetterPalindrome(String word) {
  for (int i = 0; i < word.length; i++) {
    try {
      var sequence = word.substring(i, i + 4);

      if (sequence.substring(0, 1) != sequence.substring(3, 4)) continue;
      if (sequence.substring(1, 2) != sequence.substring(2, 3)) continue;
      if (sequence.substring(0, 1) == sequence.substring(1, 2)) continue;

      return true;
    } catch (RangeError) {
      return false;
    }
  }
  return false;
}

bool supportsTls(String line) {
  var parsedSequences = parseLine(line);
  final supernetSequences = parsedSequences[0]
      .map((word) => containsFourLetterPalindrome(word))
      .toList();
  final hypernetSequences = parsedSequences[1]
      .map((word) => containsFourLetterPalindrome(word))
      .toList();

  if (hypernetSequences.contains(true)) return false;
  if (supernetSequences.contains(true)) return true;

  return false;
}

int part1(puzzleInput) {
  return parseInput(puzzleInput)
      .map((line) => supportsTls(line))
      .toList()
      .where((value) => value)
      .length;
}

List<String> findThreeLetterPalindrome(word) {
  List<String> palindromes = [];

  for (int i = 0; i < word.length; i++) {
    try {
      var sequence = word.substring(i, i + 3);

      if (sequence.substring(0, 1) != sequence.substring(2, 3)) continue;
      if (sequence.substring(0, 1) == sequence.substring(1, 2)) continue;

      palindromes.add(sequence);
    } catch (RangeError) {
      continue;
    }
  }
  return palindromes;
}

bool supportSsl(String line) {
  var parsedSequences = parseLine(line);
  final supernetPalindromes = parsedSequences[0]
      .map((word) => findThreeLetterPalindrome(word))
      .expand((element) => element)
      .toList();

  final hypernetHasReversePalindrome = parsedSequences[1].map((word) {
    for (final palindrome in supernetPalindromes) {
      final textToCheck = "${palindrome[1]}${palindrome[0]}${palindrome[1]}";
      if (word.contains(textToCheck)) return true;
    }
    return false;
  });

  return hypernetHasReversePalindrome.contains(true);
}

int part2(puzzleInput) {
  return parseInput(puzzleInput)
      .map((line) => supportSsl(line))
      .toList()
      .where((value) => value)
      .length;
}

// ###########
// RUN PROGRAM
// ###########
const TEST_INPUT1 = """abba[mnop]qrst
abcd[bddb]xyyx
aaaa[qwer]tyui
ioxxoj[asdfgh]zxcvbn\n""";

const TEST_INPUT2 = """aba[bab]xyz
xyx[xyx]xyx
aaa[kek]eke
zazbz[bzb]cdb\n""";

void main() {
  String puzzleInput = File('data/day07_input.txt').readAsStringSync();

  // part 1
  assert(part1(TEST_INPUT1) == 2);

  final stopwatchPart1 = Stopwatch()..start();
  print("part 1: ${part1(puzzleInput)}");
  stopwatchPart1.stop();
  print("Elapsed time: ${stopwatchPart1.elapsed}");

  // part 2
  assert(part2(TEST_INPUT2) == 3);

  final stopwatchPart2 = Stopwatch()..start();
  print("part 2: ${part2(puzzleInput)}");
  stopwatchPart2.stop();
  print("Elapsed time: ${stopwatchPart2.elapsed}");
}
