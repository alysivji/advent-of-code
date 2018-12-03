# Advent of Code 2018

[AoC 2018](https://adventofcode.com/2018)

## [Day 1: Chronal Calibration](https://adventofcode.com/2018/day/1)

This one was fairly straight forward. Right now it's about getting back into the flow. Start developing some tooling to make easier to perform repetitive actions.

## [Day 2: Inventory Management System](https://adventofcode.com/2018/day/2)

My first pass thru this was messy as I used generators, but I cleaned it up by adding another for loop with a break. This improved runtime:

TIL: Change `continue` to `break`

```console
In [9]: %timeit find_prototype_box_common_letters(boxes)
82.5 ms ± 1.19 ms per loop (mean ± std. dev. of 7 runs, 10 loops each)

In [10]: %timeit find_prototype_box_single_pass(boxes)
19.9 ms ± 191 µs per loop (mean ± std. dev. of 7 runs, 10 loops each)
```

## [Day 3: No Matter How You Slice It](https://adventofcode.com/2018/day/3)

Got it done before starting work. As always, had to refer to the [Regular Expression HOWTO](https://docs.python.org/3/howto/regex.html) and [regexr](https://regexr.com) to hammer something out.

TIL how to pull numbers with a quick regex ([h/t thread on /r/adventofcode](https://www.reddit.com/r/adventofcode/comments/a2lesz/2018_day_3_solutions/eazev7m/))

Since everything we are processing is a number and in the same order, we can use `re.findall` to pull all numbers and create a Claim object.

```python
def load_input_improved(lines: List[str]) -> List[Claim]:
    claims = [Claim(*map(int, re.findall(r"-?\d+", line))) for line in lines]
    return claims
```

## [Day 4: ](https://adventofcode.com/2018/day/4)

[text]

TIL [text]
