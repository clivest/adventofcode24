from typing import TextIO, Iterable

from aoc24.helpers.grid import iter_grid, Offset, move_position, get_character, Position
from aoc24.helpers.main import run_solution


def rotations(move: Offset) -> Iterable[Offset]:
    for ij in (1, -1):
        yield Offset(ij if move.i == 0 else 0, ij if move.j == 0 else 0)


def p16a(f: TextIO) -> int:
    grid = [l.strip() for l in f]
    start = None
    end = None
    for pos, c in iter_grid(grid):
        if c == "S":
            assert start is None
            start = pos
        elif c == "E":
            assert end is None
            end = pos
        if start and end:
            break
    assert start and end
    costs = {(start, Offset(0, 1)): 0}
    searched: set[tuple[Position, Offset]] = set()
    min_path_cost = None
    while True:
        to_search_pos, move = min(costs.keys() - searched, key=lambda c: costs[c])
        cost = costs[(to_search_pos, move)]
        if to_search_pos == end:
            min_path_cost = cost
            break
        new_pos = move_position(to_search_pos, move)
        new_costs = {}
        if get_character(grid, new_pos) in [".", "E"]:
            new_costs[(new_pos, move)] = cost + 1
        for new_move in rotations(move):
            new_costs[(to_search_pos, new_move)] = cost + 1000
        costs.update(
            {
                k: min(costs[k], new_cost) if k in costs else new_cost
                for k, new_cost in new_costs.items()
            }
        )
        searched.add((to_search_pos, move))
    assert min_path_cost
    print(min_path_cost)
    return min_path_cost


def p16b(f: TextIO) -> int:
    return 1


if __name__ == "__main__":
    run_solution(p16a, p16b, 16)
