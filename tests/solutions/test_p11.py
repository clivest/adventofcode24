from typing import TextIO

import pytest

from aoc24.solutions.p11 import p11a, p11b


@pytest.fixture
def day() -> int:
    return 11


def test_p11a_real_input(real_input: TextIO) -> None:
    assert p11a(real_input) == 200446


def test_p11b_real_input(real_input: TextIO) -> None:
    assert p11b(real_input) == 238317474993392
