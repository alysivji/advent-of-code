# Advent of Code 2021

Strengthening my TS skills by working my way through [Advent of Code 2024](https://adventofcode.com/2024).

#### Table of Contents

<!-- TOC -->

- [Daily Impressions](#daily-impressions)
  - [Day 1: Historian Hysteria](#day-1-historian-hysteria)
  - [Day 2: Red-Nosed Reports](#day-2-red-nosed-reports)
  - [Day 3: Mull It Over](#day-3-mull-it-over)

<!-- /TOC -->

## Daily Impressions

### [Day 1: Historian Hysteria](https://adventofcode.com/2024/day/1)

Today was easy. Since JavaScript doesn't have a `defaultdict`, it's messier than if I had used Python. :shrug: Need to see how other people solved it so I can start writing idiomatic TS.

### [Day 2: Red-Nosed Reports](https://adventofcode.com/2024/day/2)

Surprisingly hard puzzle... it's not really hard but I'm really rusty with my [JavaScript Array methods](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Array). [Array.slice](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Array/slice) and [Array.splice](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Array/splice) FTW!

Pretty happy with my solution minus the for loop. Interested to see how people do this using pure functional paradigm.

### [Day 3: Mull It Over](https://adventofcode.com/2024/day/3)

I haven't used Regular Expressions in JavaScript since probably AoC 2021. This was a great puzzle and learned a bit about RegEx. [Mozilla Web Docs](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Guide/Regular_expressions) FTW!

Once I was done the code, I refactored and used a boolean to turn on/off conditionals in my `runProgram` function. If we keep going down this path ala IntCode, I'll refactor into a `class`.
