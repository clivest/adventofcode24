import re
from itertools import count
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


def load_registers(f: TextIO) -> Registers:
    registers: Registers = {}
    for l in f:
        l = l.strip()
        if not l:
            break
        match = re.match(r"Register ([A-Z]): (\d+)", l)
        assert match and match.group(1) not in registers
        registers[match.group(1)] = int(match.group(2))
    return registers


def p17a(f: TextIO) -> str:
    registers = load_registers(f)
    output = run_program(registers, f.read().split(": ")[1])
    return ",".join(map(str, output))


def find_a_for_output(
    a_start: int, registers: Registers, program: str, output: list[int]
) -> int:
    for a in count(a_start):
        registers = registers.copy() | {"A": a}
        if run_program(registers, program) == output:
            return a
    assert False


def p17b(f: TextIO) -> int:
    # Program:
    # 2,4 B = A % 8 (= A & 0b111)
    # 1,5 B = B XOR 0b101
    # 7,5 C = A // (2**B) (= A >> B)
    # 1,6 B = B XOR 0b110
    # 4,1 B = B XOR C
    # 5,5 out B % 8
    # 0,3 A = A//8 (= A >> 3)
    # 3,0 jump 0
    # Start from the back. Find A needed to output the final number, <<=3 to reverse the 0,3 instruction then find A
    # needed to output final 2 numbers. Repeat to find A needed to output all numbers
    registers = load_registers(f)
    program = f.read().split(": ")[1]
    required_output = [int(i) for i in program.split(",")]
    a = 0
    for pos in range(len(required_output)):
        a <<= 3
        a = find_a_for_output(a, registers, program, required_output[-pos - 1 :])
    return a


if __name__ == "__main__":
    run_solution(p17a, p17b, 17)
