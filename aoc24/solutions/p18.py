import heapq
from dataclasses import dataclass
from typing import TextIO

from aoc24.helpers.grid import Position, Offset, move_position
from aoc24.helpers.main import run_solution


class NoPathFoundError(Exception):
    pass


@dataclass
class HeapItem:
    pos: Position
    cost: int
    path: set[Position]

    def __lt__(self, other):
        if isinstance(other, HeapItem):
            return self.cost < other.cost
        return NotImplemented


directions = [Offset(0, 1), Offset(1, 0), Offset(-1, 0), Offset(0, -1)]


def determine_min_path(
    start: Position, end: Position, obstacles: list[Position], grid_size: Offset
) -> set[Position]:
    # p16.py also has a djikstra algorithm. TODO: refactor out a common implementation!
    searched: set[Position] = set()
    paths: list[HeapItem] = [HeapItem(start, 0, set())]
    while True:
        if not paths:
            raise NoPathFoundError
        path = heapq.heappop(paths)
        if path.pos in searched:
            continue
        if path.pos == end:
            return path.path | {end}
        for d in directions:
            pos = move_position(path.pos, d)
            if (
                pos not in obstacles
                and 0 <= pos.i < grid_size.i
                and 0 <= pos.j < grid_size.j
            ):
                heapq.heappush(
                    paths, HeapItem(pos, path.cost + 1, path.path | {path.pos})
                )
        searched.add(path.pos)


def read_corrupt_positions(f: TextIO) -> list[Position]:
    corrupt = []
    for l in f:
        xy = l.strip().split(",")
        corrupt.append(Position(int(xy[1]), int(xy[0])))
    return corrupt


def p18a(f: TextIO) -> int:
    corrupt = read_corrupt_positions(f)
    min_path = determine_min_path(
        Position(0, 0), Position(70, 70), corrupt[:1024], Offset(71, 71)
    )
    return len(min_path) - 1


def p18b(f: TextIO, skip: int = 1024) -> str:
    corrupt = read_corrupt_positions(f)
    min_path = determine_min_path(
        Position(0, 0), Position(70, 70), corrupt[:skip], Offset(71, 71)
    )
    for i, c in enumerate(corrupt[skip:]):
        if c not in min_path:
            continue
        # else C would block current min path. Find a new min path
        try:
            min_path = determine_min_path(
                Position(0, 0),
                Position(70, 70),
                corrupt[: skip + i + 1],
                Offset(71, 71),
            )
        except NoPathFoundError:
            return f"{c.j},{c.i}"
    assert False, "No answer found"


if __name__ == "__main__":
    run_solution(p18a, p18b, 18)
