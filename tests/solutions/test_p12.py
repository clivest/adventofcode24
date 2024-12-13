from typing import TextIO

import pytest

from aoc24.solutions.p12 import p12a, p12b


@pytest.fixture
def day() -> int:
    return 12


def test_p12a_real_input(real_input: TextIO) -> None:
    assert p12a(real_input) == 1421958


def test_p12b_real_input(real_input: TextIO) -> None:
    assert p12b(real_input) == 1
