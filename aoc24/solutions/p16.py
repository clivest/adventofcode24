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


def find_char(grid: Grid, search: str) -> Position:
    for pos, c in iter_grid(grid):
        if c == search:
            return pos
    assert False, "No start found"


def p16a(f: TextIO) -> int:
    grid = [l.strip() for l in f]
    start = find_char(grid, "S")
    costs_heap = [HeapItem(0, start, Offset(0, 1))]
    searched: set[tuple[Position, Offset]] = set()
    while True:
        while True:
            # the heap may include states that we've already searched. Skip until we find a (position, move) state we've
            # not yet searched
            current_state: HeapItem = heappop(costs_heap)
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
    grid = [l.strip() for l in f]
    start = find_char(grid, "S")
    end = find_char(grid, "E")
    costs_heap = [HeapItem(0, start, Offset(0, 1))]
    searched: set[tuple[Position, Offset]] = set()
    paths: dict[tuple[Position, Offset], tuple[int, set[Position]]] = {
        (start, Offset(0, 1)): (0, set())
    }
    end_cost = None

    def update_paths(
        position: Position, dir: Offset, cost: int, from_: tuple[Position, Offset]
    ) -> None:
        key = position, dir
        if key not in paths:
            paths[key] = (cost, paths[from_][1] | {from_[0]})
        elif paths[key][0] == cost:
            paths[key][1].update(paths[from_][1] | {from_[0]})
        elif paths[key][0] > cost:
            paths[key] = (cost, paths[from_][1] | {from_[0]})

    while True:
        while True:
            # the heap may include states that we've already searched. Skip until we find a (position, move) state we've
            # not yet searched
            current_state: HeapItem = heappop(costs_heap)
            # if current_state.position == move_position(end, Offset(6, 0)):
            #     print(current_state.cost, paths.get(current_state.position))
            if current_state.pos_move not in searched:
                break
            assert paths[current_state.pos_move][0] <= current_state.cost
        if end_cost and current_state.cost > end_cost:
            path_elems = {
                p
                for d in [Offset(1, 0), Offset(0, 1), Offset(0, -1), Offset(-1, 0)]
                for p in paths.get((end, d), (None, []))[1]
            }
            for i, l in enumerate(grid):
                nl = ""
                for j, c in enumerate(l):
                    if c in "#SE":
                        nl = nl + c
                    elif Position(i, j) in path_elems:
                        nl = nl + "O"
                    else:
                        nl = nl + "."
                print(nl)
            print(len(path_elems))
            return len(path_elems)
        if current_state.position == end:
            end_cost = current_state.cost
        new_pos = move_position(current_state.position, current_state.move)
        if get_character(grid, new_pos) in [".", "E"]:
            heappush(
                costs_heap,
                HeapItem(current_state.cost + 1, new_pos, current_state.move),
            )
            update_paths(
                new_pos,
                current_state.move,
                current_state.cost + 1,
                current_state.pos_move,
            )
        for new_move in rotations(current_state.move):
            heappush(
                costs_heap,
                HeapItem(current_state.cost + 1000, current_state.position, new_move),
            )
            update_paths(
                current_state.position,
                new_move,
                current_state.cost + 1000,
                current_state.pos_move,
            )
        searched.add(current_state.pos_move)


if __name__ == "__main__":
    run_solution(p16a, p16b, 16)
