from itertools import product
from typing import TextIO

from aoc24.helpers.grid import iter_grid, Position, Offset, move_position
from aoc24.helpers.main import run_solution


directions = [Offset(1, 0), Offset(0, 1), Offset(-1, 0), Offset(0, -1)]
vert_directions = [Offset(1, 0), Offset(-1, 0)]
horiz_directions = [Offset(0, 1), Offset(0, -1)]


def load_plots(f: TextIO) -> dict[str, set[Position]]:
    # Map plant to set of locations
    plots: dict[str, set[Position]] = {}
    for pos, c in iter_grid(f):
        plots.setdefault(c, set()).add(pos)
    return plots


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


def group_into_regions(plots: dict[str, set[Position]]) -> list[set[Position]]:
    regions = []
    while plots:
        _, positions = plots.popitem()
        while positions:
            region = find_region(positions.pop(), positions)
            positions -= region
            regions.append(region)
    return regions


def calc_perimeter(region: set[Position]) -> int:
    # Each square contributes 4 - (num neighbour) sides to the perimeter
    perm = 0
    for p in region:
        for d in directions:
            neigh = move_position(p, d)
            perm += neigh not in region
    return perm


def is_neighbour_in_region(p: Position, d: Offset, region: set[Position]) -> bool:
    return move_position(p, d) in region


def num_sides(region: set[Position]) -> int:
    corners = 0
    for p in region:
        for vh in product(vert_directions, horiz_directions):
            is_neigh_in_region = [is_neighbour_in_region(p, n, region) for n in vh]
            # Convex. Double counts cases where to convex corners occur at the same point intentionally
            corners += not any(is_neigh_in_region)
            # Concave corners
            corners += all(is_neigh_in_region) and not is_neighbour_in_region(
                p, vh[0] + vh[1], region
            )
    # Number of corners equals number of edges for a 2d shape
    return corners


def p12a(f: TextIO) -> int:
    plots = load_plots(f)
    regions = group_into_regions(plots)
    total = sum(len(region) * calc_perimeter(region) for region in regions)
    return total


def p12b(f: TextIO) -> int:
    plots = load_plots(f)
    regions = group_into_regions(plots)
    total = sum(len(region) * num_sides(region) for region in regions)
    return total


if __name__ == "__main__":
    run_solution(p12a, p12b, 12)
