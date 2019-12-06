import pytest
from utils import IntCodeComputer


@pytest.mark.parametrize(
    "incode_program, expected_output",
    [
        ("1,9,10,3,2,3,11,0,99,30,40,50", "3500,9,10,70,2,3,11,0,99,30,40,50"),
        ("1,0,0,0,99", "2,0,0,0,99"),
        ("2,3,0,3,99", "2,3,0,6,99"),
        ("2,4,4,5,99,0", "2,4,4,5,99,9801"),
        ("1,1,1,4,99,5,6,0,99", "30,1,1,4,2,5,6,0,99"),
        ("1002,4,3,4,33", "1002,4,3,4,99"),
        ("1101,100,-1,4,0", "1101,100,-1,4,99"),
    ],
)
def test_process_intcode_program(incode_program, expected_output):
    cpu = IntCodeComputer(incode_program)
    cpu.process()
    assert str(cpu) == expected_output


def test_simple_input_output_program():
    intcode_program = "3,0,4,0,99"
    cpu = IntCodeComputer(intcode_program, input_value=1)
    cpu.process()
    assert cpu.captured_output[0] == 1


@pytest.mark.parametrize("input_value, expected_output", [(7, 0), (8, 1), (9, 0)])
def test_input_equal_to_8__position_mode(input_value, expected_output):
    intcode_program = "3,9,8,9,10,9,4,9,99,-1,8"
    cpu = IntCodeComputer(intcode_program, input_value=input_value)
    cpu.process()
    assert cpu.captured_output[0] == expected_output


@pytest.mark.parametrize("input_value, expected_output", [(7, 1), (8, 0), (9, 0)])
def test_input_less_than_8__position_mode(input_value, expected_output):
    intcode_program = "3,9,7,9,10,9,4,9,99,-1,8"
    cpu = IntCodeComputer(intcode_program, input_value=input_value)
    cpu.process()
    assert cpu.captured_output[0] == expected_output


@pytest.mark.parametrize("input_value, expected_output", [(7, 0), (8, 1), (9, 0)])
def test_input_equal_to_8__immediate_mode(input_value, expected_output):
    intcode_program = "3,3,1108,-1,8,3,4,3,99"
    cpu = IntCodeComputer(intcode_program, input_value=input_value)
    cpu.process()
    assert cpu.captured_output[0] == expected_output


@pytest.mark.parametrize("input_value, expected_output", [(7, 1), (8, 0), (9, 0)])
def test_input_less_than_8__immediate_mode(input_value, expected_output):
    intcode_program = "3,3,1107,-1,8,3,4,3,99"
    cpu = IntCodeComputer(intcode_program, input_value=input_value)
    cpu.process()
    assert cpu.captured_output[0] == expected_output


@pytest.mark.parametrize("input_value, expected_output", [(0, 0), (1, 1), (-1, 1)])
def test_jump__position_mode(input_value, expected_output):
    intcode_program = "3,12,6,12,15,1,13,14,13,4,13,99,-1,0,1,9"
    cpu = IntCodeComputer(intcode_program, input_value=input_value)
    cpu.process()
    assert cpu.captured_output[0] == expected_output


@pytest.mark.parametrize("input_value, expected_output", [(0, 0), (1, 1), (-1, 1)])
def test_jump__immediate_mode(input_value, expected_output):
    intcode_program = "3,3,1105,-1,9,1101,0,0,12,4,12,99,1"
    cpu = IntCodeComputer(intcode_program, input_value=input_value)
    cpu.process()
    assert cpu.captured_output[0] == expected_output


@pytest.mark.parametrize(
    "input_value, expected_output",
    [(6, 999), (7, 999), (8, 1000), (9, 1001), (9, 1001)],
)
def test_multiple_operations(input_value, expected_output):
    intcode_program = (
        "3,21,1008,21,8,20,1005,20,22,107,8,21,20,1006,20,31,"
        "1106,0,36,98,0,0,1002,21,125,20,4,20,1105,1,46,104,"
        "999,1105,1,46,1101,1000,1,20,4,20,1105,1,46,98,99"
    )
    cpu = IntCodeComputer(intcode_program, input_value=input_value)
    cpu.process()
    assert cpu.captured_output[0] == expected_output