# Advent of Code 2021

Learning TypeScript by working my way through through [Advent of Code 2021](https://adventofcode.com/2021).

#### Table of Contents

<!-- TOC -->

- [Instructions](#instructions)
  - [Run](#run)
  - [Test](#test)
  - [Debugging](#debugging)
  - [Installation Notes](#installation-notes)
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

### Installation Notes

- install [vscode-ts-debug](https://github.com/hagishi/vscode-ts-debug) and set up launch configuration
- if there are linking errors: `npm link ts-node`

## TypeScript Notes

- Use [spread syntax](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Operators/Spread_syntax) to iterate over Map and Set
  - `[... myMap].map(item => item * 2)`
  - `[... mySet].map(([key, value]) => value)`

### Todo

- [ ] get better at handling 2D arrays and adjacent neighbors without having to handle undefined issues
- [ ] write up helpers for Set operations

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

[Recursive Solution that I can learn from](https://github.com/joao-conde/advents-of-code/blob/master/2021/src/day12.ts)
