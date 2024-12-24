from functools import cache
from typing import TextIO

from aoc24.helpers.grid import Position
from aoc24.helpers.main import run_solution


Keypad = dict[str, Position]


def min_paths(code: str, location: str, keypad: Keypad) -> set[str]:
    """
    Robot arm is at position `pos` and has to input `code` on `keypad`. Find potential optimal paths
    For optimal paths, repeated key presses are preferred (e.g. prefer ^^^>>> over ^>^>^>)
    :param code: required input
    :param location: current robot location
    :param keypad: keypad (where `.` represents a gap that cannot be passed through)
    :return: set of possible min paths to consider
    """
    if not code:
        return {""}
    gap = keypad["."]
    pos = keypad[location]
    possible_min_paths = set()
    for min_path in min_paths(code[1:], code[0], keypad):
        dest = keypad[code[0]]
        v = ("^" if dest.i < pos.i else "v") * abs(dest.i - pos.i)
        h = (">" if dest.j > pos.j else "<") * abs(dest.j - pos.j)
        if not (pos.j == gap.j and dest.i == gap.i):
            # Possible if it doesn't pass through the gap
            possible_min_paths.add(v + h + "A" + min_path)
        if not (pos.i == gap.i and dest.j == gap.j):
            # Possible if it doesn't pass through the gap
            possible_min_paths.add(h + v + "A" + min_path)
    return possible_min_paths


def min_paths_r1(code: str) -> set[str]:
    """
    Min paths for the first robot (which is entering a code on the numeric keypad
    :param code: code to enter
    :return: set of potential min paths
    """
    keypad = {s: Position(i // 3, i % 3) for i, s in enumerate("789456123.0A")}
    return min_paths(code, "A", keypad)


def calc_possible_dpad_moves() -> dict[tuple[str, str], set[str]]:
    """
    Pre calculate a mapping of (current position, target) -> possible min sequences for robots working on dpads
    """
    dpad = {s: Position(i // 3, i % 3) for i, s in enumerate(".^A<v>")}
    mvs = {(a, b): min_paths(b, a, dpad) for a in dpad.keys() for b in dpad.keys()}
    return mvs


_possible_dpad_moves = calc_possible_dpad_moves()


@cache
def calc_move_len(start: str, target: str, depth: int) -> int:
    """
    Calculate the min number of moves to get a robot at depth `depth` on location `start` to press the button `target`
    :param start: current robot arm location
    :param target: button that needs to be pressed
    :param depth: depth of the robot in the chain
    :return: min number of button presses to make the robot do the move
    """
    seqs = _possible_dpad_moves[(start, target)]
    if depth == 0:
        return min(len(seq) for seq in seqs)
    # robot arm will have been left at `A` after making the next robot in the chain press the previous button
    return min(
        sum(calc_move_len(s, t, depth - 1) for s, t in zip("A" + seq, seq))
        for seq in seqs
    )


def calc_path_len(path: str, depth: int) -> int:
    """
    Calculate the min path length of a robot chain size `depth` to enter code `path`
    :param path: dpad code required on the end robot
    :param depth: depth of the chain
    :return: min path length
    """
    # robot arm is at `A` where it starts
    return sum(calc_move_len(s, t, depth - 1) for s, t in zip("A" + path, path))


def calc_complexity(code: str, robots: int) -> int:
    """
    Min path length for the code * code as an integer
    :param code: code to input on the numerical keypad
    :param robots: depth of the robot chain
    :return: complexity
    """
    paths = min_paths_r1(code)
    return min(calc_path_len(p, robots - 1) for p in paths) * int(code[:-1], base=10)


def p21a(f: TextIO) -> int:
    return sum(calc_complexity(l.strip(), 3) for l in f)


def p21b(f: TextIO) -> int:
    return sum(calc_complexity(l.strip(), 26) for l in f)


if __name__ == "__main__":
    run_solution(p21a, p21b, 21)
