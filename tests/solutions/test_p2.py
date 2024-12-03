from typing import TextIO

import pytest

from aoc24.solutions.p2 import p2a, p2b


@pytest.fixture
def day() -> int:
    return 2


def test_p2a_real_input(real_input: TextIO) -> None:
    assert p2a(real_input) == 326


def test_p2b_real_input(real_input: TextIO) -> None:
    assert p2b(real_input) == 381
