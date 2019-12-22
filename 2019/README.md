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

### [Day 10: Monitoring Station](https://adventofcode.com/2019/day/10)

Had to hack `_within_map_boundary()` to get the right answer. Not sure what's going on, but was able to hack things together to get the test case to pass. Had to review radians and degrees for part 2; used paper to figure out a formula and got things working.

Useful StackOverflow post: [Getting key of dict with maximum value](https://stackoverflow.com/questions/268272/getting-key-with-maximum-value-in-dictionary)

### [Day 11: Space Police](https://adventofcode.com/2019/day/11)

Another puzzle using the `IntCodeCalculator`. I added the ability to propagate exceptions up to allow higher order abstractions to control flow. Also allowed driver programs to control how much output to break on.

Thinking about refactoring `IntCodeCalculator` before the next go around. Also added a test file to ensure changes don't break existing functionality.

### [Day 12: The N-Body Problem](https://adventofcode.com/2019/day/12)

I wanted to practice my Python skills for this one. Fun with magic methods! I modified my simulate function to function as more of a driver. It takes a state, runs thru timesteps, returns the final stste back. This makes it more general and easier to use in other places.

I feel that part 2 is going to involve figuring out the pattern for each of the moons. I'm going to take a break with the next day's challenge before coming back to this.

### [Day 13: Care Package](https://adventofcode.com/2019/day/13)

All the work I did to make my `IntCodeCalculator` easy-to-use was work it as I was able to quickly complete Part 1.

Part 2 seems challenging, think the best plan of attack is to build a decision tree that has 3 inputs... keep track of score and/or how many blocks we broke.
