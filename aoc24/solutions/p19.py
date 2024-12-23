from typing import TextIO

from aoc24.helpers.main import run_solution


def count_possibilities(
    design: str, patterns: list[str], tested_designs: dict[str, int]
) -> int:
    if not design:
        return 1
    if design in tested_designs:
        return tested_designs[design]
    ways = 0
    for p in patterns:
        if not design.startswith(p):
            continue
        ways += count_possibilities(design.removeprefix(p), patterns, tested_designs)
    tested_designs[design] = ways
    return ways


def p19a(f: TextIO) -> int:
    patterns = f.readline().strip().split(", ")
    assert not f.readline().strip()
    patterns.sort(key=lambda p: len(p), reverse=True)
    tested_designs: dict[str, int] = {}
    return sum(
        bool(count_possibilities(l.strip(), patterns, tested_designs)) for l in f
    )


def p19b(f: TextIO) -> int:
    patterns = f.readline().strip().split(", ")
    assert not f.readline().strip()
    patterns.sort(key=lambda p: len(p), reverse=True)
    tested_designs: dict[str, int] = {}
    return sum(count_possibilities(l.strip(), patterns, tested_designs) for l in f)


if __name__ == "__main__":
    run_solution(p19a, p19b, 19)
