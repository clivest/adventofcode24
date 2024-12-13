from typing import TextIO

from aoc24.helpers.grid import Position, Offset, move_position
from aoc24.helpers.main import run_solution


Grid = list[list[int]]


directions = [Offset(0, 1), Offset(0, -1), Offset(1, 0), Offset(-1, 0)]


def get_height(input: Grid, pos: Position) -> int | None:
    if not (0 <= pos.i < len(input)) or not (0 <= pos.j < len(input[0])):
        # Out of bounds
        return None
    return input[pos.i][pos.j]


def score(head: Position, grid: Grid) -> set[Position]:
    height = get_height(grid, head)
    assert height is not None
    if height == 9:
        return {head}
    tops = set()
    for d in directions:
        pos = move_position(head, d)
        if (h := get_height(grid, pos)) is not None and h == height + 1:
            tops |= score(pos, grid)
    return tops


def p10a(f: TextIO) -> int:
    grid: Grid = []
    trail_heads: list[Position] = []
    for i, l in enumerate(f):
        grid.append([])
        for j, c in enumerate(l.strip()):
            grid[-1].append(int(c))
            if c == "0":
                trail_heads.append(Position(i, j))
    scores = 0
    for head in trail_heads:
        scores += len(score(head, grid))
    print(scores)
    return scores


def p10b(f: TextIO) -> int:
    return 1


if __name__ == "__main__":
    run_solution(p10a, p10b, 10)
