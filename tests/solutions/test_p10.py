from typing import TextIO

import pytest

from aoc24.solutions.p10 import p10a, p10b


@pytest.fixture
def day() -> int:
    return 10


def test_p10a_real_input(real_input: TextIO) -> None:
    assert p10a(real_input) == 825


def test_p10b_real_input(real_input: TextIO) -> None:
    assert p10b(real_input) == 1805
