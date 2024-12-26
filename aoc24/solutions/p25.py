from typing import TextIO

from aoc24.helpers.main import run_solution


Heights = tuple[int, ...]


def p25a(f: TextIO) -> int:
    locks: list[Heights] = list()
    keys: list[Heights] = list()
    collection: list[Heights] | None = None
    for l in f:
        l = l.strip()
        if not l:
            collection = None
        elif collection is None:
            collection = locks if all(c == "#" for c in l) else keys
            collection.append(tuple(c == "#" for c in l))
        else:
            collection[-1] = tuple(vi + (c == "#") for vi, c in zip(collection[-1], l))
    fit = sum(
        all(li + vi <= 7 for li, vi in zip(lock, key)) for lock in locks for key in keys
    )
    return fit


if __name__ == "__main__":
    # No part b today
    run_solution(p25a, None, 25)
