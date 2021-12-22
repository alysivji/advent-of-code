import fs from "fs";
import assert from "assert";
import _ from "lodash";

// ########
// SOLUTION
// ########
const parseInput = (puzzleInput: string) => {
  return puzzleInput.split("\n").map((line) => eval(line));
};
type NestedArray<T> = Array<T | NestedArray<T>>;

const nestedArrayToTree = (arr: NestedArray<number>): Node => {
  const leftElement = arr[0];
  const rightElement = arr[1];

  let node: Node;
  if (typeof leftElement === "number" && typeof rightElement === "number") {
    node = new Node(leftElement, rightElement);
  } else if (
    typeof leftElement === "number" &&
    typeof rightElement !== "number"
  ) {
    node = new Node(leftElement, nestedArrayToTree(rightElement));
  } else if (
    typeof leftElement !== "number" &&
    typeof rightElement === "number"
  ) {
    node = new Node(nestedArrayToTree(leftElement), rightElement);
  } else if (
    typeof leftElement !== "number" &&
    typeof rightElement !== "number"
  ) {
    node = new Node(
      nestedArrayToTree(leftElement),
      nestedArrayToTree(rightElement),
    );
  } else {
    throw new Error("cannot reach");
  }
  return node;
};

const reduceNumber = (root: Node) => {
  while (true) {
    const nodeToExplode = findLeftmostPairToExplode(root);
    const nodeToSplit = findNodeToExpand(root);

    if (nodeToExplode === null && nodeToSplit == null) break;

    if (nodeToExplode !== null) {
      const inorderSnailfish = inorderElementTraversal(root);
      const explosionIndex = inorderSnailfish.indexOf(nodeToExplode);
      if (explosionIndex === -1) throw new Error("cannot find node in array");

      // add number to previous
      const beforeIdx = explosionIndex - 1;
      if (beforeIdx >= 0) {
        if (typeof inorderSnailfish[beforeIdx].right === "number") {
          inorderSnailfish[beforeIdx].right =
            nodeToExplode.left_ + inorderSnailfish[beforeIdx].right_;
        } else {
          inorderSnailfish[beforeIdx].left =
            nodeToExplode.left_ + inorderSnailfish[beforeIdx].left_;
        }
      }

      // add number to next
      const afterIdx = explosionIndex + 1;
      if (afterIdx < inorderSnailfish.length) {
        if (typeof inorderSnailfish[afterIdx].left === "number") {
          inorderSnailfish[afterIdx].left =
            nodeToExplode.right_ + inorderSnailfish[afterIdx].left_;
        } else {
          inorderSnailfish[afterIdx].right =
            nodeToExplode.right_ + inorderSnailfish[afterIdx].right_;
        }
      }

      const parent = findParent(root, nodeToExplode)!;
      if (Object.is(parent.left, nodeToExplode)) {
        parent.left = 0;
        continue;
      }

      if (Object.is(parent.right, nodeToExplode)) {
        parent.right = 0;
        continue;
      }
    }

    if (nodeToSplit !== null) {
      if (typeof nodeToSplit.left === "number") {
        const left = nodeToSplit.left_;
        if (left >= 10) {
          const leftElement = Math.floor(left / 2);
          const rightElement = Math.ceil(left / 2);
          nodeToSplit.left = new Node(leftElement, rightElement);
          continue;
        }
      }

      if (typeof nodeToSplit.right === "number") {
        const right = nodeToSplit.right_;
        if (right >= 10) {
          const leftElement = Math.floor(right / 2);
          const rightElement = Math.ceil(right / 2);
          nodeToSplit.right = new Node(leftElement, rightElement);
          continue;
        }
      }
    }
  }

  return root;
};

const calculateMagnitude = (root: Node): number => {
  if (root.isLeafNode()) return 3 * root.left_ + 2 * root.right_;
  else if (typeof root.left === "number" && typeof root.right !== "number") {
    return 3 * root.left + 2 * calculateMagnitude(root.right);
  } else if (typeof root.left !== "number" && typeof root.right === "number") {
    return 3 * calculateMagnitude(root.left) + 2 * root.right;
  } else if (typeof root.left !== "number" && typeof root.right !== "number") {
    return (
      3 * calculateMagnitude(root.left) + 2 * calculateMagnitude(root.right)
    );
  }

  throw new Error("can't reach here");
};

// Tree Data Structure and Tree Algorithms
class Node {
  left;
  right;

  constructor(left: Node | number, right: Node | number) {
    this.left = left;
    this.right = right;
  }

  isLeafNode(): boolean {
    return typeof this.left === "number" && typeof this.right === "number";
  }

  get left_(): number {
    return parseInt(this.left.toString());
  }
  get right_(): number {
    return parseInt(this.right.toString());
  }
}

const findLeftmostPairToExplode = (root: Node): Node | null => {
  const toVisit = [{ node: root, level: 0 }];
  while (toVisit.length !== 0) {
    const current = toVisit.pop()!;
    if (current.node.isLeafNode() && current.level >= 4) return current.node;

    if (typeof current.node.right !== "number") {
      toVisit.push({ node: current.node.right, level: current.level + 1 });
    }

    if (typeof current.node.left !== "number") {
      toVisit.push({ node: current.node.left, level: current.level + 1 });
    }
  }

  return null;
};

const findNodeToExpand = (root: Node) => {
  const a = inorderElementTraversal(root);
  for (const node of inorderElementTraversal(root)) {
    if (typeof node.left === "number") {
      if (node.left_ >= 10) return node;
    }

    if (typeof node.right === "number") {
      if (node.right_ >= 10) return node;
    }
  }

  return null;
};

const inorderElementTraversal = (root: Node) => {
  // go through tree and find elements in the order they would be seen in a list
  const validNodes: Node[] = [];
  if (root.isLeafNode()) {
    return [root];
  }

  if (typeof root.left === "number") {
    validNodes.push(root);
  } else {
    validNodes.push(...inorderElementTraversal(root.left));
  }

  if (typeof root.right === "number") {
    validNodes.push(root);
  } else {
    validNodes.push(...inorderElementTraversal(root.right));
  }

  return validNodes;
};

const findParent = (root: Node, nodeToFind: Node) => {
  const nodesToSearch = [root];
  while (nodesToSearch.length != 0) {
    const currNode = nodesToSearch.pop()!;
    if (
      Object.is(currNode.left, nodeToFind) ||
      Object.is(currNode.right, nodeToFind)
    )
      return currNode;

    if (typeof currNode.right !== "number") nodesToSearch.push(currNode.right);
    if (typeof currNode.left !== "number") nodesToSearch.push(currNode.left);
  }

  return null;
};

// ###########
// RUN PROGRAM
// ###########
// Answer
const TEST_INPUT = `[[[0,[5,8]],[[1,7],[9,6]]],[[4,[1,2]],[[1,4],2]]]
[[[5,[2,8]],4],[5,[[9,9],0]]]
[6,[[[6,2],[5,6]],[[7,6],[4,7]]]]
[[[6,[0,7]],[0,9]],[4,[9,[9,0]]]]
[[[7,[6,4]],[3,[1,3]]],[[[5,5],1],9]]
[[6,[[7,3],[3,2]]],[[[3,8],[5,7]],4]]
[[[[5,4],[7,7]],8],[[8,3],8]]
[[9,3],[[9,9],[6,[4,9]]]]
[[2,[[7,7],7]],[[5,8],[[9,3],[0,2]]]]
[[[[5,2],5],[8,[3,7]]],[[5,[7,5]],[4,4]]]`;

const puzzleInput = fs
  .readFileSync("2021/data/day18_input.txt")
  .toString()
  .trim();

// part 1
const part1 = (puzzleInput: string) => {
  const snailfishArrays = parseInput(puzzleInput);
  const snailfishRoots = snailfishArrays.map((arr) => nestedArrayToTree(arr));
  const finalNum = snailfishRoots.reduce((result, b) => {
    const newNum = new Node(result, b);
    return reduceNumber(newNum);
  });
  return calculateMagnitude(finalNum);
};
// assert(part1(TEST_INPUT) === 4140);
console.time("part 1");
console.log(part1(puzzleInput));
console.timeEnd("part 1");

// part 2
const part2 = (puzzleInput: string) => {
  const snailfishArrays = parseInput(puzzleInput);

  let largestMagnitutude = -Infinity;
  for (let i = 0; i < snailfishArrays.length; i++) {
    for (let j = 0; j < snailfishArrays.length; j++) {
      if (i == j) continue;
      const newNum = new Node(
        nestedArrayToTree(snailfishArrays[i]),
        nestedArrayToTree(snailfishArrays[j]),
      );
      const reducedNum = reduceNumber(newNum);
      if (calculateMagnitude(reducedNum) > largestMagnitutude) {
        largestMagnitutude = calculateMagnitude(reducedNum);
      }
    }
  }
  return largestMagnitutude;
};
assert(part2(TEST_INPUT) === 3993);
console.time("part 2");
console.log(part2(puzzleInput));
console.timeEnd("part 2");
