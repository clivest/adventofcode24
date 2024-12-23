from typing import TextIO

from aoc24.helpers.main import run_solution


def is_possible(
    design: str, patterns: list[str], tested_designs: dict[str, bool]
) -> bool:
    if not design:
        return True
    if design in tested_designs:
        return tested_designs[design]
    for p in patterns:
        if not design.startswith(p):
            continue
        if is_possible(design.removeprefix(p), patterns, tested_designs):
            tested_designs[design] = True
            return True
    tested_designs[design] = False
    return False


def p19a(f: TextIO) -> int:
    patterns = f.readline().strip().split(", ")
    assert not f.readline().strip()
    patterns.sort(key=lambda p: len(p), reverse=True)
    tested_designs: dict[str, bool] = {}
    possible = sum(is_possible(l.strip(), patterns, tested_designs) for l in f)
    print(possible)
    return possible


def p19b(f: TextIO) -> int:
    return 1


if __name__ == "__main__":
    run_solution(p19a, p19b, 19)
