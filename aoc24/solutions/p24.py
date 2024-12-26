from typing import TextIO

from aoc24.helpers.main import run_solution


Wires = dict[str, bool]
Gates = list[tuple[str, str, str, str]]


def read_input(f: TextIO) -> tuple[Wires, Gates]:
    wires: Wires = {}
    for l in f:
        if not l.strip():
            break
        i, v = l.strip().split(": ")
        wires[i] = v == "1"
    gates: Gates = []
    for l in f:
        g, o = l.strip().split(" -> ")
        i0, op, i1 = g.split()
        gates.append((i0, i1, op, o))
    return wires, gates


def set_wires(x: int, y: int, bits: int) -> Wires:
    wires: Wires = {}
    for i in range(bits):
        wires[f"x{i:02}"] = bool(x & (1 << i))
        wires[f"y{i:02}"] = bool(y & (1 << i))
    return wires


def run_system(
    wires: Wires, gates: Gates, swaps_l: list[tuple[str, str]] | None = None
) -> int:
    ops = {
        "AND": lambda a, b: a and b,
        "OR": lambda a, b: a or b,
        "XOR": lambda a, b: a != b,
    }
    swaps = ({a: b for a, b in swaps_l} | {b: a for a, b in swaps_l}) if swaps_l else {}
    while gates:
        gates_next = []
        for i0, i1, op, o in gates:
            if i0 not in wires or i1 not in wires:
                gates_next.append((i0, i1, op, o))
                continue
            wires[swaps.get(o, o)] = ops[op](wires[i0], wires[i1])
        gates = gates_next
    zs = {int(w[1:], base=10): v for w, v in wires.items() if w.startswith("z")}
    z = 0
    for _, zv in sorted(zs.items(), reverse=True):
        z = (z << 1) + zv
    return z


def p24a(f: TextIO) -> int:
    wires, gates = read_input(f)
    return run_system(wires, gates)


def p24b(f: TextIO) -> str:
    wires, gates = read_input(f)
    bits = len(wires) // 2
    # Solution determined using sample inputs below and ctrl+f around the input file to determine the fixes
    # Works only because the bugs are simple and easy to see. TODO: a generic solution!
    swaps = [("rts", "z07"), ("jpj", "z12"), ("kgj", "z26"), ("vvw", "chv")]
    err_count = 0
    # Check x+0 and y+0 to check operation with no carries
    for v in range(bits):
        for x, y in [(1 << v, 0), (0, 1 << v)]:
            wires = set_wires(x, y, bits)
            z = run_system(wires, gates, swaps)
            if z != 1 << v:
                print(v, x, y, z)
                err_count += 1
    # Check x+x to check carry operation
    for v in range(bits):
        wires = set_wires(1 << v, 1 << v, bits)
        z = run_system(wires, gates, swaps)
        if z != 1 << (v + 1):
            print(v, 1 << v, 1 << v, z)
            err_count += 1
    assert err_count == 0
    return ",".join(sorted(o for p in swaps for o in p))


if __name__ == "__main__":
    run_solution(p24a, p24b, 24)
