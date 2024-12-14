from typing import TextIO

import pytest

from aoc24.solutions.p13 import p13a, p13b


@pytest.fixture
def day() -> int:
    return 13


def test_p13a_real_input(real_input: TextIO) -> None:
    assert p13a(real_input) == 29388


def test_p13b_real_input(real_input: TextIO) -> None:
    assert p13b(real_input) == 99548032866004
