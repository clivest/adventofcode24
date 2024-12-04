from typing import TextIO

import pytest

from aoc24.solutions.p3 import p3a, p3b


@pytest.fixture
def day() -> int:
    return 3


def test_p3a_real_input(real_input: TextIO) -> None:
    assert p3a(real_input) == 188741603


def test_p3b_real_input(real_input: TextIO) -> None:
    assert p3b(real_input) == 67269798
