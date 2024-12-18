from typing import TextIO

import pytest

from aoc24.solutions.p16 import p16a, p16b


@pytest.fixture
def day() -> int:
    return 16


def test_p16a_real_input(real_input: TextIO) -> None:
    assert p16a(real_input) == 99460


def test_p16b_real_input(real_input: TextIO) -> None:
    assert p16b(real_input) == 500
