import pytest
from utils import IntCodeComputer


def test_update_relative_base():
    relative_base = 2000
    instructions="109,19"

    cpu = IntCodeComputer(program=instructions)
