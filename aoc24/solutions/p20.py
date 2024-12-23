from typing import TextIO

from aoc24.helpers.grid import iter_grid, Position, Offset, move_position, vh_directions
from aoc24.helpers.main import run_solution
from aoc24.helpers.min_path import determine_min_path


def p20a(f: TextIO) -> int:
    start = None
    end = None
    grid_size = Offset(0, 0)
    walls: set[Position] = set()
    for p, c in iter_grid(f):
        match c:
            case "#":
                walls.add(p)
            case "E":
                assert not end
                end = p
            case "S":
                assert not start
                start = p
        grid_size = Offset(max(p.i + 1, grid_size.i), max(p.j + 1, grid_size.j))
    assert start and end and walls
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
