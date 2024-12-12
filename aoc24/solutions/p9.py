from typing import TextIO

from aoc24.helpers.main import run_solution


DiskMap = list[tuple[int | None, int]]


def find_gap(disk_map: DiskMap) -> int | None:
    return next(
        (i for i, (block_id, _) in enumerate(disk_map) if block_id is None), None
    )


def p9a(f: TextIO) -> int:
    disk_map: list[tuple[int | None, int]] = []
    block_id_next = 0
    is_gap = False
    for c in f.read().strip():
        if not is_gap:
            cur_block_id = block_id_next
            block_id_next += 1
        else:
            cur_block_id = None
        if l := int(c):
            disk_map.append((cur_block_id, l))
        is_gap = not is_gap

    gap_idx = find_gap(disk_map)
    while gap_idx is not None and gap_idx < len(disk_map) - 1:
        block_id, block_len = disk_map.pop()
        _, gap_len = disk_map[gap_idx]
        if block_id is None:
            continue
        disk_map[gap_idx] = (block_id, min(block_len, gap_len))
        if block_len > gap_len:
            disk_map.append((block_id, block_len - gap_len))
        elif gap_len > block_len:
            disk_map.insert(gap_idx + 1, (None, gap_len - block_len))
        gap_idx = find_gap(disk_map)

    total = 0
    idx = 0
    for block_id, block_len in disk_map:
        if block_id is not None:
            total += int(block_id * (block_len / 2) * (2 * idx + block_len - 1))
        idx += block_len
    return total


def p9b(f: TextIO) -> int:
    return 1


if __name__ == "__main__":
    run_solution(p9a, p9b, 9)
