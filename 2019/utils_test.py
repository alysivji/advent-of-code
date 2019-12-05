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
