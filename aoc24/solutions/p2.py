from typing import TextIO

from aoc24.helpers.main import run_solution


def _load_reports(f: TextIO) -> list[list[int]]:
    return [[int(c) for c in l.split()] for l in f]


def _is_good(l1: int, l2: int, l3: int | None) -> bool:
    return (1 <= abs(l1 - l2) <= 3) and (l3 is None or (l1 > l2 > l3) or (l1 < l2 < l3))


def _is_good_report(report: list[int]) -> bool:
    for levels in zip(report, report[1:], report[2:]):
        if not _is_good(*levels):
            return False
    # check last pair
    return _is_good(report[-2], report[-1], None)


def _is_good_report_skip_1(report: list[int], skipped: bool = False) -> bool:
    for i, levels in enumerate(zip(report, report[1:], report[2:])):
        if not _is_good(*levels):
            if skipped:
                return False
            # Check if the remaining sequence is good if either ith, i+1th or i+2th elements are skipped
            return any(
                _is_good_report_skip_1(
                    report[max(i - 1, 0) : i + offset] + report[i + 1 + offset :], True
                )
                for offset in range(3)
            )
    # check last pair
    return _is_good(report[-2], report[-1], None) or not skipped


def p2a(f: TextIO) -> int:
    reports = _load_reports(f)
    safe = sum(_is_good_report(report) for report in reports)
    return safe


def p2b(f: TextIO) -> int:
    reports = _load_reports(f)
    safe = sum(_is_good_report_skip_1(report) for report in reports)
    return safe


if __name__ == "__main__":
    run_solution(p2a, p2b, 2)
