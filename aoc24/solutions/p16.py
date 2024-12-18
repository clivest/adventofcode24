from dataclasses import dataclass
from functools import total_ordering
from heapq import heappush, heappop
from typing import TextIO, Iterable

from aoc24.helpers.grid import (
    iter_grid,
    Offset,
    move_position,
    get_character,
    Position,
    Grid,
)
from aoc24.helpers.main import run_solution


@dataclass
@total_ordering
class HeapItem:
    cost: int
    position: Position
    move: Offset

    def __lt__(self, other):
        if isinstance(other, HeapItem):
            return self.cost < other.cost
        return NotImplemented

    @property
    def pos_move(self) -> tuple[Position, Offset]:
        return self.position, self.move


directions = [Offset(0, 1), Offset(0, -1), Offset(1, 0), Offset(-1, 0)]


def rotations(move: Offset) -> Iterable[Offset]:
    # 90 degree rotation each way
    for ij in (1, -1):
        yield Offset(ij if move.i == 0 else 0, ij if move.j == 0 else 0)


def possible_moves(start: HeapItem, grid: Grid) -> Iterable[HeapItem]:
    # Possibilities: forwards 1 or rotation 90 degrees each way
    new_pos = move_position(start.position, start.move)
    if get_character(grid, new_pos) in [".", "E"]:
        yield HeapItem(start.cost + 1, new_pos, start.move)
    for new_move in rotations(start.move):
        yield HeapItem(start.cost + 1000, start.position, new_move)


def find_char(grid: Grid, search: str) -> Position:
    for pos, c in iter_grid(grid):
        if c == search:
            return pos
    assert False, f"No {search} found"


def p16a(f: TextIO) -> int:
    grid = [l.strip() for l in f]
    start = find_char(grid, "S")
    costs_heap = [HeapItem(0, start, Offset(0, 1))]
    searched: set[tuple[Position, Offset]] = set()
    while True:
        current_state: HeapItem = heappop(costs_heap)
        if current_state.pos_move in searched:
            # the heap may include states that we've already searched. Skip until we find a (position, move) state we've
            # not yet searched
            continue
        if get_character(grid, current_state.position) == "E":
            return current_state.cost
        for new_state in possible_moves(current_state, grid):
            heappush(costs_heap, new_state)
        searched.add(current_state.pos_move)


def print_grid_min_path(grid: Grid, min_path_elems: set[Position]) -> None:
    for i, l in enumerate(grid):
        nl = ""
        for j, c in enumerate(l):
            if c in "#SE":
                nl = nl + c
            elif Position(i, j) in min_path_elems:
                nl = nl + "O"
            else:
                nl = nl + "."
        print(nl)


def p16b(f: TextIO) -> int:
    grid = [l.strip() for l in f]
    start = find_char(grid, "S")
    end = find_char(grid, "E")
    costs_heap = [HeapItem(0, start, Offset(0, 1))]
    searched: set[tuple[Position, Offset]] = set()
    paths: dict[tuple[Position, Offset], tuple[int, set[Position]]] = {
        (start, Offset(0, 1)): (0, set())
    }
    end_cost = None

    def track_path(new_state: HeapItem, from_: tuple[Position, Offset]) -> None:
        # track the new possible path
        key = new_state.pos_move
        if key not in paths or paths[key][0] > new_state.cost:
            paths[key] = (new_state.cost, paths[from_][1] | {from_[0]})
        elif paths[key][0] == new_state.cost:
            paths[key][1].update(paths[from_][1] | {from_[0]})

        heappush(costs_heap, new_state)

    while True:
        current_state: HeapItem = heappop(costs_heap)
        if current_state.pos_move in searched:
            # the heap may include states that we've already searched. Skip until we find a (position, move) state we've
            # not yet searched
            continue
        if end_cost and current_state.cost > end_cost:
            break
        if current_state.position == end:
            end_cost = current_state.cost
        for new_state in possible_moves(current_state, grid):
            track_path(new_state, current_state.pos_move)
        searched.add(current_state.pos_move)

    path_elems = {p for d in directions for p in paths.get((end, d), (None, set()))[1]}
    print_grid_min_path(grid, path_elems)
    return len(path_elems)


if __name__ == "__main__":
    run_solution(p16a, p16b, 16)
