import pytest
from utils import IntCodeComputer


def test_update_relative_base():
    relative_base = 2000
    instructions="109,19"

    cpu = IntCodeComputer(program=instructions, relative_base=relative_base)

    try:
        cpu.process()
    except Exception:
        assert cpu.relative_base == 2019
        relative_base = cpu.relative_base
