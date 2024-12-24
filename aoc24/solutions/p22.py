from itertools import tee, islice
from typing import TextIO, Iterable, cast

from aoc24.helpers.main import run_solution


ChangeSeq = tuple[int, int, int, int]


def generate_secrets(secret: int, count: int) -> Iterable[int]:
    ops = [
        lambda s: s * 64,
        lambda s: s // 32,
        lambda s: s * 2048,
    ]
    yield secret
    for _ in range(count):
        for op in ops:
            n = op(secret)
            secret ^= n
            secret = secret % 16777216
        yield secret


def p22a(f: TextIO) -> int:
    total = 0
    for l in f:
        secret = int(l.strip())
        *_, secret = generate_secrets(secret, 2000)
        total += secret
    return total


def p22b(f: TextIO) -> int:
    max_bananas = 0
    overall_changes: dict[ChangeSeq, int] = {}
    for l in f:
        seed = int(l.strip())
        prices = tee((s % 10 for s in generate_secrets(seed, 2000)), 2)
        seen: set[ChangeSeq] = set()
        changes: tuple[int, ...] = tuple()
        for last, price in zip(prices[0], islice(prices[1], 1, None)):
            changes = (changes + (price - last,))[-4:]
            if len(changes) == 4 and changes not in seen:
                ch4 = cast(ChangeSeq, changes)
                overall_changes.setdefault(ch4, 0)
                overall_changes[ch4] += price
                seen.add(ch4)
                max_bananas = max(max_bananas, overall_changes[ch4])
    return max_bananas


if __name__ == "__main__":
    run_solution(p22a, p22b, 22)
