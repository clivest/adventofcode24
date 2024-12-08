from dataclasses import dataclass
from typing import Generator, TextIO


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


def iter_grid(input: Grid | TextIO) -> Generator[tuple[Position, str], None, None]:
    for i, row in enumerate(input):
        for j, c in enumerate(row.strip()):
            yield Position(i, j), c


def move_position(pos: Position, offset: Offset) -> Position:
    return Position(pos.i + offset.i, pos.j + offset.j)
