from typing import TextIO

from aoc24.helpers.grid import iter_grid, Position, Offset, move_position
from aoc24.helpers.main import run_solution


directions = [Offset(1, 0), Offset(0, 1), Offset(-1, 0), Offset(0, -1)]


def find_region(start: Position, plots: set[Position]) -> set[Position]:
    # Find neighbours and their neighbours etc to form a region.
    pos = start
    region = {pos}
    to_explore = {pos}
    while to_explore:
        p = to_explore.pop()
        for d in directions:
            neigh = move_position(p, d)
            if neigh in plots and neigh not in region:
                region.add(neigh)
                to_explore.add(neigh)
    return region


def calc_perimeter(region: set[Position]) -> int:
    # Each square contributes 4 - (num neighbour) sides to the perimeter
    perm = 0
    for p in region:
        for d in directions:
            neigh = move_position(p, d)
            perm += neigh not in region
    return perm


def p12a(f: TextIO) -> int:
    # Map plant to set of locations
    plots: dict[str, set[Position]] = {}
    for pos, c in iter_grid(f):
        plots.setdefault(c, set()).add(pos)
    regions = []
    while plots:
        _, positions = plots.popitem()
        while positions:
            region = find_region(positions.pop(), positions)
            positions -= region
            regions.append(region)
    total = sum(len(region) * calc_perimeter(region) for region in regions)
    return total


def p12b(f: TextIO) -> int:
    return 1


if __name__ == "__main__":
    run_solution(p12a, p12b, 12)
