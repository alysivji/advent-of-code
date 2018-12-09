# Advent of Code 2018

[AoC 2018](https://adventofcode.com/2018)

## [Day 1: Chronal Calibration](https://adventofcode.com/2018/day/1)

This one was fairly straight forward. Right now it's about getting back into the flow. Start developing some tooling to make easier to perform repetitive actions.

## [Day 2: Inventory Management System](https://adventofcode.com/2018/day/2)

My first pass thru this was messy as I used generators, but I cleaned it up by adding another for loop with a break. This improved runtime:

TIL: Change `continue` to `break`

TODO: [`difflib`](https://docs.python.org/3.7/library/difflib.html)

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

## [Day 4: Repose Record](https://adventofcode.com/2018/day/4)

Just got a PS4 with Red Dead and FIFA so I started Day 4 just before Day 5 came out. This was a very messy solution. I'm sure I could've done it with a better data structure. I used a default dict and appended each sleep record to that.

TODO: Use a more optimized data structure. Instead of having a list for each sleep, have a combined list per guard.

## [Day 5: Alchemical Reduction](https://adventofcode.com/2018/day/5)

Finally a problem where we have to be conscious not not using a naive solution! My solution to part 1 wasn't the most efficient, but it got the job done. It definitely did not work out for part 2. The input string I got required me to think of an edge case as the number was coming in way too high.

Achievement unlocked: did not import a single Python library. Straight up built-ins.

```console
In [3]: %timeit remove_unit_reaction(line)
4.06 s ± 67.2 ms per loop (mean ± std. dev. of 7 runs, 1 loop each)
```

TODO: `string.ascii_lowercase`

## [Day 6: Chronal Coordinates](https://adventofcode.com/2018/day/6)

I brute forced it by working through the problem exactly as described. I'm sure there is a smarter way of doing it, but it worked.

## Day 7

Got part 1 using a PriorityQueue. I may have gone a bit over the top for my part 2 solution as I tried to think of a generalized way of concurrently running workers in a task queue. I have a deliverable at work in the coming week which will require me to formalize how I split up and send jobs to Airflow. Thinking through this problem in a bit more depth will hopefully help me explain it in a clearer way.

TIL: [`PriorityQueue`](https://docs.python.org/3/library/queue.html#queue.PriorityQueue)

I previousy used [`heapq`](https://docs.python.org/3/library/heapq.html) and found that interface hard to use. Even wrote a [class-based wrapper](https://github.com/alysivji/sivtools/blob/master/sivtools/data_structures/priority_queue.py) around it for [`sivtools`](https://github.com/alysivji/sivtools). Of course, there is something in the standard library that does the same thing, but a lot better. Really like the `max_size` parameter.

Shoutout to Dan Bader for his [Priority Queues in Python article](https://dbader.org/blog/priority-queues-in-python) for helping me along.

## Day 8

I tried a bunch of ways to do it, realized that recursion makes the most sense. Need to sit down and give this another shot.

TIL: Always forget how array slicing works and have to try it in the REPL. In Python it's closed on the left, open on the right.

## [Day 9: Marble Mania](https://adventofcode.com/2018/day/9)

I misread the problem so I spent a lot of time debugging my code that was correct. Once I took a peek at Reddit, I realized that `last marble is worth 1618 points` means 1618 total marbles, not that placing the marble scores 1618 points.

Part 1 ran without a hitch. Part 2 is taking a while to run, this is because I'm inserting / popping from the middle of a list which is an O(n) operation in Python. The strategy I should have employed is to use a [`deque`](https://docs.python.org/3/library/collections.html#collections.deque) and rotate so that we are always inserting / popping off from the ends [i.e. O(1)], which I did when I rewrote my code for part 2.
