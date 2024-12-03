from typing import TextIO

from aoc24.helpers.main import run_solution


def seek_mul(input: str, start: int, end: int | None = None) -> tuple[int, int] | None:
    # find a mul(X,Y) in range [start, end) and return (X*Y, index of the ')') if an instruction is found
    # else None
    index = start
    while (index := input.find("mul(", index, end)) != -1:
        index += 4
        nums = [""]
        while input[index] != ")":
            if input[index].isdigit():
                nums[-1] = f"{nums[-1]}{input[index]}"
            elif input[index] == "," and len(nums) == 1:
                nums.append("")
            else:
                break
            index += 1
            if index >= len(input) or (end and index >= end):
                break
        else:
            if len(nums) == 2 and all(nums):
                return int(nums[0]) * int(nums[1]), index
    return None


def seek_do_dont(input: str, start: int) -> tuple[bool, int] | None:
    # find a do() or don't() instruction in input[start:] and (enabled, index of the next char) if an instruction is
    # found else None
    index = start
    while (index := input.find("do", index)) != -1:
        index += 2
        if input.startswith("()", index):
            return True, index + 2
        if input.startswith("n't()", index):
            return False, index + 5
    return None


def p3a(f: TextIO) -> int:
    input = f.read()
    index = 0
    total = 0
    while (mul := seek_mul(input, index)) is not None:
        total += mul[0]
        index = mul[1]
    return total


def p3b(f: TextIO) -> int:
    input = f.read()
    index = 0
    total = 0
    enabled = True
    while True:
        do_dont = seek_do_dont(input, index)
        if enabled:
            # if enabled, find mul instructions between current index and the next do/dont instruction, if there is one,
            # else end of the input
            while mul := seek_mul(input, index, do_dont[1] if do_dont else None):
                total += mul[0]
                index = mul[1]
        if do_dont is None:
            break
        # scan from the next do/dont instruction
        enabled, index = do_dont
    return total


if __name__ == "__main__":
    run_solution(p3a, p3b, 3)
