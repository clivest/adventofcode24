import heapq
from dataclasses import dataclass
from typing import TextIO

from aoc24.helpers.grid import Position, Offset, move_position
from aoc24.helpers.main import run_solution


@dataclass
class HeapItem:
    pos: Position
    cost: int

    def __lt__(self, other):
        if isinstance(other, HeapItem):
            return self.cost < other.cost
        return NotImplemented


directions = [Offset(0, 1), Offset(1, 0), Offset(-1, 0), Offset(0, -1)]


def min_path_len(
    start: Position, end: Position, obstacles: list[Position], grid_size: Offset
) -> int:
    searched: set[Position] = set()
    paths: list[HeapItem] = [HeapItem(start, 0)]
    while True:
        path = heapq.heappop(paths)
        if path.pos in searched:
            continue
        if path.pos == end:
            return path.cost
        for d in directions:
            pos = move_position(path.pos, d)
            if (
                pos not in obstacles
                and 0 <= pos.i < grid_size.i
                and 0 <= pos.j < grid_size.j
            ):
                heapq.heappush(paths, HeapItem(pos, path.cost + 1))
        searched.add(path.pos)


def p18a(f: TextIO) -> int:
    corrupt = []
    for l in f:
        xy = l.strip().split(",")
        corrupt.append(Position(int(xy[1]), int(xy[0])))
    corrupt = corrupt[:1024]
    start = Position(0, 0)
    end = Position(70, 70)
    grid_size = Offset(71, 71)
    return min_path_len(start, end, corrupt, grid_size)


def p18b(f: TextIO) -> int:
    return 1


if __name__ == "__main__":
    run_solution(p18a, p18b, 18)
