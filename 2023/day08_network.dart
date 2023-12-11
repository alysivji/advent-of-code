import 'dart:core';
import 'dart:io';

// generated this from ChatGPT -- asked about how I can copy itertools.cycle
Stream<T> cycle<T>(Iterable<T> iterable) async* {
  if (iterable.isEmpty) {
    return;
  }
  while (true) {
    for (T element in iterable) {
      yield element;
    }
  }
}

int gcd(int a, int b) {
  return b == 0 ? a : gcd(b, a % b);
}

int lcm(int a, int b) {
  return (a * b) ~/ gcd(a, b);
}

int lcmOfList(List<int> numbers) {
  return numbers.reduce((currentLcm, number) => lcm(currentLcm, number));
}

void main() async {
  // Sample data
  String sampleInput = File('data/day08_sample.txt').readAsStringSync();
  Network sampleNetwork = Network.fromPuzzleInput(sampleInput);
  assert(await sampleNetwork.numStepsForHumans() == 2);

  sampleInput = File('data/day08_sample2.txt').readAsStringSync();
  sampleNetwork = Network.fromPuzzleInput(sampleInput);
  assert(await sampleNetwork.numStepsForHumans() == 6);

  sampleInput = File('data/day08_sample3.txt').readAsStringSync();
  sampleNetwork = Network.fromPuzzleInput(sampleInput);
  assert(await sampleNetwork.numStepsForGhosts() == 6);

  String puzzleInput = File('data/day08_input.txt').readAsStringSync();

  // part 1
  final stopwatchPart1 = Stopwatch()..start();
  Network network = Network.fromPuzzleInput(puzzleInput);
  print("part 1: ${await network.numStepsForHumans()}");
  stopwatchPart1.stop();
  print("Elapsed time: ${stopwatchPart1.elapsed}");

  // part 2
  final stopwatchPart2 = Stopwatch()..start();
  network = Network.fromPuzzleInput(puzzleInput);
  print("part 2: ${await network.numStepsForGhosts()}");
  stopwatchPart2.stop();
  print("Elapsed time: ${stopwatchPart2.elapsed}");
}

class Network {
  String directions;
  Map<String, Node> nodes;

  Network(this.directions, this.nodes);

  Future<int> numStepsForHumans() async {
    Stream<String> directionCycle = cycle(directions.split("").toList());

    int numSteps = 0;
    Node currentNode = nodes["AAA"]!;
    await for (String direction in directionCycle) {
      if (direction == "L") {
        currentNode = nodes[currentNode.left]!;
      } else {
        currentNode = nodes[currentNode.right]!;
      }
      numSteps++;
      if (currentNode.name == "ZZZ") break;
    }

    return numSteps;
  }

  Future<int> numStepsForGhosts() async {
    List<Node> currentNodes =
        nodes.values.where((node) => node.name.endsWith("A")).toList();

    var futures = currentNodes.map((node) {
      return numStepsForGhostForSinglePath(node.name);
    }).toList();

    List<int> numStepsToEnd = await Future.wait(futures);

    return lcmOfList(numStepsToEnd);
  }

  Future<int> numStepsForGhostForSinglePath(String startNodeName) async {
    Stream<String> directionCycle = cycle(directions.split("").toList());
    int numSteps = 0;

    Node currentNode = nodes[startNodeName]!;
    await for (String direction in directionCycle) {
      if (direction == "L") {
        currentNode = nodes[currentNode.left]!;
      } else {
        currentNode = nodes[currentNode.right]!;
      }
      numSteps++;
      if (currentNode.name.endsWith("Z")) break;
    }

    return numSteps;
  }

  factory Network.fromPuzzleInput(String input) {
    List<String> groups = input.split("\n\n");
    String directions = groups.first;

    Map<String, Node> nodes = {};
    groups.last
        .split("\n")
        .where((line) => line.length > 0)
        .map((line) => Node.fromLine(line))
        .forEach((node) {
      nodes[node.name] = node;
    });

    return Network(directions, nodes);
  }
}

class Node {
  String name;
  String left;
  String right;

  Node(this.name, this.left, this.right);

  factory Node.fromLine(String line) {
    List<String> parts = line.split(" = ");
    String name = parts[0];

    List<String> directions = parts.last.split(", ");
    String left = directions.first.substring(1);
    String right = directions.last.substring(0, 3);

    return Node(name, left, right);
  }

  @override
  String toString() {
    return "name=$name, left=$left, right=$right";
  }
}
