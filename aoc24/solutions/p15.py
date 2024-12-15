from typing import TextIO

from aoc24.helpers.grid import iter_grid, Position, Offset, move_position
from aoc24.helpers.main import run_solution


def load_grid(f: TextIO) -> tuple[Position, set[Position], set[Position], Offset]:
    robot: Position | None = None
    grid_size = Offset(0, 0)
    obstacles: set[Position] = set()
    walls: set[Position] = set()
    for pos, c in iter_grid(f, stop=lambda l: not l):
        match c:
            case "#":
                walls.add(pos)
            case "O":
                obstacles.add(pos)
            case "@":
                assert not robot
                robot = pos
        grid_size = Offset(max(grid_size.i, pos.i), max(grid_size.j, pos.j))
    assert robot
    return robot, obstacles, walls, grid_size + Offset(1, 1)


def find_end_of_obstacle_chain(
    start: Position, move: Offset, obstacles: set[Position]
) -> Position:
    while start in obstacles:
        start = move_position(start, move)
    return start


def p15a(f: TextIO) -> int:
    robot, obstacles, walls, grid_size = load_grid(f)
    for i in f.read().strip():
        move = {
            "v": Offset(1, 0),
            "^": Offset(-1, 0),
            "<": Offset(0, -1),
            ">": Offset(0, 1),
            "\n": None,
        }[i]
        if not move:
            continue
        robot_new = move_position(robot, move)
        end_of_chain = find_end_of_obstacle_chain(robot_new, move, obstacles)
        if end_of_chain in walls:
            continue
        robot = robot_new
        if robot_new in obstacles:
            obstacles.remove(robot_new)
            obstacles.add(end_of_chain)
    gps = sum(p.i * 100 + p.j for p in obstacles)
    print(gps)
    return gps


def p15b(f: TextIO) -> int:
    return 1


if __name__ == "__main__":
    run_solution(p15a, p15b, 15)
