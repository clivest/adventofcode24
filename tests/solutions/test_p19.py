from typing import TextIO

import pytest

from aoc24.solutions.p19 import p19a, p19b


@pytest.fixture
def day() -> int:
    return 19


def test_p19a_real_input(real_input: TextIO) -> None:
    assert p19a(real_input) == 280


def test_p19b_real_input(real_input: TextIO) -> None:
    assert p19b(real_input) == 1
