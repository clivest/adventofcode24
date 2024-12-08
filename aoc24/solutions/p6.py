from itertools import cycle
from typing import TextIO


from aoc24.helpers.grid import iter_grid, Offset, move_position
from aoc24.helpers.main import run_solution


directions = [
    Offset(-1, 0),
    Offset(0, 1),
    Offset(1, 0),
    Offset(0, -1),
]


def p6a(f: TextIO) -> int:
    # TODO: there's a much better way of solving this. Store obstacles mapping i -> sorted(js) and j -> sorted(is)
    #  then bisect the lists to find the next nearest obstacle
    start = None
    obstacles = set()
    grid_size = Offset(0, 0)
    for pos, c in iter_grid(f):
        match c:
            case "^":
                assert not start
                start = pos
            case "#":
                obstacles.add(pos)
        grid_size = Offset(max(grid_size.i, pos.i), max(grid_size.j, pos.j))
    assert start
    direction_iter = iter(cycle(directions))
    direction = next(direction_iter)
    pos = start
    visited = {start}
    while True:
        new_pos = move_position(pos, direction)
        if new_pos in obstacles:
            direction = next(direction_iter)
        elif 0 <= new_pos.i < grid_size.i and 0 <= new_pos.j < grid_size.j:
            pos = new_pos
            visited.add(pos)
        else:
            break
    return len(visited)


def p6b(f: TextIO) -> int:
    return 1


if __name__ == "__main__":
    run_solution(p6a, p6b, 6)
