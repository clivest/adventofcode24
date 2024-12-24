from itertools import combinations
from typing import TextIO, cast

from aoc24.helpers.main import run_solution


Connected3 = tuple[str, str, str]


def load_connections(f: TextIO) -> dict[str, set[str]]:
    connections: dict[str, set[str]] = {}
    for l in f:
        cs = l.strip().split("-")
        for c1, c2 in [cs, reversed(cs)]:
            connections.setdefault(c1, set()).add(c2)
    return connections


def p23a(f: TextIO) -> int:
    connections = load_connections(f)
    t_nodes: set[str] = {c for c in connections.keys() if c.startswith("t")}
    sets: set[Connected3] = set()
    for t_node in t_nodes:
        for others in combinations(connections[t_node], 2):
            if others[1] in connections[others[0]]:
                connected_set = cast(Connected3, tuple(sorted((t_node,) + others)))
                sets.add(connected_set)
    return len(sets)


def p23b(f: TextIO) -> str:
    connections: list[dict[str, set[tuple[str, ...]]]] = [
        {k: {(vi,) for vi in v} for k, v in load_connections(f).items()}
    ]
    while True:
        print(len(connections), len(connections[-1]))
        cons: dict[str, set[tuple[str, ...]]] = {}
        for node in connections[-1]:
            for others in combinations(connections[-1][node], 2):
                s0, s1 = (set(s) for s in others)
                if len(s0 - s1) != 1:
                    continue
                a, b = (s0 - s1).pop(), (s1 - s0).pop()
                if (b,) in connections[0][a]:
                    t = tuple(sorted((b, node) + others[0]))
                    cons.setdefault(t[0], set()).add(t[1:])
        if not cons:
            break
        connections.append(cons)
    assert len(connections[-1]) == 1
    k, grp = connections[-1].popitem()
    assert len(grp) == 1
    code = ",".join((k,) + grp.pop())
    return code


if __name__ == "__main__":
    run_solution(p23a, p23b, 23)
