from functools import cache
from typing import TextIO

from aoc24.helpers.grid import Position
from aoc24.helpers.main import run_solution


Keypad = dict[str, Position]


def min_paths(code: str, pos: Position, keypad: Keypad, gap: Position) -> set[str]:
    if not code:
        return {""}
    possible_min_paths = set()
    for min_path in min_paths(code[1:], keypad[code[0]], keypad, gap):
        dest = keypad[code[0]]
        v = ("^" if dest.i < pos.i else "v") * abs(dest.i - pos.i)
        h = (">" if dest.j > pos.j else "<") * abs(dest.j - pos.j)
        if not (pos.j == gap.j and dest.i == gap.i):
            possible_min_paths.add(v + h + "A" + min_path)
        if not (pos.i == gap.i and dest.j == gap.j):
            possible_min_paths.add(h + v + "A" + min_path)
    return possible_min_paths


def min_paths_r1(code: str) -> set[str]:
    keypad = {s: Position(i // 3, i % 3) for i, s in enumerate("789456123.0A")}
    return min_paths(code, keypad["A"], keypad, keypad["."])


def calc_possible_dpad_moves() -> dict[tuple[str, str], set[str]]:
    dpad = {s: Position(i // 3, i % 3) for i, s in enumerate(".^A<v>")}
    mvs = {
        (a, b): min_paths(b, pos, dpad, Position(0, 0))
        for a, pos in dpad.items()
        for b in dpad.keys()
    }
    return mvs


_possible_dpad_moves = calc_possible_dpad_moves()


@cache
def calc_move_len(start: str, target: str, depth: int) -> int:
    seqs = _possible_dpad_moves[(start, target)]
    if depth == 0:
        return min(len(seq) for seq in seqs)
    return min(
        sum(calc_move_len(s, t, depth - 1) for s, t in zip("A" + seq, seq))
        for seq in seqs
    )


def calc_path_len(path: str, depth: int) -> int:
    return sum(calc_move_len(s, t, depth - 1) for s, t in zip("A" + path, path))


def calc_complexity(code: str, robots: int) -> int:
    paths = min_paths_r1(code)
    return min(calc_path_len(p, robots - 1) for p in paths) * int(code[:-1], base=10)


def p21a(f: TextIO) -> int:
    return sum(calc_complexity(l.strip(), 3) for l in f)


def p21b(f: TextIO) -> int:
    return sum(calc_complexity(l.strip(), 26) for l in f)


if __name__ == "__main__":
    run_solution(p21a, p21b, 21)
