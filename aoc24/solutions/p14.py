import operator
from functools import reduce
from typing import TextIO

from aoc24.helpers.grid import Offset, Position, move_position
from aoc24.helpers.main import run_solution


def parse_ij(input: str) -> tuple[int, ...]:
    return tuple(int(s) for s in input.split("=")[1].split(","))


def simulate(p: Position, v: Offset, reps: int, grid_size: Offset) -> Position:
    np = move_position(p, v * reps)
    return Position(np.i % grid_size.i, np.j % grid_size.j)


def p14a(f: TextIO) -> int:
    grid_size = Offset(101, 103)
    robots = []
    for l in f:
        pv = l.strip().split()
        robots.append((Position(*parse_ij(pv[0])), Offset(*parse_ij(pv[1]))))
    positions = [simulate(p, v, 100, grid_size) for p, v in robots]
    quads = {i: 0 for i in range(4)}
    for robot in positions:
        if robot.i < 50 and robot.j < 51:
            quads[0] += 1
        if robot.i > 50 and robot.j < 51:
            quads[1] += 1
        if robot.i < 50 and robot.j > 51:
            quads[2] += 1
        if robot.i > 50 and robot.j > 51:
            quads[3] += 1
    safety_factor = reduce(operator.mul, quads.values(), 1)
    return safety_factor


def p14b(f: TextIO) -> int:
    return 1


if __name__ == "__main__":
    run_solution(p14a, p14b, 14)
