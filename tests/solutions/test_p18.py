from typing import TextIO

import pytest

from aoc24.solutions.p18 import p18a, p18b


@pytest.fixture
def day() -> int:
    return 18


def test_p18a_real_input(real_input: TextIO) -> None:
    assert p18a(real_input) == 438


def test_p18b_real_input(real_input: TextIO) -> None:
    # Skip a bit to speed up unit test
    assert p18b(real_input, skip=2800) == "26,22"
