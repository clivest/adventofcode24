from typing import TextIO

import pytest

from aoc24.solutions.p8 import p8a, p8b


@pytest.fixture
def day() -> int:
    return 8


def test_p8a_real_input(real_input: TextIO) -> None:
    assert p8a(real_input) == 323


def test_p8b_real_input(real_input: TextIO) -> None:
    assert p8b(real_input) == 1077
