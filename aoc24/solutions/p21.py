from functools import cache
from typing import TextIO, Iterable

from aoc24.helpers.grid import Position
from aoc24.helpers.main import run_solution


Keypad = dict[str, Position]

dpad = {
    "^": Position(0, 1),
    "A": Position(0, 2),
    "<": Position(1, 0),
    "v": Position(1, 1),
    ">": Position(1, 2),
}


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
    return min_paths(code, dpad["A"], dpad, Position(0, 0))


def move_count(dcode: str) -> int:
    def mc(p1: Position, p2: Position) -> int:
        return abs(p1.i - p2.i) + abs(p1.j - p2.j)

    return sum(mc(dpad[c1], dpad[c2]) for c1, c2 in zip(dcode, dcode[1:]))


def moves_() -> dict[tuple[str, str], set[str]]:
    mvs = {}
    gap = Position(0,0)
    for a, pos in dpad.items():
        for b, dest in dpad.items():
            v = ("^" if dest.i < pos.i else "v") * abs(dest.i - pos.i)
            h = (">" if dest.j > pos.j else "<") * abs(dest.j - pos.j)
            mvs_i = set()
            if not (pos.j == gap.j and dest.i == gap.i):
                mvs_i.add(v + h + "A")
            if not (pos.i == gap.i and dest.j == gap.j):
                mvs_i.add(h + v + 'A')
            mvs[(a,b)] = mvs_i
    return mvs


moves = moves_()

@cache
def calc_move_len(start: str, target: str, depth: int) -> int:
    seqs = moves[(start, target)]
    if depth == 0:
        return min(len(seq) for seq in seqs)
    return min(sum(calc_move_len(s, t, depth - 1) for s, t in zip('A' + seq, seq)) for seq in seqs)


def calc_path_len(path: str, depth: int) -> int:
    return sum(calc_move_len(s, t, depth-1) for s, t in zip('A' + path, path))


def calc_complexity(code: str, robots: int) -> int:
    paths = set(min_paths_r1(code))
    return min(calc_path_len(p, robots-1) for p in paths) * int(code[:-1], base=10)


def p21a(f: TextIO) -> int:
    return sum(calc_complexity(l.strip(), 3) for l in f)


def p21b(f: TextIO) -> int:
    c = sum(calc_complexity(l.strip(), 26) for l in f)
    print(c)
    return c


if __name__ == "__main__":
    run_solution(p21a, p21b, 21)
