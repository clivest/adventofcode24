from typing import TextIO

import pytest

from aoc24.solutions.p1 import p1a, p1b


@pytest.fixture
def day() -> int:
    return 1


def test_p1a_real_input(real_input: TextIO) -> None:
    assert p1a(real_input) == 1223326


def test_p1b_real_input(real_input: TextIO) -> None:
    assert p1b(real_input) == 21070419
