import heapq
from dataclasses import dataclass
from typing import TextIO

from aoc24.helpers.grid import iter_grid, Position, Offset, move_position
from aoc24.helpers.main import run_solution


@dataclass
class HeapItem:
    pos: Position
    cost: int
    path: list[Position]

    def __lt__(self, other):
        if isinstance(other, HeapItem):
            return self.cost < other.cost
        return NotImplemented


directions = [Offset(0, 1), Offset(1, 0), Offset(-1, 0), Offset(0, -1)]


def determine_min_path(
    start: Position, end: Position, obstacles: set[Position], grid_size: Offset
) -> list[Position]:
    # p16.py also has a djikstra algorithm. TODO: refactor out a common implementation!
    searched: set[Position] = set()
    paths: list[HeapItem] = [HeapItem(start, 0, [])]
    while True:
        path = heapq.heappop(paths)
        if path.pos in searched:
            continue
        if path.pos == end:
            return path.path + [end]
        for d in directions:
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


def p20a(f: TextIO) -> int:
    start = None
    end = None
    grid_size = Offset(0, 0)
    walls: set[Position] = set()
    for p, c in iter_grid(f):
        match c:
            case "#":
                walls.add(p)
            case "E":
                assert not end
                end = p
            case "S":
                assert not start
                start = p
        grid_size = Offset(max(p.i + 1, grid_size.i), max(p.j + 1, grid_size.j))
    assert start and end and walls
    min_path = determine_min_path(start, end, walls, grid_size)
    cheats: dict[tuple[Position, Position], int] = {}
    path_elems = {p: i for i, p in enumerate(min_path)}
    for i, p in enumerate(min_path):
        for d in directions:
            new_p = move_position(p, d)
            new_p = move_position(new_p, d)
            if (cheat_len := path_elems.get(new_p, 0) - i - 2) > 0:
                cheats[(p, new_p)] = cheat_len
    cheat_gte_100 = sum(c >= 100 for c in cheats.values())
    print(cheat_gte_100)
    return cheat_gte_100


def p20b(f: TextIO) -> int:
    return 1


if __name__ == "__main__":
    run_solution(p20a, p20b, 20)
