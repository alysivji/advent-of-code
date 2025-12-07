# Advent of Code 2025

Strengthening my TS skills by working my way through [Advent of Code 2025](https://adventofcode.com/2025).

#### Table of Contents

<!-- TOC -->

- [Installation Notes](#installation-notes)
- [Daily Impressions](#daily-impressions)
  - [Day 1: Secret Entrance](#day-1-secret-entrance)
  - [Day 2: Gift Shop](#day-2-gift-shop)
  - [Day 3: Lobby](#day-3-lobby)
  - [Day 4: Printing Department](#day-4-printing-department)
  - [Day 5: Cafeteria](#day-5-cafeteria)
  - [Day 6: Trash Compactor](#day-6-trash-compactor)
- [Todo](#todo)

<!-- /TOC -->

## Installation Notes

Node.js has [TypeScript support](https://nodejs.org/api/typescript.html#full-typescript-support)! We can now use `tsx` vs `ts-node` to run scripts: `npx tsx file.ts`.

Downside is that `tsx` doesn't support type checking ([more info](https://betterstack.com/community/guides/scaling-nodejs/tsx-explained/)), but my IDE does so that should be good enough. Can always switch to stricter type checker later.

## Daily Impressions

### [Day 1: Secret Entrance](https://adventofcode.com/2025/day/1)

Part 1 was fairly straight forward. Part 2, I got accidently. My edge cases weren't well defined, but it somehow produced the right number. After I got it done, I fixed the edge cases properly.

### [Day 2: Gift Shop](https://adventofcode.com/2025/day/2)

Part 2 took a while as I created a array chunker from scratch. In Part 1, I used an array to keep track of the productIds -- but in part 2, productIds were in the array twice so I had to use a set. The runtime is slightly slow at `719.746ms` but I think this is good enough.

Tomorrow will take a look at other solutions.

### [Day 3: Lobby](https://adventofcode.com/2025/day/3)

Generalized my part 1 solution for part 2. First time this year. Took some time to complete part 2 because I forgot that `Array.sort()` is a in-place operation.

Not really a big fan of debugging with `tsx`. Don't really like `ts-node` either. Thinking about switching to [bun](https://bun.com/) -- probably a good use of time now that [Anthropic bought Bun](https://bun.com/blog/bun-joins-anthropic). Better to do it now and only have to modify a few things.

### [Day 4: Printing Department](https://adventofcode.com/2025/day/4)

Normally I write out the GridMap data structure, but today I decided to use the one I wrote out last year.

Not happy with my part 2, feels like it could have been cleaner or used my part 1.

Spent time dealing with Xfinity issues so had to use my hotspot. This also means I didn't have time to switch over to Bun.

### [Day 5: Cafeteria](https://adventofcode.com/2025/day/5)

Finished part 1 fairly quickly the night the challenge came out. My algorithm for part 2 tried to find overlapping intervals using two for loops, but that wasn't working. Got a hint from ChatGPT that sorting the intervals would help out and would only require a single loop. That did it!

Had another hint about using [Interval Trees](https://en.wikipedia.org/wiki/Interval_tree), but feels like a bit more work than I actually want to put in.

Sorting to simplify problems by only looping once is definitely another trick I need to put in my toolbox.

### [Day 6: Trash Compactor](https://adventofcode.com/2025/day/6)

This was an easy problem. Did it while watching the College Football Conference Championships so not really fully paying attention.

First time this year I've had to modify my input parsing for part 2.

## Todo

- [ ] fix import errors in IDE for node imports
- [ ] migrate to Bun
- [ ] solve day 2 with RegEx
