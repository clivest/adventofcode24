from typing import TextIO

from aoc24.helpers.grid import iter_grid, Position, Offset, move_position
from aoc24.helpers.main import run_solution


class ImpossibleMove(Exception):
    pass


def load_grid(f: TextIO) -> tuple[Position, set[Position], set[Position]]:
    robot: Position | None = None
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
    assert robot
    return robot, obstacles, walls


def find_end_of_obstacle_chain(
    start: Position, move: Offset, obstacles: set[Position]
) -> Position:
    while start in obstacles:
        start = move_position(start, move)
    return start


def double_grid_size(robot: Position, obstacles: set[Position], walls:set[Position]) -> tuple[Position, set[Position], set[Position]]:
    robot = Position(robot.i, robot.j*2)
    walls = {Position(w.i, w.j*2) for w in walls} | {Position(w.i, w.j*2 + 1) for w in walls}
    obstacles = {Position(o.i, o.j*2) for o in obstacles}
    return robot, obstacles, walls


def find_large_obstacles_to_move(start: Position, move: Offset, obstacles: set[Position], walls: set[Position]) -> set[Position]:
    obstacles_to_move = set()
    to_explore = {start}
    while to_explore:
        position = to_explore.pop()
        if position in walls:
            raise ImpossibleMove
        if move == Offset(0, 1):
            if position in obstacles:
                to_explore.add(move_position(position, move * 2))
                obstacles_to_move.add(position)
        elif move == Offset(0, -1):
            possible_obstacle = move_position(position, move)
            if possible_obstacle in obstacles:
                to_explore.add(move_position(position, move * 2))
                obstacles_to_move.add(possible_obstacle)
        else:
            for offset in [Offset(0, 0), Offset(0, -1)]:
                possible_obstacle = move_position(position, offset)
                if possible_obstacle in obstacles:
                    obstacles_to_move.add(possible_obstacle)
                    to_explore.add(move_position(possible_obstacle, move))
                    to_explore.add(move_position(move_position(possible_obstacle, move), Offset(0, 1)))
    return obstacles_to_move


def p15a(f: TextIO) -> int:
    robot, obstacles, walls = load_grid(f)
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
    return gps


def p15b(f: TextIO) -> int:
    robot, obstacles, walls = load_grid(f)
    robot, obstacles, walls = double_grid_size(robot, obstacles, walls)
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
        try:
            obstacles_to_move = find_large_obstacles_to_move(robot_new, move, obstacles, walls)
        except ImpossibleMove:
            continue
        robot = robot_new
        obstacles -= obstacles_to_move
        obstacles |= {move_position(o, move) for o in obstacles_to_move}
    gps = sum(p.i * 100 + p.j for p in obstacles)
    return gps


if __name__ == "__main__":
    run_solution(p15a, p15b, 15)
