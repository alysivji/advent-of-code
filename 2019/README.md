# Advent of Code 2019

[AoC 2019](https://adventofcode.com/2019)

## Instructions

### Run

```console
$ ipython
%run 2019/day01_fuel.py
```

## Test

```console
pytest 2019/day01_fuel.py
```

## Daily Impressions

### [Day 1: The Tyranny of the Rocket Equation](https://adventofcode.com/2019/day/1)

First part was built for Python so it wasn't too difficult.

I tried to take a shortcut on the 2nd part by calculating on the fuel required for fuel and turns out that wasn't right. Did it the right way and got another answer, but the website said it wasn't right. Tried another person's solution, got the same answer as what I submitted. Tried submitting one more time, and it worked. 🤷

Hopefully I have better luck copying and pasting going forward...

### [Day 2: 1202 Program Alarm](https://adventofcode.com/2019/day/2)

Fairly straightforward. Thinking about converting the `IntCode` computer function into a class as we will reuse.... will do that later.

### [Day 3: Crossed Wires](https://adventofcode.com/2019/day/4)

Solved this challenge with dictionaries, but changed it to sets once I saw I could do it a bit more simply. Then part 2 required a dictionary... oh well.

### [Day 4: Secure Container](https://adventofcode.com/2019/day/4)

Not really proud of the code, but this challenge was grindy so I don't really mind too much. Did have some fun using `zip` to do math with adjacent indices.

### [Day 5: Sunny with a Chance of Asteroids](https://adventofcode.com/2019/day/5)

As they hinted at, `IntCodeComputer` was being reused so before starting the problem, I refactored my solution to change my implementation from a function to a class. This allowed me to replicate my conditional logic with objects versus `if` statements.

Once that was done, adding new OP codes and tests was a breeze. This way of doing things makes it a lot easier to debug.

A bit overkill? Probably. But then again... I am the guy who thinks that [if statements are a code smell](http://bit.ly/code-smell-if-statements).

### [Day 6: Universal Orbit Map](https://adventofcode.com/2019/day/6)

I stumbled into using trees with path calcutions. Had to backtrack and re-learn about graphs and path finding.

Python `dict` make graph data structures a breeze.

### [Day 7: Amplification Circuit](https://adventofcode.com/2019/day/7)

Day 7 was super grindy and process heavy. I had to add a couple of variables to my `IntCodeComputer` class to get things working for today's challenge.

First solution was hacking together a series of 5 `IntCodeComptuer`. It did the job, but when we started having to feed outputs in a loop, this was not the right way of doing things. By adding an instance variable that breaks when an output is generate, we can get the `IntCodeComputer` to function in a way that can solve the problem.

I used a generator to create inputs given outputs from the previous step. TIL: you can modify instance methods and generators will output terms given the updated value.

### [Day 8: Space Image Format](https://adventofcode.com/2019/day/8)

Day 8 was a nice change from all the `IntCodeCalcualtor` challenges. Even though Day 7 was straight-forward, it took me a while. Then again... I am also doing it at 2am while eating Taco Bell.

### [Day 9: Sensor Boost](https://adventofcode.com/2019/day/9)

After a couple of weeks off, I'm picking this back up. Took some time to remember how the `IntCodeComputer` works. This wasn't too difficult once I remembered some details of work from 2-3 weeks back. Luckily the code isn't TOO TOO messy. I think there are a few more puzzles coming up that will use the `IntCodeComputer`. Might clean it up before the next set of challenges.
