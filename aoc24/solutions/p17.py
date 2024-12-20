import re
from typing import TextIO, Callable
from aoc24.helpers.main import run_solution


Registers = dict[str, int]


def combo_op(operand: int, registers: Registers) -> int:
    assert operand != 7
    return operand_table.get(operand, lambda r: operand)(registers)


def div(operand: int, registers: Registers, register: str) -> None:
    registers[register] = registers["A"] // (2 ** combo_op(operand, registers))


def bxl(operand: int, registers: Registers) -> None:
    registers["B"] = registers["B"] ^ operand


def bst(operand: int, registers: Registers) -> None:
    registers["B"] = combo_op(operand, registers) % 8


def jnz(operand: int, registers: Registers) -> None:
    if registers["A"] == 0:
        return
    # subtract additional 2 as it'll be incremented after running the instruction
    registers["I"] = operand - 2


def bxc(operand: int, registers: Registers) -> None:
    registers["B"] = registers["B"] ^ registers["C"]


def out(operand: int, registers: Registers) -> int:
    return combo_op(operand, registers) % 8


instruction_table: dict[int, Callable[[int, Registers], int | None]] = {
    0: lambda o, r: div(o, r, "A"),
    1: bxl,
    2: bst,
    3: jnz,
    4: bxc,
    5: out,
    6: lambda o, r: div(o, r, "B"),
    7: lambda o, r: div(o, r, "C"),
}

operand_table: dict[int, Callable[[Registers], int]] = {
    4: lambda r: r["A"],
    5: lambda r: r["B"],
    6: lambda r: r["C"],
}


def run_program(registers: Registers, ps: str) -> list[int]:
    program = [int(i) for i in ps.split(",")]
    registers["I"] = 0
    all_output = []
    while registers["I"] < len(program):
        opcode = program[registers["I"]]
        operand = program[registers["I"] + 1]
        output = instruction_table[opcode](operand, registers)
        if output is not None:
            all_output.append(output)
        registers["I"] += 2
    return all_output


def p17a(f: TextIO) -> str:
    registers: Registers = {}
    for l in f:
        l = l.strip()
        if not l:
            break
        match = re.match(r"Register ([A-Z]): (\d+)", l)
        assert match and match.group(1) not in registers
        registers[match.group(1)] = int(match.group(2))

    output = run_program(registers, f.read().split(": ")[1])
    return ",".join(map(str, output))


def p17b(f: TextIO) -> str:
    return "1"


if __name__ == "__main__":
    run_solution(p17a, p17b, 17)
