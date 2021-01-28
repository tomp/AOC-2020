#!/usr/bin/env python3
#
#  Advent of Code 2020 - day 8
#
from pathlib import Path
import re

INPUTFILE = "input.txt"


SAMPLE_INPUT = """
nop +0
acc +1
jmp +4
acc +3
jmp -3
acc -99
acc +1
jmp -4
acc +6
"""

def sample_input():
    return filter_blank_lines(SAMPLE_INPUT.split("\n"))


# Utility functions


def load_input(infile):
    return list(filter_blank_lines(Path(infile).open()))


def filter_blank_lines(lines):
    return [line.strip() for line in lines if line.strip()]


# Solution

INS_RE = re.compile(r"(nop|acc|jmp) ([+-]\d+)$")

ACC = "acc"
JMP = "jmp"
NOP = "nop"

def parse_program(lines):
    prog = list()
    pc = 0
    for line in lines:
        line = line.strip()
        if not line:
            continue
        m = INS_RE.match(line)
        ins, val = m.groups()
        prog.append((ins, int(val)))
        pc += 1
    return prog


def execute_program(prog, pc=0, acc=0):
    """Execute the given program starting at the given program counter,
    with the given initial accumulator value.  The program will run until
    it exits, or an instruction is executed a second time.  The final
    program counter and accumulator values are returned.
    """
    seen = set()
    while pc not in seen:
        seen.add(pc)
        ins, val = prog[pc]
        if ins == ACC:
            acc += val
            pc += 1
        elif ins == JMP:
            pc += val
        else:
            pc += 1
        if pc < 0 or pc >= len(prog):
            break
    success = (pc == len(prog))
    return success, pc, acc

def solve(lines):
    """Solve the problem."""
    prog = parse_program(lines)
    print(f"Loaded {len(prog)}-line program")
    success, pc, acc = execute_program(prog)
    return acc

def solve2(lines):
    """Solve the problem."""
    prog = parse_program(lines)
    idx = 0
    print(f"Loaded {len(prog)}-line program")
    success, pc, acc = execute_program(prog)
    while not success:
        ins, val = prog[idx]
        alt_prog = prog.copy()
        if ins == JMP:
            alt_prog[idx] = (NOP, val)
        elif ins == NOP and val != 0:
            alt_prog[idx] = (JMP, val)
        else:
            idx += 1
            continue
        success, pc, acc = execute_program(alt_prog)
        idx += 1
    return acc


# PART 1


def example1():
    lines = sample_input()
    result = solve(lines)
    expected = 5
    print(f"'sample-input' -> {result} (expected {expected})")
    assert result == expected
    print("= " * 32)


def part1(lines):
    result = solve(lines)
    print(f"result is {result}")
    print("= " * 32)


# PART 2


def example2():
    lines = sample_input()
    result = solve2(lines)
    expected = 8
    print(f"'sample-input' -> {result} (expected {expected})")
    assert result == expected
    print("= " * 32)


def part2(lines):
    result = solve2(lines)
    print(f"result is {result}")
    print("= " * 32)


if __name__ == "__main__":
    example1()
    lines = load_input(INPUTFILE)
    part1(lines)
    example2()
    part2(lines)
