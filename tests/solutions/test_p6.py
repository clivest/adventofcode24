from typing import TextIO

import pytest

from aoc24.solutions.p6 import p6a


@pytest.fixture
def day() -> int:
    return 6


def test_p6a_real_input(real_input: TextIO) -> None:
    assert p6a(real_input) == 4778


# def test_p5b_real_input(real_input: TextIO) -> None:
#     assert p6b(real_input) == 5723
