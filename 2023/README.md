# Advent of Code 2023

Learning Dart by working my way through [Advent of Code 2023](https://adventofcode.com/2013).

#### Table of Contents

<!-- TOC -->

- [Daily Impressions](#daily-impressions)
  - [Day 1: Trebuchet?!](#day-1-trebuchet)
  - [Day 2: Cube Conundrum](#day-2-cube-conundrum)
  - [Day 3: Gear Ratios](#day-3-gear-ratios)
  - [Day 4: Scratchcards](#day-4-scratchcards)
  - [Day 5: If You Give A Seed A Fertilizer](#day-5-if-you-give-a-seed-a-fertilizer)
  - [Day 6: Wait For It](#day-6-wait-for-it)
  - [Day 7: Camel Cards](#day-7-camel-cards)

<!-- /TOC -->

## Daily Impressions

### [Day 1: Trebuchet?!](https://adventofcode.com/2013/day/1)

While the company I work for uses Dart / Flutter, it's not something I do on a regular basis as I'm a backend developer. I spent some time before this job practicing [Dart with Advent of Code](../2016/) and used that code to help me get this done.

I definitely hacked together a solution to get things out the door. Totally okay with it for now, its good to get re-familiar with types.

### [Day 2: Cube Conundrum](https://adventofcode.com/2023/day/2)

This was more about reading the data into a data structure I could work with easily. Think I did a pretty good job as the second part flowed easily from my part 1.

### [Day 3: Gear Ratios](https://adventofcode.com/2023/day/3)

Used an object-oriented approach to set up the problem and then used a functional style approach to solve each of the methods. There were some edges that I didn't think about, but after a while I realized I had to track clusters separately since the part numbers repeat.

Found a great article that showed me how to [overload operators in Dart](https://medium.com/pinch-nl/comparing-objects-in-dart-made-easy-with-equatable-d208e5eb9571).

### [Day 4: Scratchcards](https://adventofcode.com/2023/day/4)

Today was easy. Feels like I'm going back to a lot of the OOP principles that I'm comfortable with in Dart. I should start looking at other people's solutions to make sure I'm doing things in a way that makes sense.

### [Day 5: If You Give A Seed A Fertilizer](https://adventofcode.com/2023/day/5)

I skipped this day initially since it sounded confusing when I read it at midnight. Came back to it on Day 10 -- part 1 was simple, but part 2 required a trick. Took some time to think through intersections of ranges (after getting a hint from the Chicago Python Slack). I feel like I re-write the same code every year as there is a problem like this every single year.

### [Day 6: Wait For It](https://adventofcode.com/2023/day/6)

I brute-forced this one. Focused a lot more on writing functional Dart than I did thinking of a smart way to solve the problem, i.e. solving quadratic functions. Definitely learned a bit more about how to work in Dart which is good since I need to get a PR into our Flutter repo in the next few days.

### [Day 7: Camel Cards](https://adventofcode.com/2023/day/7)

ChatGPT was helpful in learning about more Dart features like Comparable and `asMap`.

This was a fairly easy puzzle. I'm sure I could have done it in a much better way, but I'm fairly happy with how readable my code is. Dart is a fun language to work with.

TIL:
- [Comparable interface](https://api.dart.dev/stable/3.2.3/dart-core/Comparable-class.html)
- `asMap` returns a MapEntry element has a `key` and a `value` attribute
