from typing import TextIO

from aoc24.helpers.grid import iter_grid, Position, Offset, move_position
from aoc24.helpers.main import run_solution


directions = [Offset(1, 0), Offset(0, 1), Offset(-1, 0), Offset(0, -1)]


def p12a(f: TextIO) -> int:
    plots: dict[str, set[Position]] = {}
    for pos, c in iter_grid(f):
        plots.setdefault(c, set()).add(pos)
    regions = []
    while plots:
        _, positions = plots.popitem()
        while positions:
            pos = positions.pop()
            region = {pos}
            to_explore = {pos}
            while to_explore:
                p = to_explore.pop()
                for d in directions:
                    neigh = move_position(p, d)
                    if neigh in positions:
                        positions.discard(neigh)
                        region.add(neigh)
                        to_explore.add(neigh)
            regions.append(region)
    total = 0
    for region in regions:
        area = len(region)
        perm = 0
        for p in region:
            for d in directions:
                neigh = move_position(p, d)
                perm += neigh not in region
        total += area * perm
    print(total)
    return total


def p12b(f: TextIO) -> int:
    return 1


if __name__ == "__main__":
    run_solution(p12a, p12b, 12)
