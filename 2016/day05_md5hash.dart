import 'dart:convert';
import 'package:crypto/crypto.dart';

// ########
// SOLUTION
// ########
String generateMd5(String input) {
  return md5.convert(utf8.encode(input)).toString();
}

String part1(puzzleInput) {
  int counter = 0;
  String password = "";
  while (true) {
    String candidateString = puzzleInput + counter.toString();
    String hashedString = generateMd5(candidateString);

    if (hashedString.startsWith("00000")) {
      password += hashedString[5];
    }

    if (password.length == 8) {
      break;
    }
    counter++;
  }
  return password;
}

String part2(puzzleInput) {
  int counter = -1;
  List<String> password = ["*", "*", "*", "*", "*", "*", "*", "*"];

  while (true) {
    counter++;
    String candidateString = puzzleInput + counter.toString();
    String hashedString = generateMd5(candidateString);

    if (hashedString.startsWith("00000")) {
      int characterPosition = int.parse(hashedString[5], radix: 16);
      if (characterPosition > 7) continue;
      if (password[characterPosition] != "*") continue;
      String character = hashedString[6];
      password[characterPosition] = character;
    }

    if (!password.contains("*")) {
      break;
    }
  }
  return password.reduce((a, b) => a + b);
}

// ###########
// RUN PROGRAM
// ###########
void main() {
  // part 1
  // const TEST_INPUT = "abc";
  // assert(part1(TEST_INPUT) == "18f47a30");

  // String puzzleInput = "reyedfim";
  // final stopwatchPart1 = Stopwatch()..start();
  // print("part 1: ${part1(puzzleInput)}");
  // stopwatchPart1.stop();
  // print("Elapsed time: ${stopwatchPart1.elapsed}");

  // part 2
  // const TEST_INPUT = "abc";
  // assert(part2(TEST_INPUT) == "05ace8e3");

  String puzzleInput = "reyedfim";
  final stopwatchPart2 = Stopwatch()..start();
  print("part 2: ${part2(puzzleInput)}");
  stopwatchPart2.stop();
  print("Elapsed time: ${stopwatchPart2.elapsed}");
}
