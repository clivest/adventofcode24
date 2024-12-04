from typing import TextIO

import pytest

from aoc24.solutions.p4 import p4a, p4b


@pytest.fixture
def day() -> int:
    return 4


def test_p4a_real_input(real_input: TextIO) -> None:
    assert p4a(real_input) == 2336


def test_p4b_real_input(real_input: TextIO) -> None:
    assert p4b(real_input) == 1831
