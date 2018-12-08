TEST_INPUT = "dabAcCaCBAcCcaDA"

# ascii difference between large and small is
ASCII_DIFFERENCE = abs(ord("A") - ord("a"))


def reaction(polymer: str) -> int:
    reduced_polymer = polymer
    start_loc = 0
    while True:
        for i, j in zip(reduced_polymer[start_loc:], reduced_polymer[start_loc + 1:]):
            if abs(ord(i) - ord(j)) == ASCII_DIFFERENCE:
                loc = reduced_polymer.find(i + j)
                reduced_polymer = reduced_polymer[:loc] + reduced_polymer[loc + 2:]
                start_loc = loc - 1 if loc >= 1 else 0
                break
        else:
            break
    return len(reduced_polymer)


assert reaction(TEST_INPUT) == 10


def remove_unit_reaction(polymer: str) -> int:
    min_length = float("inf")
    for ascii_char in range(ord("A"), ord("Z") + 1):
        ucase = chr(ascii_char)
        lcase = chr(ascii_char + ASCII_DIFFERENCE)
        reduced_polymer = polymer.replace(ucase, "").replace(lcase, "")
        reduced_length = reaction(reduced_polymer)

        if reduced_length < min_length:
            min_length = reduced_length
    return min_length


assert remove_unit_reaction(TEST_INPUT) == 4


if __name__ == "__main__":
    with open("day05_input.txt", "r") as f:
        line = f.readline().split("\n")[0]
    print(reaction(line))
    print(remove_unit_reaction(line))
