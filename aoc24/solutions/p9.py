from typing import TextIO

from aoc24.helpers.main import run_solution


DiskMap = list[tuple[int | None, int]]


def find_gap(disk_map: DiskMap) -> int | None:
    return next(
        (i for i, (block_id, _) in enumerate(disk_map) if block_id is None), None
    )


def find_gap_at_least(disk_map: DiskMap, gap_len: int) -> int | None:
    return next(
        (
            i
            for i, (block_id, l) in enumerate(disk_map)
            if block_id is None and l >= gap_len
        ),
        None,
    )


def checksum(disk_map: DiskMap) -> int:
    total = 0
    idx = 0
    for block_id, block_len in disk_map:
        if block_id is not None:
            total += int(block_id * (block_len / 2) * (2 * idx + block_len - 1))
        idx += block_len
    return total


def p9a(f: TextIO) -> int:
    disk_map: DiskMap = []
    block_id_next = 0
    for i, c in enumerate(f.read().strip()):
        if i % 2 == 0:
            cur_block_id = block_id_next
            block_id_next += 1
        else:
            cur_block_id = None
        if l := int(c):
            disk_map.append((cur_block_id, l))

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
    return checksum(disk_map)


def p9b(f: TextIO) -> int:
    disk_map: DiskMap = []
    block_id_next = 0
    for i, c in enumerate(f.read().strip()):
        if i % 2 == 0:
            cur_block_id = block_id_next
            block_id_next += 1
        else:
            cur_block_id = None
        if l := int(c):
            disk_map.append((cur_block_id, l))

    not_done = list(range(block_id_next))
    while not_done:
        block_id = not_done.pop()
        block_idx, block_len = next(
            (
                (i, block_len)
                for i, (blckid, block_len) in enumerate(disk_map)
                if blckid == block_id
            ),
            (None, 0),
        )
        if block_idx is None:
            continue
        gap_idx = find_gap_at_least(disk_map, block_len)
        # print(i, block_id, gap_idx, gap_len, gaps[gap_len] if gap_len else None)
        if gap_idx is None or gap_idx > block_idx:
            continue
        _, gap_len = disk_map[gap_idx]
        disk_map[gap_idx] = (block_id, block_len)
        disk_map[block_idx] = (None, block_len)
        if gap_len > block_len:
            disk_map.insert(gap_idx + 1, (None, gap_len - block_len))
    return checksum(disk_map)


if __name__ == "__main__":
    run_solution(p9a, p9b, 9)
