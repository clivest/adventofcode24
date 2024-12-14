from typing import TextIO

from aoc24.helpers.grid import Offset, Position, position_diff, move_position
from aoc24.helpers.main import run_solution
import re


def parse_offset(input: str) -> Offset:
    match = re.match(r"X[+]([0-9]*), Y[+]([0-9]*)", input)
    assert match
    return Offset(*[int(i) for i in match.groups()])


def parse_position(input: str) -> Position:
    match = re.match(r"X=([0-9]*), Y=([0-9]*)", input)
    assert match
    return Position(*[int(i) for i in match.groups()])


def play_min(
    l: Offset, r: Offset, prize: Position, l_cost: int, r_cost: int
) -> int | None:
    # minimise number of `l` button presses
    l_count_max = int(
        position_diff(prize, Position(0, 0)).magnitude() / l.magnitude() + 1
    )
    for l_count in range(l_count_max, 0, -1):
        r_r_count = position_diff(move_position(Position(0, 0), l * l_count), prize)
        if (
            r_r_count.i % r.i == r_r_count.j % r.j == 0
            and r_r_count.i // r.i == r_r_count.j // r.j
        ):
            r_count = r_r_count.i // r.i
            return l_count * l_cost + r_count * r_cost
    return None


def play(a: Offset, b: Offset, prize: Position) -> int | None:
    if a.magnitude() < b.magnitude() * 3:
        return play_min(a, b, prize, 3, 1)
    else:
        return play_min(b, a, prize, 1, 3)


def p13a(f: TextIO) -> int:
    a = None
    b = None
    prize = None
    min_cost = 0
    for l in f:
        l = l.strip()
        if not l:
            assert a and b and prize
            if (cost := play(a, b, prize)) is not None:
                min_cost += cost
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
        if (cost := play(a, b, prize)) is not None:
            min_cost += cost
    return min_cost


def p13b(f: TextIO) -> int:
    return 1


if __name__ == "__main__":
    run_solution(p13a, p13b, 13)
