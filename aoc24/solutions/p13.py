from typing import TextIO, Generator

from aoc24.helpers.grid import Offset, Position, move_position
from aoc24.helpers.main import run_solution
import re


def load_puzzles(f: TextIO) -> Generator[tuple[Offset, Offset, Position], None, None]:
    a = b = prize = None
    for l in f:
        l = l.strip()
        if not l:
            assert a and b and prize
            yield a, b, prize
            a = b = prize = None
            continue
        thing, loc = l.split(": ")
        match thing:
            case "Button A":
                assert a is None
                a = parse_offset(loc)
            case "Button B":
                assert b is None
                b = parse_offset(loc)
            case "Prize":
                assert prize is None
                prize = parse_position(loc)
            case _:
                assert False, thing
    if a:
        assert a and b and prize
        yield a, b, prize


def parse_offset(input: str) -> Offset:
    match = re.match(r"X[+]([0-9]*), Y[+]([0-9]*)", input)
    assert match
    return Offset(*[int(i) for i in match.groups()])


def parse_position(input: str) -> Position:
    match = re.match(r"X=([0-9]*), Y=([0-9]*)", input)
    assert match
    return Position(*[int(i) for i in match.groups()])


def play(a: Offset, b: Offset, prize: Position) -> int | None:
    if a.i * b.j != b.i * a.j:
        # There's a unique solution
        num = a.j * prize.i - a.i * prize.j
        den = b.i * a.j - b.j * a.i
        if num % den != 0:
            return None
        b_count = num // den
        num = prize.i - b_count * b.i
        den = a.i
        if num % den != 0:
            return None
        return b_count + 3 * num // den
    else:
        # No unique solution. The 2 simultaneous equations reduce to 1
        # No input requires this solution. TODO!
        raise NotImplementedError


def p13a(f: TextIO) -> int:
    min_cost = 0
    for a, b, prize in load_puzzles(f):
        if (cost := play(a, b, prize)) is not None:
            min_cost += cost
    return min_cost


def p13b(f: TextIO) -> int:
    min_cost = 0
    for a, b, prize in load_puzzles(f):
        prize = move_position(prize, Offset(10000000000000, 10000000000000))
        if (cost := play(a, b, prize)) is not None:
            min_cost += cost
    return min_cost


if __name__ == "__main__":
    run_solution(p13a, p13b, 13)
