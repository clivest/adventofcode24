from typing import TextIO

from aoc24.helpers.main import run_solution


def p25a(f: TextIO) -> int:
    locks: set[tuple[int, ...]] = set()
    keys: set[tuple[int, ...]] = set()
    v: tuple[int, ...] = tuple()
    is_lock: bool | None = None
    for l in f:
        l = l.strip()
        if not l:
            assert is_lock is not None
            (locks if is_lock else keys).add(v)
            v = ()
            is_lock = None
        elif is_lock is None:
            is_lock = all(c == "#" for c in l)
            v = tuple(c == "#" for c in l)
        else:
            v = tuple(vi + (c == "#") for vi, c in zip(v, l))
    if v:
        assert is_lock is not None
        (locks if is_lock else keys).add(v)
    fit = sum(
        all(li + vi <= 7 for li, vi in zip(lock, key)) for lock in locks for key in keys
    )
    return fit


if __name__ == "__main__":
    # No part b today
    run_solution(p25a, None, 25)
