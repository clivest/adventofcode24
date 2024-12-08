from typing import TextIO

import pytest

from aoc24.solutions.p7 import p7a


@pytest.fixture
def day() -> int:
    return 7


def test_p7a_real_input(real_input: TextIO) -> None:
    assert p7a(real_input) == 1430271835320


# @pytest.mark.skip
# def test_p6b_real_input(real_input: TextIO) -> None:
#     # Takes ~15s. Skipped for now to streamline tests
#     assert p6b(real_input) == 1618
