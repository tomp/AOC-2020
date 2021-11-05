#!/usr/bin/env python3
#
#  Advent of Code 2020 - day 14
#
from pathlib import Path
import re

INPUTFILE = "input.txt"

SAMPLE_INPUT = """
mask = XXXXXXXXXXXXXXXXXXXXXXXXXXXXX1XXXX0X
mem[8] = 11
mem[7] = 101
mem[8] = 0
"""

SAMPLE_INPUT2 = """
mask = 000000000000000000000000000000X1001X
mem[42] = 100
mask = 00000000000000000000000000000000X0XX
mem[26] = 1
"""

MASK_RE = re.compile(r"mask = ([X01]{36})")
MEM_RE = re.compile(r"mem\[(\d+)\] = (\d+)")


def sample_input():
    return filter_blank_lines(SAMPLE_INPUT.split("\n"))

def sample_input2():
    return filter_blank_lines(SAMPLE_INPUT2.split("\n"))


# Utility functions

def load_input(infile):
    return filter_blank_lines(Path(infile).open())

def filter_blank_lines(lines):
    return [line.strip() for line in lines if line.strip()]


# Solution

def apply_val_mask(mask, val):
    inbits = bin(val)[2:]
    size = len(inbits)
    inbits = "0" * (len(mask) - size) + inbits
    outbits = []
    for maskbit, valbit in zip(mask, inbits):
        if maskbit == "X":
            outbits.append(valbit)
        else:
            outbits.append(maskbit)
    return int("".join(outbits), 2)

def solve(lines):
    """Solve the problem."""
    mem = dict()
    mask = "X" * 36
    for line in lines:
        if line.startswith("mem"):
            m = MEM_RE.match(line)
            loc, val = [int(v) for v in m.groups()]
            mem[loc] = apply_val_mask(mask, val)
        elif line.startswith("mask"):
            m = MASK_RE.match(line)
            mask = m.group(1)
    return sum(mem.values())

def locations(ch, text):
    return [i for i, v in enumerate(text) if v == ch]

def apply_mem_mask(mask, addr):
    addrbits = bin(addr)[2:]
    size = len(addrbits)
    addrbits = "0" * (len(mask) - size) + addrbits
    membits = []
    for maskbit, addrbit in zip(mask, addrbits):
        if maskbit == "0":
            membits.append(addrbit)
        else:
            membits.append(maskbit)

    nfloat = membits.count("X")
    if not nfloat:
        return [int("".join(membits), 2)]

    result = []
    locs = locations("X", membits)
    for i in range(pow(2, nfloat)):
        floatbits = (("0" * nfloat) + bin(i)[2:])[-nfloat:]
        outbits = membits
        for i, v in zip(locs, floatbits):
            outbits[i] = v
        result.append(int("".join(outbits), 2))
    return result

def solve2(lines):
    """Solve the problem."""
    mem = dict()
    mask = "0" * 36
    for line in lines:
        if line.startswith("mem"):
            m = MEM_RE.match(line)
            loc, val = [int(v) for v in m.groups()]
            for floatloc in apply_mem_mask(mask, loc):
                mem[floatloc] = val
        elif line.startswith("mask"):
            m = MASK_RE.match(line)
            mask = m.group(1)
    return sum(mem.values())


# PART 1

def example1():
    lines = sample_input()
    result = solve(lines)
    expected = 165
    print(f"'sample-input' -> {result} (expected {expected})")
    assert result == expected
    print("= " * 32)

def part1(lines):
    result = solve(lines)
    print(f"result is {result}")
    print("= " * 32)


# PART 2

def example2():
    lines = sample_input2()
    result = solve2(lines)
    expected = 208
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
