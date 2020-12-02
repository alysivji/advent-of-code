from collections import Counter
import re
from typing import List, NamedTuple


PASSWORD_PATTERN = r"(?P<num1>\d+)-(?P<num2>\d+) (?P<letter>[a-z]): (?P<password>[a-z]+)"


class Password(NamedTuple):
    num1: int
    num2: int
    letter: str
    password: str


def load_input(lines: List[str]) -> List[Password]:
    p = re.compile(PASSWORD_PATTERN)

    passwords = []
    for line in lines:
        cleaned_line = line.strip()
        m = p.match(cleaned_line)

        password = Password(
            num1=int(m.group("num1")),
            num2=int(m.group("num2")),
            letter=m.group("letter"),
            password=m.group("password"),
        )
        passwords.append(password)
    return passwords


def find_valid_password__old_policy(passwords: List[Password]) -> List[Password]:
    """
    - num1 is min times letter appears
    - num2 is max times letter appears

    valid if letter appears between num1 and num2
    """
    valid_passwords = []
    for password in passwords:
        counter = Counter(password.password)
        if password.num1 <= counter[password.letter] <= password.num2:
            valid_passwords.append(password)
    return valid_passwords


def test_valid_passwords__old_policy():
    TEST_INPUT="""1-3 a: abcde
    1-3 b: cdefg
    2-9 c: ccccccccc""".split("\n")

    passwords = load_input(TEST_INPUT)
    valid_passwords = find_valid_password__old_policy(passwords)
    assert len(valid_passwords) == 2


def find_valid_password__new_policy(passwords: List[Password]) -> List[Password]:
    """
    - num1 is 1-index position letter appears
    - num2 is 1-index position letter apperas

    valid if letter is in either num1 or num2 position
    """
    valid_passwords = []
    for password in passwords:
        first_position = password.password[password.num1 - 1]
        second_position = password.password[password.num2 - 1]
        if first_position == second_position == password.letter:
            continue

        if first_position == password.letter or second_position == password.letter:
            valid_passwords.append(password)
    return valid_passwords


def test_find_valid_password__new_policy():
    TEST_INPUT="""1-3 a: abcde
    1-3 b: cdefg
    2-9 c: ccccccccc""".split("\n")

    passwords = load_input(TEST_INPUT)
    valid_passwords = find_valid_password__new_policy(passwords)
    assert len(valid_passwords) == 1



if __name__ == "__main__":
    with open("2020/data/day02_input.txt") as f:
        passwords = load_input(f.readlines())

    valid_passwords = find_valid_password__old_policy(passwords)
    print(f"Part 1 answer is {len(valid_passwords)}")

    valid_passwords = find_valid_password__new_policy(passwords)
    print(f"Part 2 answer is {len(valid_passwords)}")
