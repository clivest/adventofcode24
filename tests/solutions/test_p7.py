from typing import TextIO

import pytest

from aoc24.solutions.p7 import p7a, p7b


@pytest.fixture
def day() -> int:
    return 7


def test_p7a_real_input(real_input: TextIO) -> None:
    assert p7a(real_input) == 1430271835320


def test_p7b_real_input(real_input: TextIO) -> None:
    assert p7b(real_input) == 456565678667482
