from typing import TextIO

from aoc24.helpers.grid import Position, Offset
from aoc24.helpers.main import run_solution
from aoc24.helpers.min_path import determine_min_path, NoPathFoundError


def solve_memory_path(corrupt: list[Position]) -> set[Position]:
    path = determine_min_path(
        Position(0, 0), Position(70, 70), set(corrupt), Offset(71, 71)
    )
    return set(path)


def read_corrupt_positions(f: TextIO) -> list[Position]:
    corrupt = []
    for l in f:
        xy = l.strip().split(",")
        corrupt.append(Position(int(xy[1]), int(xy[0])))
    return corrupt


def p18a(f: TextIO) -> int:
    corrupt = read_corrupt_positions(f)
    min_path = solve_memory_path(corrupt[:1024])
    return len(min_path) - 1


def p18b(f: TextIO, skip: int = 1024) -> str:
    corrupt = read_corrupt_positions(f)
    min_path = solve_memory_path(corrupt[:skip])
    for i, c in enumerate(corrupt[skip:]):
        if c not in min_path:
            continue
        # else C would block current min path. Find a new min path
        try:
            min_path = solve_memory_path(
                corrupt[: skip + i + 1],
            )
        except NoPathFoundError:
            return f"{c.j},{c.i}"
    assert False, "No answer found"


if __name__ == "__main__":
    run_solution(p18a, p18b, 18)
