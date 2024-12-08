from typing import TextIO


from aoc24.helpers.main import run_solution


def can_solve(total: int, inputs: list[int]) -> bool:
    if not inputs:
        return total == 0
    v = inputs[-1]
    if total % v == 0 and can_solve(total // v, inputs[:-1]):
        return True
    if total >= v and can_solve(total - v, inputs[:-1]):
        return True
    return False


def p7a(f: TextIO) -> int:
    total_solvable = 0
    for l in f:
        total_s, rest = l.split(":")
        total = int(total_s)
        inputs = [int(i) for i in rest.split()]
        if can_solve(total, inputs):
            total_solvable += total
    print(total_solvable)
    return total_solvable


def p7b(f: TextIO) -> int:
    return 1


if __name__ == "__main__":
    run_solution(p7a, p7b, 7)
