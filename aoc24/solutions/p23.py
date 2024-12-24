from itertools import combinations
from typing import TextIO, cast

from aoc24.helpers.main import run_solution


Connected3 = tuple[str, str, str]


def p23a(f: TextIO) -> int:
    connections: dict[str, set[str]] = {}
    for l in f:
        cs = l.strip().split("-")
        for c1, c2 in [cs, reversed(cs)]:
            connections.setdefault(c1, set()).add(c2)
    t_nodes: set[str] = {c for c in connections.keys() if c.startswith("t")}
    sets: set[Connected3] = set()
    for t_node in t_nodes:
        for others in combinations(connections[t_node], 2):
            if others[1] in connections[others[0]]:
                connected_set = cast(Connected3, tuple(sorted((t_node,) + others)))
                sets.add(connected_set)
    return len(sets)


def p23b(f: TextIO) -> int:
    return 1


if __name__ == "__main__":
    run_solution(p23a, p23b, 23)
