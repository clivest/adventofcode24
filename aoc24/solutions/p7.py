from typing import TextIO

from aoc24.helpers.main import run_solution


def can_solve_add_mult(total: int, inputs: list[int]) -> bool:
    if not inputs:
        # Finished
        return total == 0
    # Check if we can divide or subtract the final value from the input, then solve the remaining equation
    v = inputs[-1]
    return (total % v == 0 and can_solve_add_mult(total // v, inputs[:-1])) or (
        total >= v and can_solve_add_mult(total - v, inputs[:-1])
    )


def reverse_concat(input: int, total: int) -> int | None:
    # Normally there's a better way of manipulating numbers than converting to string and back
    tstr = str(total)
    istr = str(input)
    if tstr.endswith(istr):
        return int(tstr.removesuffix(istr))
    return None


def can_solve_add_mult_concat(total: int, inputs: list[int]) -> bool:
    if not inputs:
        # Finished
        return total == 0
    # Check if we can divide or subtract the final value from the input, then solve the remaining equation
    v = inputs[-1]
    return (
        (total % v == 0 and can_solve_add_mult_concat(total // v, inputs[:-1]))
        or (total >= v and can_solve_add_mult_concat(total - v, inputs[:-1]))
        or bool(
            (new_total := reverse_concat(v, total))
            and can_solve_add_mult_concat(new_total, inputs[:-1])
        )
    )


def p7a(f: TextIO) -> int:
    total_solvable = 0
    for l in f:
        total_s, rest = l.split(":")
        total = int(total_s)
        inputs = [int(i) for i in rest.split()]
        if can_solve_add_mult(total, inputs):
            total_solvable += total
    return total_solvable


def p7b(f: TextIO) -> int:
    total_solvable = 0
    for l in f:
        total_s, rest = l.split(":")
        total = int(total_s)
        inputs = [int(i) for i in rest.split()]
        if can_solve_add_mult_concat(total, inputs):
            total_solvable += total
    return total_solvable


if __name__ == "__main__":
    run_solution(p7a, p7b, 7)
