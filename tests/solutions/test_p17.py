from io import StringIO
from typing import TextIO

import pytest

from aoc24.solutions.p17 import Registers, run_program, p17a


@pytest.fixture
def day() -> int:
    return 17


sample_input = """
Register A: 729
Register B: 0
Register C: 0

Program: 0,1,5,4,3,0"""


@pytest.mark.parametrize(
    "program, registers, expected_registers, expected_output",
    [
        ("2,6", {"C": 9}, {"B": 1}, ""),
        ("5,0,5,1,5,4", {"A": 10}, {}, "0,1,2"),
        ("0,1,5,4,3,0", {"A": 2024}, {"A": 0}, "4,2,5,6,7,7,7,7,3,1,0"),
        ("1,7", {"B": 29}, {"B": 26}, ""),
        ("4,0", {"B": 2024, "C": 43690}, {"B": 44354}, ""),
    ],
)
def test_p17a_examples(
    program: str,
    registers: Registers,
    expected_registers: Registers,
    expected_output: str,
) -> None:
    output = run_program(registers, program)
    assert ",".join(map(str, output)) == expected_output
    for r, expected_value in expected_registers.items():
        assert registers[r] == expected_value


def test_p17a_sample_input() -> None:
    input = StringIO(sample_input.strip())
    assert p17a(input) == "4,6,3,5,6,3,5,2,1,0"


def test_p17b_real_input(real_input: TextIO) -> None:
    assert p17a(real_input) == "3,5,0,1,5,1,5,1,0"
