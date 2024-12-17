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


def rotations(move: Offset) -> Iterable[Offset]:
    for ij in (1, -1):
        yield Offset(ij if move.i == 0 else 0, ij if move.j == 0 else 0)


def find_start(grid: Grid) -> Position:
    for pos, c in iter_grid(grid):
        if c == "S":
            return pos
    assert False, "No start found"


def p16a(f: TextIO) -> int:
    grid = [l.strip() for l in f]
    start = find_start(grid)
    costs_heap = [HeapItem(0, start, Offset(0, 1))]
    searched: set[tuple[Position, Offset]] = set()
    while True:
        while True:
            current_state = heappop(costs_heap)
            if current_state.pos_move not in searched:
                break
        if get_character(grid, current_state.position) == "E":
            return current_state.cost
        new_pos = move_position(current_state.position, current_state.move)
        if get_character(grid, new_pos) in [".", "E"]:
            heappush(
                costs_heap,
                HeapItem(current_state.cost + 1, new_pos, current_state.move),
            )
        for new_move in rotations(current_state.move):
            heappush(
                costs_heap,
                HeapItem(current_state.cost + 1000, current_state.position, new_move),
            )
        searched.add(current_state.pos_move)


def p16b(f: TextIO) -> int:
    return 1


if __name__ == "__main__":
    run_solution(p16a, p16b, 16)
