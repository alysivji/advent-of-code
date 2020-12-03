# Advent of Code 2019

[AoC 2020](https://adventofcode.com/2020)

## Instructions

### Run

```console
$ ipython
%run 2020/day01_fuel.py
%run 2020/day01_expense_report.py
```

## Test

```console
pytest 2019/day01_fuel.py
pytest 2020/day01_expense_report.py
```

## Daily Impressions

### [Day 1: Report Repair](https://adventofcode.com/2020/day/1)

I tried to solve this in JavaScript,
but it's been a while and setting up a development environment
took longer than I had before work.
Hope to set it up tonight (2020-12-01) or this weekend.

Fell back to Python... hacked together a solution with tests.
Once submitted, when back and generalized it.

### [Day 2: Password Philosophy](https://adventofcode.com/2020/day/2)

It's been a while since I've done RegEx so I decided to use that module.

Used `collections.Counter` to count letters, but apparently strings have a `str.count` method built-in.

### [Day 3: Toboggan Trajectory](https://adventofcode.com/2020/day/3)

This wasn't too bad. Was able to take advantage of the `math.prod` function I learned about while reading other people's solution for Day 1.
