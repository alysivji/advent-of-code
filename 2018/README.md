# Advent of Code 2018

[AoC 2018](https://adventofcode.com/2018)

## [Day 1](https://adventofcode.com/2018/day/1)

This one was fairly straight forward. Right now it's about getting back into the flow. Start developing some tooling to make easier to perform repetitive actions.

## [Day 2](https://adventofcode.com/2018/day/2)

My first pass thru this was messy as I used generators, but I cleaned it up by adding another for loop with a break. This improved runtime:

```console
In [9]: %timeit find_prototype_box_common_letters(boxes)
82.5 ms ± 1.19 ms per loop (mean ± std. dev. of 7 runs, 10 loops each)

In [10]: %timeit find_prototype_box_single_pass(boxes)
19.9 ms ± 191 µs per loop (mean ± std. dev. of 7 runs, 10 loops each)
```
