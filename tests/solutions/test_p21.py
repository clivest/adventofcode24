from typing import TextIO

import pytest

from aoc24.solutions.p21 import p21b, p21a


@pytest.fixture
def day() -> int:
    return 21


def test_p21a_real_input(real_input: TextIO) -> None:
    assert p21a(real_input) == 164960


def test_p21b_real_input(real_input: TextIO) -> None:
    assert p21b(real_input) == 205620604017764
