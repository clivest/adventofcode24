from typing import TextIO

import pytest

from aoc24.solutions.p18 import p18a


@pytest.fixture
def day() -> int:
    return 18


def test_p18a_real_input(real_input: TextIO) -> None:
    assert p18a(real_input) == 438
