from typing import TextIO

import pytest

from aoc24.solutions.p14 import p14b, p14a


@pytest.fixture
def day() -> int:
    return 14


def test_p14a_real_input(real_input: TextIO) -> None:
    assert p14a(real_input) == 208437768


def test_p14b_real_input(real_input: TextIO) -> None:
    assert p14b(real_input) == 7492
