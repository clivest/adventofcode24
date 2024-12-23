from typing import TextIO

from aoc24.helpers.grid import (
    Position,
    Offset,
    load_grid,
    position_diff,
)
from aoc24.helpers.main import run_solution
from aoc24.helpers.min_path import determine_min_path


def load_input(f: TextIO) -> tuple[Position, Position, set[Position], Offset]:
    d, grid_size = load_grid(f)
    assert len(d["E"]) == 1 and len(d["S"]) == 1
    return d["S"].pop(), d["E"].pop(), d["#"], grid_size


def find_cheats(
    min_path: list[Position], max_cheat_len: int
) -> dict[tuple[Position, Position], int]:
    cheats: dict[tuple[Position, Position], int] = {}
    for i, p in enumerate(min_path):
        for j, other in enumerate(min_path[i + 1 :]):
            other_i = j + i + 1
            offset = position_diff(p, other)
            distance = abs(offset.i) + abs(offset.j)
            if distance > max_cheat_len:
                continue
            if (cheat_len := other_i - i - distance) > 0:
                cheats[(p, other)] = cheat_len
    return cheats


def p20a(f: TextIO) -> int:
    start, end, walls, grid_size = load_input(f)
    min_path = determine_min_path(start, end, walls, grid_size)
    cheats = find_cheats(min_path, 2)
    return sum(c >= 100 for c in cheats.values())


def p20b(f: TextIO) -> int:
    start, end, walls, grid_size = load_input(f)
    min_path = determine_min_path(start, end, walls, grid_size)
    cheats = find_cheats(min_path, 20)
    return sum(c >= 100 for c in cheats.values())


if __name__ == "__main__":
    run_solution(p20a, p20b, 20)
