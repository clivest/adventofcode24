from typing import TextIO, Generator
from aoc24.helpers.input import input_file

import pytest


@pytest.fixture
def real_input(day: int) -> Generator[TextIO, None, None]:
    with open(input_file(day), "r") as f:
        yield f
