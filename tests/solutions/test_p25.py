from typing import TextIO

import pytest

from aoc24.solutions.p25 import p25b, p25a


@pytest.fixture
def day() -> int:
    return 25


def test_p25a_real_input(real_input: TextIO) -> None:
    assert p25a(real_input) == 3466


def test_p25b_real_input(real_input: TextIO) -> None:
    assert p25b(real_input) == 1
