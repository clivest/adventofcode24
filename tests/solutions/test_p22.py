from typing import TextIO

import pytest

from aoc24.solutions.p22 import p22b, p22a


@pytest.fixture
def day() -> int:
    return 22


def test_p22a_real_input(real_input: TextIO) -> None:
    assert p22a(real_input) == 16953639210


def test_p22b_real_input(real_input: TextIO) -> None:
    assert p22b(real_input) == 1863
