import itertools
from dataclasses import dataclass
from typing import TextIO

from aoc24.helpers.main import run_solution


@dataclass
class Coord:
    i: int
    j: int


@dataclass
class Offset:
    i: int
    j: int


Grid = list[str]


directions = [
    Offset(*d) for d in itertools.product([0, 1, -1], repeat=2) if d != (0, 0)
]


def get_character(input: Grid, pos: Coord) -> str | None:
    if not (0 <= pos.i < len(input)) or not (0 <= pos.j < len(input[0])):
        return None
    return input[pos.i][pos.j]


def add_coord(pos: Coord, offset: Offset) -> Coord:
    return Coord(pos.i + offset.i, pos.j + offset.j)


def find_xmas(input: list[str], x: Coord, direction: Offset) -> bool:
    assert get_character(input, x) == "X"
    pos = x
    for c in "MAS":
        pos = add_coord(pos, direction)
        if get_character(input, pos) != c:
            return False
    return True


def p4a(f: TextIO) -> int:
    input = f.read().split()
    count = 0
    for i in range(len(input)):
        for j in range(len(input[i])):
            pos = Coord(i, j)
            if get_character(input, pos) == "X":
                for direction in directions:
                    count += find_xmas(input, pos, direction)
    return count


# def p4b(f: TextIO) -> int:
#     input = f.read()
#     index = 0
#     total = 0
#     enabled = True
#     while True:
#         do_dont = seek_do_dont(input, index)
#         if enabled:
#             # if enabled, find mul instructions between current index and the next do/dont instruction, if there is one,
#             # else end of the input
#             while mul := seek_mul(input, index, do_dont[1] if do_dont else None):
#                 total += mul[0]
#                 index = mul[1]
#         if do_dont is None:
#             break
#         # scan from the next do/dont instruction
#         enabled, index = do_dont
#     return total


if __name__ == "__main__":
    run_solution(p4a, None, 4)
