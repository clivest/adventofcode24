from typing import TextIO

from aoc24.helpers.main import run_solution


Heights = tuple[int, ...]


def p25a(f: TextIO) -> int:
    locks: set[Heights] = set()
    keys: set[Heights] = set()
    v: Heights = tuple()
    collection: set[Heights] | None = None
    for l in f:
        l = l.strip()
        if not l:
            assert collection is not None
            collection.add(v)
            v = ()
            collection = None
        elif collection is None:
            collection = locks if all(c == "#" for c in l) else keys
            v = tuple(c == "#" for c in l)
        else:
            v = tuple(vi + (c == "#") for vi, c in zip(v, l))
    if v:
        assert collection is not None
        collection.add(v)
    fit = sum(
        all(li + vi <= 7 for li, vi in zip(lock, key)) for lock in locks for key in keys
    )
    return fit


if __name__ == "__main__":
    # No part b today
    run_solution(p25a, None, 25)
