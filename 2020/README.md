# Advent of Code 2020

[AoC 2020](https://adventofcode.com/2020)

## Instructions

### Run

```console
$ ipython
%run 2020/day01_expense_report.py
```

## Test

```console
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

TIL: `str.count`

### [Day 3: Toboggan Trajectory](https://adventofcode.com/2020/day/3)

This wasn't too bad. Was able to take advantage of the `math.prod` function I learned about while reading other people's solution for Day 1.

### [Day 4: Passport Processing](https://adventofcode.com/2020/day/4)

Validating data without a serializer is not a lot of fun. It took me a few attempts to get this question correct... my RegEx-es were not accurate enough.

TIL: Make sure to start and end strings with `^` and `$`

### [Day 5: Binary Boarding](https://adventofcode.com/2020/day/5)

Finally got a JavaScript environment set up using [parcel](https://parceljs.org/). Have to use Node since I'm reading files from disk and have no idea how to debug except for using `console.log`, but that's the point. Only way to get better in an ecosystem is to work in that ecosystem until you are comfortable.

The problem wasn't too hard, spent most of my time re-learning how to basic things in JavaScript.

TIL: `Array.sort` does not sort numbers, have to use `.sort((a, b) => { return a - b; })` instead.

### [Day 6: Custom Customs](https://adventofcode.com/2020/day/6)

Today was pretty easy. Have a bunch of stuff to do today so I went back to Python to get it done. Question would have taken me a 20-30 minutes longer in JavaScript.

Took advantage of the `.split("\n\n")` trick to read blank lines. Thanks to Wim in the Chicago Python Slack for the tip!

### [Day 7: Handy Haversacks](https://adventofcode.com/2020/day/7)

First hard-ish puzzle of the year! Stuck with Python since I have an 8:30 meeting in the morning and only had an hour to finish.

Used a graph search for Part 1 since I figured Part 2 would require it.

### [Day 8: Handheld Halting](https://adventofcode.com/2020/day/8)

Today's puzzle was reminiscent of last year's IntCode Calculator. I just wrote up some if statments and called it a day for part 1. Part 2 required me to add a check to my part 1 function to ensure that it had halted.

Probably a good idea to refactor my computer into a class. A wise man once said that [`if` statements are a code smell](https://www.youtube.com/watch?v=P0kfKqMHioQ) and it's more likely than not future problems will build upon this one.

### [Day 9: Encoding Error](https://adventofcode.com/2020/day/9)

This felt very similar to day 1. Was pretty straightforward.
