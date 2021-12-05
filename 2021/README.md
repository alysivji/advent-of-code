# Advent of Code 2021

[AoC 2021](https://adventofcode.com/2021)

## Instructions

### Run

- VSCode: `F5`
- Terminal: `npx ts-node [path-to-file]`

## Test

Need to figure out how to do it in TS. What testing framework works is a good fit here?

## Debugging

- Use `debugger;` keyword to add breakpoint
- `F5` to start debugger

### Installation Notes

- install [vscode-ts-debug](https://github.com/hagishi/vscode-ts-debug) and set up launch configuration
- if there are linking errors: `npm link ts-node`

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
