import 'dart:io';

final roomRegex = RegExp(r'^((?:[a-z]+-*)+)-(\d+)\[([a-z]+)\]$');

class Room {
  String encryptedName;
  int sectorId;
  String checksum;

  Room(this.encryptedName, this.sectorId, this.checksum);

  isRealRoom() {
    // count all characters
    // https://api.dart.dev/stable/2.16.0/dart-core/Map/putIfAbsent.html
    Map<String, int> counter = {};
    for (final letter in this.encryptedName.split("")) {
      if (letter == "-") continue;
      int currentCount = counter.putIfAbsent(letter, () => 0);
      counter[letter] = currentCount + 1;
    }

    // sort counter by value (descending) and letter (ascending)
    // https://stackoverflow.com/questions/61343000/dart-sort-list-by-two-properties
    var sortedCount = counter.entries.toList()
      ..sort((a, b) {
        if (a.value != b.value) {
          return b.value.compareTo(a.value);
        } else {
          return a.key.compareTo(b.key);
        }
      });

    var checksum = sortedCount
        .sublist(0, 5)
        .map((item) => item.key)
        .reduce((a, b) => "${a}${b}");

    return checksum == this.checksum;
  }

  // https://dart.dev/codelabs/dart-cheatsheet#getters-and-setters
  String get decryptedName {
    final characterShift = this.sectorId % 26;
    final lowerAAscii = "a".codeUnitAt(0);

    var decryptedName = "";
    for (var i = 0; i < this.encryptedName.length; i++) {
      final letter = this.encryptedName[i];
      if (letter == "-") {
        decryptedName += " ";
        continue;
      }

      var shiftedCode =
          ((letter.codeUnitAt(0) - lowerAAscii) + characterShift) % 26 +
              lowerAAscii;
      final decryptedLetter = String.fromCharCode(shiftedCode);

      decryptedName += decryptedLetter;
    }

    return decryptedName;
  }
}

// ########
// SOLUTION
// ########
List<Room> parseInput(String puzzleInput) {
  return puzzleInput.trim().split("\n").map((line) {
    var match = roomRegex.firstMatch(line)!;
    final encryptedName = match.group(1)!;
    final sectorId = int.parse(match.group(2)!);
    final checksum = match.group(3)!;
    return Room(encryptedName, sectorId, checksum);
  }).toList();
}

int part1(puzzleInput) {
  var allRooms = parseInput(puzzleInput);
  allRooms.removeWhere((room) => !room.isRealRoom());
  return allRooms.map((item) => item.sectorId).reduce((a, b) => a + b);
}

int part2(puzzleInput) {
  var allRooms = parseInput(puzzleInput);
  allRooms.removeWhere((room) => !room.isRealRoom());
  for (final room in allRooms) {
    if (room.decryptedName.contains("northpole")) {
      return room.sectorId;
    }
  }
  throw Exception("should not get here");
}

// ###########
// RUN PROGRAM
// ###########
const TEST_INPUT = """aaaaa-bbb-z-y-x-123[abxyz]
a-b-c-d-e-f-g-h-987[abcde]
not-a-real-room-404[oarel]
totally-real-room-200[decoy]\n""";

void main() {
  String puzzleInput = File('data/day04_input.txt').readAsStringSync();

  // part 1
  assert(part1(TEST_INPUT) == 1514);

  final stopwatchPart1 = Stopwatch()..start();
  print("part 1: ${part1(puzzleInput)}");
  stopwatchPart1.stop();
  print("Elapsed time: ${stopwatchPart1.elapsed}");

  // part 2
  final testRoom = Room("qzmt-zixmtkozy-ivhz", 343, "abcde");
  assert(testRoom.decryptedName == "very encrypted name");

  final stopwatchPart2 = Stopwatch()..start();
  print("part 2: ${part2(puzzleInput)}");
  stopwatchPart2.stop();
  print("Elapsed time: ${stopwatchPart2.elapsed}");
}
