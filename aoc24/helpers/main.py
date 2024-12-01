from pathlib import Path
from typing import TextIO, Callable

Solution = Callable[[TextIO], None]


def run_solution(pa: Solution, pb: Solution | None, day: int) -> None:
    # This is the pattern I use to run the tests i1.txt is input for day 1 i2.txt is input for day 2 etc
    input = Path(__file__).parent.parent / "inputs" / f"i{day}.txt"
    with open(input, "r") as f:
        pa(f)
        if pb:
            f.seek(0)
            pb(f)
