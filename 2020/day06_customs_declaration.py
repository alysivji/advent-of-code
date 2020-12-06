from collections import Counter

TEST_INPUT = """abc

a
b
c

ab
ac

a
a
a
a

b"""

group_answers = [group.split("\n") for group in TEST_INPUT.strip().split("\n\n")]


def sum_answers_that_were_yes(answers_by_group):
    yes_answers = 0
    for answers in answers_by_group:
        counts = Counter()
        for individual_answers in answers:
            for question in individual_answers:
                counts[question] += 1

        yes_answers += len(counts.keys())

    return yes_answers


def sum_answers_that_were_yes_across_the_group(answers_by_group):
    yes_answers = 0
    for answers in answers_by_group:
        counts = Counter()
        for individual_answers in answers:
            for question in individual_answers:
                counts[question] += 1

        for question, count in counts.items():
            if count == len(answers):
                yes_answers += 1

    return yes_answers


assert sum_answers_that_were_yes_across_the_group(group_answers) == 6


if __name__ == "__main__":
    with open("2020/data/day06_input.txt") as f:
        group_answers = [group.split("\n") for group in f.read().strip().split("\n\n")]

    result = sum_answers_that_were_yes(group_answers)
    print(f"Result for part 1 is {result}")

    result = sum_answers_that_were_yes_across_the_group(group_answers)
    print(f"Result for part 22is {result}")
