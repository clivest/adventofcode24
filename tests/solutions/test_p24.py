from typing import TextIO

import pytest

from aoc24.solutions.p24 import p24b, p24a


@pytest.fixture
def day() -> int:
    return 24


def test_p24a_real_input(real_input: TextIO) -> None:
    assert p24a(real_input) == 56620966442854


def test_p24b_real_input(real_input: TextIO) -> None:
    assert p24b(real_input) == "chv,jpj,kgj,rts,vvw,z07,z12,z26"
