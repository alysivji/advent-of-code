# Advent of Code 2025

Strengthening my TS skills by working my way through [Advent of Code 2025](https://adventofcode.com/2025).

#### Table of Contents

<!-- TOC -->

- [Installation Notes](#installation-notes)
- [Daily Impressions](#daily-impressions)
  - [Day 1: Secret Entrance](#day-1-secret-entrance)
  - [Day 2: Gift Shop](#day-2-gift-shop)
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

## Todo

- [ ] fix import errors in IDE for node imports
