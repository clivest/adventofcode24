from typing import TextIO

from aoc24.helpers.main import run_solution


def p5a(f: TextIO) -> int:
    before_rules: dict[int, set[int]] = {}  # k must come before vs
    lines = iter(f)
    for l in lines:
        l = l.strip()
        if not l:
            break
        a, b = [int(c) for c in l.split("|")]
        before_rules.setdefault(a, set()).add(b)

    total = 0
    for l in lines:
        update = [int(c) for c in l.strip().split(",")]
        seen: set[int] = set()
        for page in update:
            if page in before_rules and (seen & before_rules[page]):
                break
            seen.add(page)
        else:
            # All rules followed
            total += update[len(update) // 2]
    return total


def p5b(f: TextIO) -> None:
    pass


if __name__ == "__main__":
    run_solution(p5a, p5b, 5)
