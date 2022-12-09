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
