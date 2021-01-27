#!/usr/bin/env python3
#
#  Advent of Code 2020 - day 6
#
from pathlib import Path

INPUTFILE = "input.txt"

SAMPLE_TEXT = """
abc

a
b
c

ab
ac

a
a
a
a

b
"""


# Utility functions


def load_input(infile):
    return list(Path(infile).open())


# Solution


def parse_answers(lines):
    groups = []
    group = set()
    for line in lines:
        line = line.strip()
        if not line:
            if group:
                groups.append(group)
                group = set()
            continue
        group |= set(line)
    if group:
        groups.append(group)
    return groups


def parse_answers2(lines):
    groups = []
    group = set()
    bad_group = False
    for line in lines:
        line = line.strip()
        if not line:
            if group:
                groups.append(group)
                group = set()
            bad_group = False
            continue
        if bad_group:
            continue
        if not group:
            group = set(line)
        else:
            group &= set(line)
            if not group:
                bad_group = True
    if group:
        groups.append(group)
    return groups


def solve(lines):
    """Solve the problem."""
    result = 0
    for group in parse_answers(lines):
        result += len(group)
    return result


def solve2(lines):
    """Solve the problem."""
    result = 0
    for group in parse_answers2(lines):
        result += len(group)
    return result

# PART 1


def example1():
    lines = SAMPLE_TEXT.split("\n")
    result = solve(lines)
    expected = 11
    print(f"'sample-input' -> {result} (expected {expected})")
    assert result == expected
    print("= " * 32)


def part1(lines):
    result = solve(lines)
    print(f"result is {result}")
    print("= " * 32)


# PART 2

def example2():
    lines = SAMPLE_TEXT.split("\n")
    result = solve2(lines)
    expected = 6
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
