from typing import TextIO

import pytest

from aoc24.solutions.p5 import p5a, p5b


@pytest.fixture
def day() -> int:
    return 5


def test_p5a_real_input(real_input: TextIO) -> None:
    assert p5a(real_input) == 4609


def test_p5b_real_input(real_input: TextIO) -> None:
    assert p5b(real_input) == 5723
