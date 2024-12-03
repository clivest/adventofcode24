from typing import TextIO

from aoc24.helpers.main import run_solution


def seek_mul(input: str, start: int) -> tuple[int, int] | None:
    index = start
    while (index := input.find("mul(", index)) != -1:
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
            if index >= len(input):
                break
        else:
            if len(nums) == 2 and all(nums):
                return int(nums[0]) * int(nums[1]), index
    return None


def p3a(f: TextIO) -> int:
    input = f.read()
    index = 0
    total = 0
    while (mul := seek_mul(input, index)) is not None:
        total += mul[0]
        index = mul[1]
    return total


# def p3b(f: TextIO) -> int:
#     reports = _load_reports(f)
#     safe = sum(_is_good_report_skip_1(report) for report in reports)
#     return safe


if __name__ == "__main__":
    run_solution(p3a, None, 3)
