from functools import cache
from typing import TextIO

from aoc24.helpers.main import run_solution


@cache
def blink(s: int, iter: int) -> int:
    digs = str(s)
    if iter == 0:
        return 1
    if not s:
        return blink(1, iter - 1)
    elif len(digs) % 2 == 0:
        return blink(int(digs[: len(digs) // 2]), iter - 1) + blink(
            int(digs[len(digs) // 2 :]), iter - 1
        )
    else:
        return blink(s * 2024, iter - 1)


def p11a(f: TextIO) -> int:
    stones = [int(i) for i in f.read().split()]
    total = sum(blink(s, 25) for s in stones)
    print(total)
    return total


def p11b(f: TextIO) -> int:
    stones = [int(i) for i in f.read().split()]
    total = sum(blink(s, 75) for s in stones)
    print(total)
    return total


if __name__ == "__main__":
    run_solution(p11a, p11b, 11)
