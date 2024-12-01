from typing import TextIO

from aoc24.helpers.main import run_solution


def _load_input(f: TextIO) -> tuple[list[int], list[int]]:
    # if x is a list of tuples, zip(*x) converts to a tuple of lists - [(1, 2), (3, 4)] -> ([1, 3], [2, 4])
    l1: list[int]
    l2: list[int]
    l1, l2 = zip(*[[int(c) for c in l.strip().split()] for l in f])  # type: ignore[assignment]
    return l1, l2


def p1a(f: TextIO) -> int:
    l1, l2 = _load_input(f)
    diffs = sum(abs(i1 - i2) for i1, i2 in zip(sorted(l1), sorted(l2)))
    return diffs


def p1b(f: TextIO) -> int:
    l1, l2 = _load_input(f)
    counts: dict[int, int] = {}
    for i in l2:
        counts[i] = counts.get(i, 0) + 1
    sims = sum(i * counts.get(i, 0) for i in l1)
    return sims


if __name__ == "__main__":
    run_solution(p1a, p1b, 1)
