from typing import TextIO

import pytest

from aoc24.solutions.p9 import p9b, p9a


@pytest.fixture
def day() -> int:
    return 9


def test_p9a_real_input(real_input: TextIO) -> None:
    assert p9a(real_input) == 6519155389266


def test_p8b_real_input(real_input: TextIO) -> None:
    assert p9b(real_input) == 1
