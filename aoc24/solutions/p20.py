from typing import TextIO

from aoc24.helpers.grid import (
    Position,
    Offset,
    move_position,
    vh_directions,
    load_grid,
)
from aoc24.helpers.main import run_solution
from aoc24.helpers.min_path import determine_min_path


def load_input(f: TextIO) -> tuple[Position, Position, set[Position], Offset]:
    d, grid_size = load_grid(f)
    assert len(d["E"]) == 1 and len(d["S"]) == 1
    return d["S"].pop(), d["E"].pop(), d["#"], grid_size


def p20a(f: TextIO) -> int:
    start, end, walls, grid_size = load_input(f)
    min_path = determine_min_path(start, end, walls, grid_size)
    cheats: dict[tuple[Position, Position], int] = {}
    path_elems = {p: i for i, p in enumerate(min_path)}
    for i, p in enumerate(min_path):
        for d in vh_directions:
            new_p = move_position(p, d)
            new_p = move_position(new_p, d)
            if (cheat_len := path_elems.get(new_p, 0) - i - 2) > 0:
                cheats[(p, new_p)] = cheat_len
    return sum(c >= 100 for c in cheats.values())


def p20b(f: TextIO) -> int:
    return 1


if __name__ == "__main__":
    run_solution(p20a, p20b, 20)
