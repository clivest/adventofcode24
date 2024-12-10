from itertools import combinations
from typing import TextIO, Iterable

from aoc24.helpers.grid import iter_grid, Offset, Position, position_diff, move_position
from aoc24.helpers.main import run_solution


Antennas = dict[str, list[Position]]


def is_valid(n: Position, grid_size: Offset) -> bool:
    return 0 <= n.i < grid_size.i and 0 <= n.j < grid_size.j


def load_antennas(f: TextIO) -> tuple[Antennas, Offset]:
    antennas: dict[str, list[Position]] = {}
    grid_size = Offset(0, 0)
    for pos, c in iter_grid(f):
        if c != ".":
            antennas.setdefault(c, []).append(pos)
        grid_size = Offset(max(grid_size.i, pos.i), max(grid_size.j, pos.j))
    return antennas, grid_size + Offset(1, 1)


def walk(pos: Position, step: Offset, grid_size: Offset) -> Iterable[Position]:
    while is_valid(pos, grid_size):
        yield pos
        pos = move_position(pos, step)


def p8a(f: TextIO) -> int:
    antennas, grid_size = load_antennas(f)
    nodes: set[Position] = set()
    for ants in antennas.values():
        for a1, a2 in combinations(ants, 2):
            diff = position_diff(a1, a2)
            nodes.add(move_position(a2, diff))
            nodes.add(move_position(a1, -diff))
    nodes = {n for n in nodes if is_valid(n, grid_size)}
    return len(nodes)


def p8b(f: TextIO) -> int:
    antennas, grid_size = load_antennas(f)
    nodes: set[Position] = set()
    for ants in antennas.values():
        for a1, a2 in combinations(ants, 2):
            diff = position_diff(a1, a2)
            nodes |= set(walk(a2, diff, grid_size))
            nodes |= set(walk(a1, -diff, grid_size))
    return len(nodes)


if __name__ == "__main__":
    run_solution(p8a, p8b, 8)
