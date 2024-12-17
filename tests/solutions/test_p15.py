from typing import TextIO

import pytest

from aoc24.solutions.p15 import p15a, p15b


@pytest.fixture
def day() -> int:
    return 15


def test_p14a_real_input(real_input: TextIO) -> None:
    assert p15a(real_input) == 1371036


def test_p15b_real_input(real_input: TextIO) -> None:
    assert p15b(real_input) == 1392847
