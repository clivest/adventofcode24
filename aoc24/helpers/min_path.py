import heapq
from dataclasses import dataclass

from aoc24.helpers.grid import Position, Offset, move_position, vh_directions


class NoPathFoundError(Exception):
    pass


@dataclass
class HeapItem:
    pos: Position
    cost: int
    path: list[Position]

    def __lt__(self, other):
        if isinstance(other, HeapItem):
            return self.cost < other.cost
        return NotImplemented


def determine_min_path(
    start: Position, end: Position, obstacles: set[Position], grid_size: Offset
) -> list[Position]:
    """
    Finds min path from start to end (both inclusive). Assumes valid moves are up down left right (no diagonals)
    :param start: start position
    :param end: end position
    :param obstacles: locations which cannot be passed through
    :param grid_size: size of the grid
    :return: the min path
    """
    # TODO also refactor p16.py which has a djikstra algorithm
    searched: set[Position] = set()
    paths: list[HeapItem] = [HeapItem(start, 0, [])]
    while True:
        if not paths:
            raise NoPathFoundError
        path = heapq.heappop(paths)
        if path.pos in searched:
            continue
        if path.pos == end:
            return path.path + [end]
        for d in vh_directions:
            pos = move_position(path.pos, d)
            if (
                pos not in obstacles
                and 0 <= pos.i < grid_size.i
                and 0 <= pos.j < grid_size.j
            ):
                heapq.heappush(
                    paths, HeapItem(pos, path.cost + 1, path.path + [path.pos])
                )
        searched.add(path.pos)
