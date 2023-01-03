# Advent of Code 2021

Learning Go by working my way through [Advent of Code 2022](https://adventofcode.com/2022).

#### Table of Contents

- [Daily Impressions](#daily-impressions)
  - [Day 1: Calorie Counting](#day-1-calorie-counting)
  - [Day 2: Rock Paper Scissors](#day-2-rock-paper-scissors)
  - [Day 3: Rucksack Reorganization](#day-3-rucksack-reorganization)
  - [Day 4: Camp Cleanup](#day-4-camp-cleanup)
  - [Day 5: Supply Stacks](#day-5-supply-stacks)
  - [Day 6: Tuning Trouble](#day-6-tuning-trouble)
  - [Day 7: No Space Left On Device](#day-7-no-space-left-on-device)
  - [Day 8: Treetop Tree House](#day-8-treetop-tree-house)
  - [Day 9: Rope Bridge](#day-9-rope-bridge)
  - [Day 10: Cathode-Ray Tube](#day-10-cathode-ray-tube)
  - [Day 11: Monkey in the Middle](#day-11-monkey-in-the-middle)
  - [Day 12: Hill Climbing Algorithm](#day-12-hill-climbing-algorithm)
  - [Day 13](#day-13)
  - [Day 14: Regolith Reservoir](#day-14-regolith-reservoir)
  - [Day 15: Beacon Exclusion Zone](#day-15-beacon-exclusion-zone)
  - [Day 16](#day-16)

## Daily Impressions

### [Day 1: Calorie Counting](https://adventofcode.com/2022/day/1)

Fairly straight forward problem, but this was my first time writing a Go program so I struggled a ton.

TODO: look at solutions to figure out how to

### [Day 2: Rock Paper Scissors](https://adventofcode.com/2022/day/2)

[Good ole rock, nothing beats that](https://www.youtube.com/watch?v=b0SoKWLkmLU)

Today was a mess. Had to learn how to write Go code across multiple files.... which is a lot harder than it sounds.

Overall the logic was easy; still struggling with the lnguage

### [Day 3: Rucksack Reorganization](https://adventofcode.com/2022/day/3)

> If you work with Go programming, you quickly realize there are no concept sets. However, we can play some tricks with maps and structs to create a set.
>
> Unlike some programming languages, Go does not have any convenience functions to list out the keys or values of a map.

Today was a grind; would've been a few lines if I could do it in Python or TS. I did find [golang-set](https://github.com/deckarep/golang-set), but wanted to power through using the Go Standard Library which is apparently "batteries included". Not sure what batteries they are talking about; definitely not AA or AAA.

Aside: there is apparently a [Go port of lodash](https://github.com/samber/lo).

### [Day 4: Camp Cleanup](https://adventofcode.com/2022/day/4)

Another grindy day. Brute forced it instead of checking bounds. I'm mostly fighting my lack of knowledge of Go. Hopefully will have some time in the next few days to read through [The Go Programming Language](https://www.gopl.io/) book.

### [Day 5: Supply Stacks](https://adventofcode.com/2022/day/5)

Today was Towers of Hanoi more or less. I gave up on only using the Go Standard Library and installed the fantastic [deque](https://pkg.go.dev/github.com/gammazero/deque@v0.2.1) library.

Reading input was not a lot of fun, but am learning about a lot of ways to make things easier to process in Go.

### [Day 6: Tuning Trouble](https://adventofcode.com/2022/day/6)

First time I didn't fight Golang to get the solution done. But it was a very easy problem which used all of the knowledge I accquired from previous puzzles.

Also it was very easy to modify part 1 to solve part 2.

### [Day 7: No Space Left On Device](https://adventofcode.com/2022/day/7)

I used ChatGPT to help me parse the input into a tree and to create a print function that takes my tree and prints it out nicely. Learned more feature of Go this way than by actually reading a book (which has been hard to do on vacation). The GPT generated code wasn't perfect, but it helped me get started.

Finally starting to feel comfortable in Go. Not struggling as much as I was for the first few days. I'm still not 100% sure on pointers and the `&` vs `*` operators, but I think that will come in through time.

### [Day 8: Treetop Tree House](https://adventofcode.com/2022/day/8)

I brute forced today's challenge using a mapping. Could probably clean it up with 2D arrays and direction vectors to reduce the code, but it's probably not worth it.

Definitely need to look at other people's Go solutions to ensure I'm doing things in "The Go Way."

### [Day 9: Rope Bridge](https://adventofcode.com/2022/day/9)

I finally broke down and started writing methods for my `strut`s. This was another method which required (x, y) coordinates so I created a utility module for `Point` operations.

Some day I need to understand how imaginary numbers make this a lot easier to handle.

### [Day 10: Cathode-Ray Tube](https://adventofcode.com/2022/day/10)

Today's question was hard to parse, but the actual solution fairly straight forward. First day I felt like my solution is not that bad for Go -- a language I started learning at the end of November.

### [Day 11: Monkey in the Middle](https://adventofcode.com/2022/day/11)

Reading this in with Go was painful. I should have looked at the input because I went down the path of installing [maja42/goval](github.com/maja42/goval) to handle the operation. The `new = old * old` totally threw me for a loop.

Part 2 took forever. I tried out `big.Int`, but it wasn't the right solution. Found a hint on Slack / Reddit that helped me get the answer. I always get caught by LCM-type questions.

Aside: [this solution](https://github.com/mnml/aoc/blob/main/2022/11/1.go) has a really clean way of parsing input

### [Day 12: Hill Climbing Algorithm](https://adventofcode.com/2022/day/12)

This was a "shortest path" problem that took me a bit longer than normal to code up. I was just treating it as a find a path to X vs find the shortest path to X. My idea in part 1 was to work backwards, but I didn't code it that way until part 2 which required it.

### Day 13

Stashing -- will come back to

### [Day 14: Regolith Reservoir](https://adventofcode.com/2022/day/14)

Today was a fairly straight forward puzzle. After struggling with Day 13; I decided to skip it and come back to it later when I could read it with a fresh set of eyes.

It was nice to have a easy puzzle today which could be simulated very quickly in Go. Not sure if this puzzle required a trick or not.

### [Day 15: Beacon Exclusion Zone](https://adventofcode.com/2022/day/15)

Fun puzzle! For part 1, I tired to count the instances where y=limit. Solution ran pretty fast. Brute forcing part 1 for part 2 did not seem like it would work today. I was stuck for a few hours until I saw a Reddit animation with a diamond-shaped bounding box.

That gave me an idea for an algorithm. Find all the boundary points for each of the signals + manhattan distance to closest beacon + 1. Then filter out the points that don't work. This gave me the correct result in ~30-35 seconds (on average). Not perfect, but it does the job.

TODO -- look up other people's solutions for this one

### Day 16

Go has python style capture groups which is pretty awesome!

- https://dev.to/dandyvica/go-regular-expressions-53dn
- https://stackoverflow.com/a/39635221/4326704

Spent a lot of time on this one but still can't get the example to work for more than 1 agent. Will come back to it with Python when I have some time.
