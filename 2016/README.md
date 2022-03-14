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

<!-- /TOC -->

## Instructions

Installed Dart 2.16.1 via `homebrew`.

### Run

- VSCode: ``
- Terminal `dart run [path-to-file]`

### Test

<!-- how to test in Dart? -->

## Dart Notes

- Dart is mostly OOP with a few functional constructs like `map`

### Todo

- [x] how to read in a file?
  - https://fluttermaster.com/how-to-read-file-using-dart/
- [x] configure vs code debugger
  - https://dartcode.org/docs/launch-configuration/
- [ ] is there a linter?
- [ ] final vs const
- [ ] clean up how we approach this problem to make it easy to switch between test cases and actual dataset
- [ ] add assert statement for Day 1

## Daily Impressions

### [Day 1: No Time for a Taxicab](https://adventofcode.com/2016/day/1)

Fairly straightforward problem. This is my first time using Dart so I have been looking up modules and syntax as I worked through the problem. Dart does not have native Tuple support; tried a [Google implementation](https://pub.dev/packages/tuple) but it was not right.

The `.toString` method does make life easy if we have to hash small arrays (which we treat as tuples) inside of a Set.
