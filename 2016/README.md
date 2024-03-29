# Advent of Code 2016

Learning Dart by working my way through [Advent of Code 2016](https://adventofcode.com/2016) (in March 2022).

#### Table of Contents

<!-- TOC -->

- [Instructions](#instructions)
  - [Run](#run)
  - [Test](#test)
- [Dart Notes](#dart-notes)
  - [Todo](#todo)
- [Daily Impressions](#daily-impressions)
  - [Day 1: No Time for a Taxicab](#day-1-no-time-for-a-taxicab)
  - [Day 2: Bathroom Security](#day-2-bathroom-security)
  - [Day 3: Squares With Three Sides](#day-3-squares-with-three-sides)
  - [Day 4: Security Through Obscurity](#day-4-security-through-obscurity)
  - [Day 5: How About a Nice Game of Chess?](#day-5-how-about-a-nice-game-of-chess)
  - [Day 6: Signals and Noise](#day-6-signals-and-noise)
  - [Day 7: Internet Protocol Version 7](#day-7-internet-protocol-version-7)
  - [Day 8: Two-Factor Authentication](#day-8-two-factor-authentication)

<!-- /TOC -->

## Instructions

Installed Dart 2.16.1 via `homebrew`.

### Run

- VSCode: `F5`
- Terminal `dart run [path-to-file]`

### Test

<!-- how to test in Dart? -->

## Dart Notes

- Dart is mostly OOP with a few functional constructs like `map`
- [.removeWhere is like .filter](https://flutterbyexample.com/lesson/removing-elements-remove-clear-remove-where)
- can use [LineSplitter](https://www.woolha.com/tutorials/dart-split-string-by-newline-using-linesplitter) to separate new line characters across all OS
- [cascade notation](https://dart.dev/guides/language/language-tour#cascade-notation) can be used to chain together operations on a single object

### Todo

- [x] how to read in a file?
  - https://fluttermaster.com/how-to-read-file-using-dart/
- [x] configure vs code debugger
  - https://dartcode.org/docs/launch-configuration/
- [ ] is there a linter?
- [ ] final vs const
- [x] clean up how we approach this problem to make it easy to switch between test cases and actual dataset
- [x] add assert statement for Day 1
- [ ] should we start approaching everything with an OOP mindset?
  - very easy to set up equality b/w objects: https://work.j832.com/2014/05/equality-and-dart.html
  - [ ] how lightweight are Dart classes?
- [ ] Found a [Day 6 solution](https://github.com/julemand101/AdventOfCode2016/blob/master/bin/day06/main.dart) that features Multiset and fold
  - if this patterns comes up again; learn what's going on there

## Daily Impressions

Comparing solutions against https://github.com/julemand101/AdventOfCode2016/tree/master/bin

### [Day 1: No Time for a Taxicab](https://adventofcode.com/2016/day/1)

Fairly straightforward problem. This is my first time using Dart so I have been looking up modules and syntax as I worked through the problem. Dart does not have native Tuple support; tried a [Google implementation](https://pub.dev/packages/tuple) but it was not right.

The `.toString` method does make life easy if we have to hash small arrays (which we treat as tuples) inside of a Set. TIL: We can use the [Point class](https://api.flutter.dev/flutter/dart-math/Point-class.html) to represent 2D positions.

### [Day 2: Bathroom Security](https://adventofcode.com/2016/day/2)

Used `Point` and `Map` to build a key-value data structure for all the values in the Number Pad. Still trying to find a good way to organize Dart scripts. I think my template will be more helpful tomorrow than it was today.

### [Day 3: Squares With Three Sides](https://adventofcode.com/2016/day/3)

Had to reach into the RegEx toolbox today to parse the puzzle data. Dart arrow functions are used to define a single expression. When using functional programming functions (`map`, `reduce`, and `forEach`), we have to use the regular function syntax to pass in functions.

### [Day 4: Security Through Obscurity](https://adventofcode.com/2016/day/4)

Converting my input data into Objects and used straight forward OOP to solve this problem. Need to do some research into how lightweight Dart classes are, but I can see this being a powerful way to handle JSON-like data.

I can start to see how Dart is a powerful language -- it's syntax gets out of the way letting you get classes up and running really quickly.

#### Day 4 TIL

- Regex non-capturing groups start with `?:`
- `final` keyword in Dart is similar to how we use `const` in ES6 and TS
- Dart OOP -- creating classes, getters, setters, etc

### [Day 5: How About a Nice Game of Chess?](https://adventofcode.com/2016/day/5)

Today was a brute-force problem that used the MD5 algorithm (via Dart's [crypto](https://pub.dev/packages/crypto) package) to calculate a hash. It took around 50 seconds for each of my solutions to run.

Once I learn Flutter, this will be a fun one to animate.

### [Day 6: Signals and Noise](https://adventofcode.com/2016/day/6)

A simple counting puzzle. 2016 is pretty straightforward so far.

### [Day 7: Internet Protocol Version 7](https://adventofcode.com/2016/day/7)

Lots of text manipulation in this puzzle. Wrote a function to process each line and then I solved this problem in a fairly functional way.

### [Day 8: Two-Factor Authentication](https://adventofcode.com/2016/day/8)

This was took a bit longer than expected. Used a very Object-Oriented solution, but got wires mixed up with rows / columns vs y / x. Really liking Dart; can't seem to find anything about naming function parameters... but I need to do a bit more research.
