from itertools import combinations
from typing import TextIO, cast

from aoc24.helpers.main import run_solution


Connected3 = tuple[str, str, str]
ConnectedSets = dict[str, set[tuple[str, ...]]]


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
    connections = load_connections(f)
    # the largest set must contain the historian (i.e. contain a node starting with t)
    # for subsequent iterations, the connected set key will be the first element in the connected set (sorted
    # alphabetically)
    connected_sets: ConnectedSets = {
        k: {(vi,) for vi in v} for k, v in connections.items() if k.startswith("t")
    }
    while True:
        connected_sets_next: ConnectedSets = {}
        for node in connected_sets:
            # look at all possible parings of groups that contain `node`. Find ones with a difference of 1 and where
            # there's a connection between the 2 differing elements
            for others in combinations(connected_sets[node], 2):
                a = [n for n in others[0] if n not in others[1]]
                if len(a) != 1:
                    continue
                b = [n for n in others[1] if n not in others[0]]
                assert len(b) == 1
                if b[0] in connections[a[0]]:
                    t = tuple(sorted((b[0], node) + others[0]))
                    connected_sets_next.setdefault(t[0], set()).add(t[1:])
        if not connected_sets_next:
            break
        connected_sets = connected_sets_next
    assert len(connected_sets) == 1
    k, grp = connected_sets.popitem()
    assert len(grp) == 1
    return ",".join((k,) + grp.pop())


if __name__ == "__main__":
    run_solution(p23a, p23b, 23)
