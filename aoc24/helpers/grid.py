from dataclasses import dataclass
from typing import Generator, TextIO, Callable


@dataclass(frozen=True)
class Position:
    i: int
    j: int


@dataclass(frozen=True)
class Offset:
    i: int
    j: int

    def magnitude(self) -> float:
        return (self.i**2 + self.j**2) ** 0.5

    def __add__(self, other) -> "Offset":
        if isinstance(other, Offset):
            return Offset(self.i + other.i, self.j + other.j)
        return NotImplemented

    def __neg__(self) -> "Offset":
        return Offset(-self.i, -self.j)

    def __mul__(self, other) -> "Offset":
        if isinstance(other, int):
            return Offset(self.i * other, self.j * other)
        return NotImplemented


vh_directions = [Offset(0, 1), Offset(1, 0), Offset(-1, 0), Offset(0, -1)]


Grid = list[str]


def get_character(input: Grid, pos: Position) -> str | None:
    if not (0 <= pos.i < len(input)) or not (0 <= pos.j < len(input[0])):
        # Out of bounds
        return None
    return input[pos.i][pos.j]


def iter_grid(
    input: Grid | TextIO, *, stop: Callable[[str], bool] = lambda l: False
) -> Generator[tuple[Position, str], None, None]:
    for i, row in enumerate(input):
        if stop(row.strip()):
            return
        for j, c in enumerate(row.strip()):
            yield Position(i, j), c


def load_grid(
    input: Grid | TextIO, *, stop: Callable[[str], bool] = lambda l: False
) -> tuple[dict[str, set[Position]], Offset]:
    elems: dict[str, set[Position]] = {}
    grid_size = Offset(0, 0)
    for p, c in iter_grid(input, stop=stop):
        elems.setdefault(c, set()).add(p)
        grid_size = Offset(max(grid_size.i, p.i + 1), max(grid_size.j, p.j + 1))
    return elems, grid_size


def move_position(pos: Position, offset: Offset) -> Position:
    return Position(pos.i + offset.i, pos.j + offset.j)


def position_diff(a: Position, b: Position) -> Offset:
    return Offset(b.i - a.i, b.j - a.j)
