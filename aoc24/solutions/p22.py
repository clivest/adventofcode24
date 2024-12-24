from typing import TextIO

from aoc24.helpers.main import run_solution


def p22a(f: TextIO) -> int:
    ops = [
        lambda s: s * 64,
        lambda s: s // 32,
        lambda s: s * 2048,
    ]
    total = 0
    for l in f:
        secret = int(l.strip())
        for _ in range(2000):
            for op in ops:
                n = op(secret)
                secret ^= n
                secret = secret % 16777216
        total += secret
    print(total)
    return total


def p22b(f: TextIO) -> int:
    return 1


if __name__ == "__main__":
    run_solution(p22a, p22b, 22)
