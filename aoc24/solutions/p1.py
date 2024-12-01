from typing import TextIO

from helpers.main import run_solution


def load_input(f: TextIO) -> tuple[list[int], list[int]]:
    # if x is a list of tuples, zip(*x) converts to a tuple of lists - [(1, 2), (3, 4)] -> ([1, 3], [2, 4])
    l1, l2 = zip(*[[int(c) for c in l.strip().split()] for l in f])
    return l1, l2


def pa(f: TextIO) -> None:
    l1, l2 = load_input(f)
    diffs = sum(abs(i1 - i2) for i1, i2 in zip(sorted(l1), sorted(l2)))
    # originally code as print(diffs) then switch to an assert based on the accepted answer so I can refactor and test
    assert diffs == 1223326


def pb(f: TextIO) -> None:
    l1, l2 = load_input(f)
    counts = {}
    for i in l2:
        counts[i] = counts.get(i, 0) + 1
    sims = sum(i * counts.get(i, 0) for i in l1)
    assert sims == 21070419


if __name__ == "__main__":
    run_solution(pa, pb, 1)
