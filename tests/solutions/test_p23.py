from typing import TextIO

import pytest

from aoc24.solutions.p23 import p23a, p23b


@pytest.fixture
def day() -> int:
    return 23


def test_p22a_real_input(real_input: TextIO) -> None:
    assert p23a(real_input) == 926


def test_p22b_real_input(real_input: TextIO) -> None:
    assert p23b(real_input) == "az,ed,hz,it,ld,nh,pc,td,ty,ux,wc,yg,zz"
