import operator
from functools import reduce
from itertools import count
from typing import TextIO

from aoc24.helpers.grid import Offset, Position, move_position
from aoc24.helpers.main import run_solution


grid_size = Offset(101, 103)


def parse_ij(input: str) -> tuple[int, ...]:
    return tuple(int(s) for s in input.split("=")[1].split(","))


def load_input(f: TextIO) -> list[tuple[Position, Offset]]:
    robots = []
    for l in f:
        pv = l.strip().split()
        robots.append((Position(*parse_ij(pv[0])), Offset(*parse_ij(pv[1]))))
    return robots


def simulate(p: Position, v: Offset, reps: int, grid_size: Offset) -> Position:
    np = move_position(p, v * reps)
    return Position(np.i % grid_size.i, np.j % grid_size.j)


def quadrant(p: Position, grid_size: Offset) -> int | None:
    if p.i == grid_size.i // 2 or p.j == grid_size.j // 2:
        return None
    return ((p.i > grid_size.i // 2) << 1) + (p.j > grid_size.j // 2)


def p14a(f: TextIO) -> int:
    robots = load_input(f)
    positions = [simulate(p, v, 100, grid_size) for p, v in robots]
    quads = {i: 0 for i in range(4)}
    for robot in positions:
        if (quad := quadrant(robot, grid_size)) is not None:
            quads[quad] += 1
    return reduce(operator.mul, quads.values(), 1)


def display(robots: set[Position]) -> None:
    for j in range(grid_size.j + 1):
        l = ""
        for i in range(grid_size.i + 1):
            if Position(i, j) in robots:
                l = l + "#"
            else:
                l = l + "."
        print(l)


def find_vert_lines(positions: set[Position], min_length: int) -> int:
    positions = positions.copy()
    count = 0
    while positions:
        p = positions.pop()
        line = {p}
        to_search = {p}
        while to_search:
            p = to_search.pop()
            for move in [Offset(0, 1), Offset(0, -1)]:
                np = move_position(p, move)
                if np in positions:
                    to_search.add(np)
                    line.add(np)
                    positions.discard(np)
        count += len(line) >= min_length
    return count


def p14b(f: TextIO) -> int:
    # Answer: 7492
    robots = load_input(f)
    # Skip forwards now I know the solution. Remove for exploring
    robots = [(simulate(p, v, 7000, grid_size), v) for p, v in robots]
    i = 0
    for i in count(7001):
        robots = [(simulate(p, v, 1, grid_size), v) for p, v in robots]
        if find_vert_lines({p for p, _ in robots}, 6) >= 2:
            display({p for p, _ in robots})
            print(f"i={i}")
            break
    return i


if __name__ == "__main__":
    run_solution(p14a, p14b, 14)
