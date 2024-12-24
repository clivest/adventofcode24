from typing import TextIO

from aoc24.helpers.main import run_solution


def p24a(f: TextIO) -> int:
    wires: dict[str, int] = {}
    for l in f:
        if not l.strip():
            break
        i, v = l.strip().split(": ")
        wires[i] = v == "1"
    gates = []
    for l in f:
        g, o = l.strip().split(" -> ")
        i0, op, i1 = g.split()
        gates.append((i0, i1, op, o))
    ops = {
        "AND": lambda a, b: a and b,
        "OR": lambda a, b: a or b,
        "XOR": lambda a, b: a != b,
    }
    while gates:
        gates_next = []
        for i0, i1, op, o in gates:
            if i0 not in wires or i1 not in wires:
                gates_next.append((i0, i1, op, o))
                continue
            wires[o] = ops[op](wires[i0], wires[i1])
        gates = gates_next
    zs = {int(w[1:], base=10): v for w, v in wires.items() if w.startswith("z")}
    z = 0
    for _, zv in sorted(zs.items(), reverse=True):
        z = (z << 1) + zv
    print(z)
    return z


def p24b(f: TextIO) -> int:
    return 1


if __name__ == "__main__":
    run_solution(p24a, p24b, 24)
