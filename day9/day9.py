#!/usr/bin/env python3
#
#  Advent of Code 2020 - day 9
#
from pathlib import Path
from itertools import combinations


INPUTFILE = "input.txt"


SAMPLE_INPUT = """
35
20
15
25
47
40
62
55
65
95
102
117
150
182
127
219
299
277
309
576
"""


def sample_input():
    return filter_blank_lines(SAMPLE_INPUT.split("\n"))


# Utility functions


def load_input(infile):
    return filter_blank_lines(Path(infile).open())


def filter_blank_lines(lines):
    return [line.strip() for line in lines if line.strip()]


# Solution

def not_sum(val, prev):
    for a, b in combinations(prev, 2):
        if a + b == val:
            return False
    return True

def solve(lines, prefix=25):
    """Solve the problem."""
    seq = [int(v) for v in lines]
    for idx in range(prefix, len(seq)):
        prev, val = seq[idx-prefix:idx], seq[idx]
        if not_sum(val, prev):
            return val
    return 0

def solve2(lines, target=0, prefix=25):
    """Solve the problem."""
    seq = [int(v) for v in lines]
    idx, size = 0, 3
    while idx + size <= len(seq):
        total = sum(seq[idx:idx+size])
        if total == target:
            return min(seq[idx:idx+size]) + max(seq[idx:idx+size])
        if total > target:
            idx += 1
            size -= 1
        elif total < target:
            size += 1
    return 0


# PART 1


def example1():
    lines = sample_input()
    result = solve(lines, prefix=5)
    expected = 127
    print(f"'sample-input' -> {result} (expected {expected})")
    assert result == expected
    print("= " * 32)


def part1(lines):
    result = solve(lines)
    print(f"result is {result}")
    print("= " * 32)
    return result


# PART 2


def example2():
    lines = sample_input()
    result = solve2(lines, target=127, prefix=5)
    expected = 62
    print(f"'sample-input' -> {result} (expected {expected})")
    assert result == expected
    print("= " * 32)


def part2(lines, target):
    result = solve2(lines, target)
    print(f"result is {result}")
    print("= " * 32)


if __name__ == "__main__":
    example1()
    lines = load_input(INPUTFILE)
    val = part1(lines)
    example2()
    part2(lines, target=val)
