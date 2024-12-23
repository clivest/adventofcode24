from typing import TextIO, Iterable

from aoc24.helpers.grid import Position
from aoc24.helpers.main import run_solution


Keypad = dict[str, Position]


def min_paths(code: str, pos: Position, keypad: Keypad, gap: Position) -> Iterable[str]:
    if not code:
        yield ""
        return
    for min_path in min_paths(code[1:], keypad[code[0]], keypad, gap):
        dest = keypad[code[0]]
        v = ("^" if dest.i < pos.i else "v") * abs(dest.i - pos.i)
        h = (">" if dest.j > pos.j else "<") * abs(dest.j - pos.j)
        if not (pos.j == gap.j and dest.i == gap.i):
            yield v + h + "A" + min_path
            if not v or not h:
                continue
        if not (pos.i == gap.i and dest.j == gap.j):
            yield h + v + "A" + min_path


def min_paths_r1(code: str) -> Iterable[str]:
    keypad = {str(i): Position((9 - i) // 3, (i - 7) % 3) for i in range(1, 10)} | {
        "0": Position(3, 1),
        "A": Position(3, 2),
    }
    return min_paths(code, keypad["A"], keypad, Position(3, 0))


def min_paths_rn(code: str) -> Iterable[str]:
    keypad = {
        "^": Position(0, 1),
        "A": Position(0, 2),
        "<": Position(1, 0),
        "v": Position(1, 1),
        ">": Position(1, 2),
    }
    return min_paths(code, keypad["A"], keypad, Position(0, 0))


def p21a(f: TextIO) -> int:
    complexity = 0
    for l in f:
        code = l.strip()
        min_path_len: int | None = None
        for p1 in min_paths_r1(code):
            for p2 in min_paths_rn(p1):
                for p3 in min_paths_rn(p2):
                    min_path_len = (
                        min(min_path_len, len(p3)) if min_path_len else len(p3)
                    )
        assert min_path_len
        complexity += min_path_len * int(code[:-1], base=10)
    print(complexity)
    return complexity


def p21b(f: TextIO) -> int:
    return 1


if __name__ == "__main__":
    run_solution(p21a, p21b, 21)
