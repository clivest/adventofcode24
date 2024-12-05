import itertools
from dataclasses import dataclass
from typing import TextIO, Generator

from aoc24.helpers.main import run_solution


@dataclass(frozen=True)
class Position:
    i: int
    j: int


@dataclass
class Offset:
    i: int
    j: int


Grid = list[str]


def get_character(input: Grid, pos: Position) -> str | None:
    if not (0 <= pos.i < len(input)) or not (0 <= pos.j < len(input[0])):
        # Out of bounds
        return None
    return input[pos.i][pos.j]


def iter_grid(input: Grid) -> Generator[tuple[Position, str], None, None]:
    for i, row in enumerate(input):
        for j, c in enumerate(row):
            yield Position(i, j), c


def move_position(pos: Position, offset: Offset) -> Position:
    return Position(pos.i + offset.i, pos.j + offset.j)


def find_xmas(input: list[str], x: Position, direction: Offset) -> bool:
    # x is the position of an X. Walk in direction and see if MAS are found
    assert get_character(input, x) == "X"
    pos = x
    for c in "MAS":
        pos = move_position(pos, direction)
        if get_character(input, pos) != c:
            return False
    return True


def same_row_or_col(a: Position, b: Position) -> bool:
    return a.i == b.i or a.j == b.j


def p4a(f: TextIO) -> int:
    directions = [
        Offset(*d) for d in itertools.product([0, 1, -1], repeat=2) if d != (0, 0)
    ]

    input = f.read().split()
    count = 0
    for pos, c in iter_grid(input):
        if c != "X":
            continue
        for direction in directions:
            count += find_xmas(input, pos, direction)
    return count


def p4b(f: TextIO) -> int:
    diagonals = [Offset(*d) for d in itertools.product([1, -1], repeat=2)]

    input = f.read().split()
    # find MAS coordinates
    positions: dict[str, set[Position]] = {c: set() for c in "MAS"}
    for pos, c in iter_grid(input):
        if c in positions:
            positions[c].add(pos)

    count = 0
    for a in positions["A"]:
        surrounds = {move_position(a, d) for d in diagonals}
        count += (
            # diagonal adjacencies must be MMSS
            all(len(surrounds & positions[c]) == 2 for c in "MS")
            # The Ms (or Ss) must be in the same row or col
            and same_row_or_col(*(surrounds & positions["M"]))
        )
    return count


if __name__ == "__main__":
    run_solution(p4a, p4b, 4)
