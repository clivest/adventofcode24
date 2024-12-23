from typing import TextIO

import pytest

from aoc24.solutions.p20 import p20a, p20b


@pytest.fixture
def day() -> int:
    return 20


def test_p20a_real_input(real_input: TextIO) -> None:
    assert p20a(real_input) == 1360


def test_p20b_real_input(real_input: TextIO) -> None:
    assert p20b(real_input) == 1
