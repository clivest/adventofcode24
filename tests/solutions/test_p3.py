from typing import TextIO

import pytest

from aoc24.solutions.p3 import p3a


@pytest.fixture
def day() -> int:
    return 3


def test_p3a_real_input(real_input: TextIO) -> None:
    assert p3a(real_input) == 188741603


# def test_p2b_real_input(real_input: TextIO) -> None:
#     assert p2b(real_input) == 381
