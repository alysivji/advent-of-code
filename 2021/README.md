# Advent of Code 2021

Learning TypeScript by working my way through through [Advent of Code 2021](https://adventofcode.com/2021).

#### Table of Contents

<!-- TOC -->

- [Instructions](#instructions)
  - [Run](#run)
  - [Test](#test)
  - [Debugging](#debugging)
- [TypeScript Notes](#typescript-notes)
  - [Todo](#todo)
- [Daily Impressions](#daily-impressions)
  - [Day 1: Sonar Sweep](#day-1-sonar-sweep)
  - [Day 2: Dive!](#day-2-dive)
  - [Day 3: Binary Diagnostic](#day-3-binary-diagnostic)
  - [Day 4: Giant Squid](#day-4-giant-squid)
  - [Day 5: Hydrothermal Venture](#day-5-hydrothermal-venture)
  - [Day 6: Lanternfish](#day-6-lanternfish)
  - [Day 7: The Treachery of Whales](#day-7-the-treachery-of-whales)
  - [Day 8: Seven Segment Search](#day-8-seven-segment-search)
  - [Day 9: Smoke Basin](#day-9-smoke-basin)
  - [Day 10: Syntax Scoring](#day-10-syntax-scoring)
  - [Day 11: Dumbo Octopus](#day-11-dumbo-octopus)
  - [Day 12: Passage Pathing](#day-12-passage-pathing)
  - [Day 13: Transparent Origami](#day-13-transparent-origami)
  - [Day 14: Extended Polymerization](#day-14-extended-polymerization)
  - [Day 15: Chiton](#day-15-chiton)
  - [Day 16: Packet Decoder](#day-16-packet-decoder)
  - [Day 17: Packet Decoder](#day-17-packet-decoder)

<!-- /TOC -->

## Instructions

### Run

- VSCode: `F5`
- Terminal: `npx ts-node [path-to-file]`

### Test

Need to figure out how to do it in TS. What testing framework works is a good fit here?

### Debugging

- Use `debugger;` keyword to add breakpoint
- `F5` to start debugger

#### Installation Notes

- install [vscode-ts-debug](https://github.com/hagishi/vscode-ts-debug) and set up launch configuration
- if there are linking errors: `npm link ts-node`

## TypeScript Notes

- Use [spread syntax](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Operators/Spread_syntax) to iterate over Map and Set
  - `[... myMap].map(item => item * 2)`
  - `[... mySet].map(([key, value]) => value)`

### Todo

- [x] get better at handling 2D arrays and adjacent neighbors without having to handle undefined issues
  - created a Grid type; also check if x and y are between a certain range
- [ ] write up helpers for Set operations
- [ ] how to perform a step in function programming
  - do we have to pass a ton of information to the function to keep track?

## Daily Impressions

### [Day 1: Sonar Sweep](https://adventofcode.com/2021/day/1)

I spent some time after work
setting up a TypeScript development environment
so this wasn't as bad as doing things from scratch.
Learning TypeScript is not like Python
when it comes to element-wise array-maps.

Got the problem done, don't think it's the nicest solution,
but we are learning.
What more do I want?

### [Day 2: Dive!](https://adventofcode.com/2021/day/2)

Spent a couple of hours improving my TypeScript development environment by making it easier to run scripts / debug. This was a worthwhile exercise as I was able to focus on writing code versus struggling with developer tooling.

I need to figure out a better way of parsing input to reduce code duplication. Will work on that tomorrow.

TIL: [TypeScript Interfaces](https://www.typescriptlang.org/docs/handbook/interfaces.html)

### [Day 3: Binary Diagnostic](https://adventofcode.com/2021/day/3)

Part 1 was pretty straight-forward. Part 2 took a bit of time to get. Had to calculate it in the REPL vs coming up with a clean solution; it's hard to think in TypeScript... hopefully will get easier as we move along.

### [Day 4: Giant Squid](https://adventofcode.com/2021/day/4)

Created a BingoBoard class to handle the logic of playing Bingo. Using for loops which does not feel right in TypeScript... but it works :shrug:

TIL: Can enumerate the index of a for loop as follows: `for (const [idx, item] of items.entries())`

### [Day 5: Hydrothermal Venture](https://adventofcode.com/2021/day/5)

Cut down on the number of loops I've used which feels good. Not a fan of JavaScript / TypeScript [Maps](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Map) and their lack of iterable methods; really would love a `my_dict.items()` I can map and filter through.

### [Day 6: Lanternfish](https://adventofcode.com/2021/day/6)

Playing catchup... doing this a day later. Part 1 was done in a naive way. Used a better data structure for Part 2. Can probably replace my for loops with reduce calls, but it works so no point.

### [Day 7: The Treachery of Whales](https://adventofcode.com/2021/day/7)

Used the formula for calculating the sum of an infinite series of natural numbers. High school math came in handy!

### [Day 8: Seven Segment Search](https://adventofcode.com/2021/day/8)

This was challenging, especially for being in the middle of the week. Brute forced an algorithm to deduce the numbers... not pretty but gets the job done.

Found a [great solution](https://gist.github.com/bluepichu/94ccd0aed5fb8d1eaf0bc5ae0f39076f) which uses the Set data type from [Immutable.js](https://immutable-js.com/docs/).

### [Day 9: Smoke Basin](https://adventofcode.com/2021/day/9)

This is a simple problem in Python, but not so much in JavaScript. I initially tried to use functional programming techniques, but I'm still getting the hang of FP and mapping through a double array wasn't making a lot of sense.

I tried using immutable.js, but it looks like JavaScript has some issues with doing a `===` check for Maps and Sets which is fine. Ended up installing [`typescript-collections`](https://github.com/basarat/typescript-collections) to have Python-esque Data Structures... but even then the [Set](https://github.com/basarat/typescript-collections/blob/release/src/lib/Set.ts) type does not have a way to pop a random element off.

Also had some problems where `0` is treated like false so when I'm doing a check for `undefined`, `i.e. Map.getValue(xyz) || 10`, `0` is treated like `false` and the result is 10.

Still... got things done by hacking together a solution by stuffing 2D points into a (x, y) coordinate string to have the native Map work as expected.

Fought the language for 2-3 hours... don't feel like I won. Really missed Python today, but definitely learned a lot. At least my `part1()` and `part2()` functions look sort of functional!

Look forward to seeing how experienced TypeScript programmers completed today.

Update: Refactored my solution to use builtin data structures. Have to do a little bit of hacking to store points into dictionaries, but it's better than depending on libraries that don't exactly do what I need so I have to hack anyways.

### [Day 10: Syntax Scoring](https://adventofcode.com/2021/day/10)

This was fairly straight-forward. Feels like I used for loops a bit too much since this is the bracket matching problem and that's my normal way of doing it. Looking forward to seeing other people's better solutions.

### [Day 11: Dumbo Octopus](https://adventofcode.com/2021/day/11)

Another fairly straight-forward puzzle. Only trick was making sure the process was done in the right order. Learned that `[]` is not a falsy value in JavaScript.

[Complete List of JavaScript Falsy Values](https://developer.mozilla.org/en-US/docs/Glossary/Falsy)

### [Day 12: Passage Pathing](https://adventofcode.com/2021/day/12)

My part 2 solution is very slow since I just brute forced it. Takes around 32 seconds to run which is way too long. If I was using Python, I would just use pypy to speed things up and call it a day... but for JS I need some better optimizations.

- [Recursive Solution that I can learn from](https://github.com/joao-conde/advents-of-code/blob/master/2021/src/day12.ts)
- [using strategy pattern](https://github.com/bhosale-ajay/adventofcode/blob/master/2021/ts/D12.test.ts)

### [Day 13: Transparent Origami](https://adventofcode.com/2021/day/13)

I cracked out a piece of paper and figured out the algorithm required to get the answer. Wrote up a console logger to visualize the solution to part 2. Not too bad, but felt a bit messy. Getting better at TypeScript though.

### [Day 14: Extended Polymerization](https://adventofcode.com/2021/day/14)

Started this late as I was playing catchup on previous days so I only got part 1 done in a naive way before I went to bed. Woke up this morning with an idea about keep track of pair counts as we don't really care what the string looks like. Refactored part 1 solution into a solution that works for part 2. Used lodash and a class; fairly happy with my solution.

I feel like I'm over-dependent on tuples since that's what I'm used to in Python. I need to start thinking JSON objects every time I think `tuple`. Thinking in JSON will also let me take advantage of lodash and other fun map-reduce things.

Update: Refactored by making it more functional and taking advantage of JSON objects. Looks a lot nicer. Also making better use of lodash

- [Useful lodash functions](https://geekflare.com/lodash-functions-for-javascript-developers/)

### [Day 15: Chiton](https://adventofcode.com/2021/day/15)

Straight-forward application of pathfinding: used [heap](https://www.npmjs.com/package/heap) + Dijkstra's Algorithm. My part 2 solution runs in 1.2 seconds which is good enough for me. I created a [TypeScript utilities module](../aoc/utilities.ts) to simplify working with grids using the builtin Map and Set data types.

Todo: implement A* and write up a custom implementation of a heap / priority queue.

### [Day 16: Packet Decoder](https://adventofcode.com/2021/day/16)

I had to re-read part 1 a bunch of times before I was able to solve it. Hacked together a solution which created a flat array and then I summed over the version numbers to get the answer.

I knew for part 2, I would need to create a nested data structure to make it easier to solve. I went down the route of creating classes for Operators and Literals and then using functional programming techniques to get the final answer.

Found myself struggling against TypeScript types. Used an interface and class to get to the final solution.

After looking at a [TypeScript solution I found on Reddit](https://github.com/ElCholoGamer/advent-of-code/blob/main/src/days/2021/16.ts), I noticed that I was on the right track but didn't know I could use the `as` keyword to cast union types into a more strict type. I think I like my approach of combining classes and recursion versus doing straight up JSON manipulation and recursion. Feels more readable and easier to extend for other types.

TIL: [parseInt()](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/parseInt) has an optional `radix` parameters that can be used to convert between bases

### [Day 17: Trick Shot](https://adventofcode.com/2021/day/17)

I just brute-forced this once. I think there is a trick involving reducing the search space, but I just played with my for loop ranges until the answer converged. Sometimes it's not worth it.
