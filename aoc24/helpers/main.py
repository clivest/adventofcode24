from typing import TextIO, Callable, Any

from aoc24.helpers.input import input_file

Solution = Callable[[TextIO], Any]


def run_solution(pa: Solution, pb: Solution | None, day: int) -> None:
    # This is the pattern I use to run the tests i1.txt is input for day 1 i2.txt is input for day 2 etc
    with open(input_file(day), "r") as f:
        pa(f)
        if pb:
            f.seek(0)
            pb(f)
