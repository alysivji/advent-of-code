# Advent of Code 2024

Strengthening my TS skills by working my way through [Advent of Code 2024](https://adventofcode.com/2024).

#### Table of Contents

<!-- TOC -->

- [Daily Impressions](#daily-impressions)
  - [Day 1: Historian Hysteria](#day-1-historian-hysteria)
  - [Day 2: Red-Nosed Reports](#day-2-red-nosed-reports)
  - [Day 3: Mull It Over](#day-3-mull-it-over)
  - [Day 4: Ceres Search](#day-4-ceres-search)
  - [Day 5: Print Queue](#day-5-print-queue)
  - [Day 6: Guard Gallivant](#day-6-guard-gallivant)
  - [Day 7: Bridge Repair](#day-7-bridge-repair)
  - [Day 8: Resonant Collinearity](#day-8-resonant-collinearity)
  - [Day 9: Disk Fragmenter](#day-9-disk-fragmenter)
- [Todo](#todo)

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

### [Day 4: Ceres Search](https://adventofcode.com/2024/day/4)

I attempted this puzzle right when it came out, but I forgot that JavaScript Maps and Sets store keys as values if passing in an `object`. Took a week off, came back and wrote up a utility module that has helpers that make JS' data structures function like Python NamedTuples (how I miss thee...).

Once that was done, I was able to write up some hybrid code -- functional shell to perform the calculation, object-oriented core to manage the grid data structure. I'm happy with the code, but I could probably refactor a bit to make part 1 and part 2 flow smoothly.

Did have a bit of a `eureka` moment when I figured out a better way to do a for loop with a `map` and then again using `filter` and keeping the exact data structure I need for the next set of steps. But again, feels like I have this moment everytime I do something complex with functional code vs the standard React DOM mappings. This is my first proper TypeScript job so I'm hoping a lot of the concepts stick.

A+++++ puzzle. Would buy from again.

### [Day 5: Print Queue](https://adventofcode.com/2024/day/5)

Part 1 was pretty straight forward. Had to refactor a bit to set things up for Part 2. I was wondering if I could use something like `permutations` to not have to think, but this was not a brute force solution. Looked at the data a few times before I saw the pattern. Took longer than I'd like to admin.

Update -- saw on reddit that people created a custom comparison function -- which makes sense since we know to sort two numbers.

### [Day 6: Guard Gallivant](https://adventofcode.com/2024/day/6)

Completed using an imperative approach. Honestly, I'm not quite sure how I'd make this functional. Part 2 was brute-forced and took 15 seconds. I should be doing better here, but solving a puzzle is solving a puzzle... especially since I'm over a week behind.

Created a wrapper around the native `Set` to have it work with my custom `Point` class.

[Some optimizations from Reddit](https://www.reddit.com/r/adventofcode/comments/1h7z9sj/2024_day_6_pt_2_what_optimisations_are_there/):
- put obstacles on the original path vs every single point
  - implemented
- store direction in the "seen" set so we can find cycles if something repeats by comparing point and the direction that the guard walks
- do not iterate over every point, you can teleport the guard to the step before the obstacle
  - this is probably a good one to do, but honestly I don't really want to implement it

### [Day 7: Bridge Repair](https://adventofcode.com/2024/day/7)

I was thinking about using permutations for this one but 12 choose 12 is a very big number so there definitely must have been another way. Found a recursive solution that worked for part 1, but not part 2 since I recursed backwards vs forwards. Ran into some issues during the part 2 implementation that made me realize I could more easily solve this by recursing forward.

Felt really comfortable to write the solution in TypeScript. Also, learned about [structuredClone()](https://developer.mozilla.org/en-US/docs/Web/API/Window/structuredClone)

### [Day 8: Resonant Collinearity](https://adventofcode.com/2024/day/8)

Read through this one almost a couple of weeks ago, but didn't want to spend the time doing yet another grid problem. Came back to it after a while since I have to do some algorithmic thinking for a side project I need to do and this was good practice.

Hacked togethered a solution for Part 1 in a functional way. For Part 2, I had to refactor a bit since my solution was more or less hard coded for part 1. New approach was a bit more functional, but to get things done, I buried a `while` loop in there as iteration made more sense for the problem at hand. Can clean things up, but :shrug: not worth the effort.

### [Day 9: Disk Fragmenter](https://adventofcode.com/2024/day/9)

I brute-forced it. This was not a fun problem. I feel like this year's AoC has been a bit of a slog with us doing a lot of the same type of iteration tricks.

## Todo

- [ ] Day 5 -- create custom comparison function
- [x] Day 6 -- implement some of the optimizations
- [ ] Day 6 -- figure out how to do functionally
