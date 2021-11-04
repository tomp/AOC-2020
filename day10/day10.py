#!/usr/bin/env python3
#
#  Advent of Code 2020 - day 10
#
from pathlib import Path
from collections import Counter, defaultdict


INPUTFILE = "input.txt"

SAMPLE_INPUT = """
16
10
15
5
1
11
7
19
6
12
4
"""

SAMPLE_INPUT2 = """
28
33
18
42
31
14
46
20
48
47
24
23
49
45
19
38
39
11
1
32
25
35
8
17
7
9
4
2
34
10
3
"""


# Utility functions

def load_input(infile):
    return filter_blank_lines(Path(infile).open())


def filter_blank_lines(lines):
    return [line.strip() for line in lines if line.strip()]


# Solution


def solve(lines):
    """Solve the problem."""
    jolts = [0] + [int(line) for line in lines]
    jolts.sort()
    jolts.append(max(jolts) + 3)
    c = Counter([b-a for a, b in zip(jolts[:-1], jolts[1:])])
    return c[1] * c[3]


def solve2(lines):
    """Solve the problem."""
    jolts = [0] + [int(line) for line in lines]
    jolts.sort()

    count = defaultdict(int)
    count[max(jolts)] = 1

    for jolt in reversed(jolts):
        count[jolt] += count[jolt + 1] + count[jolt + 2] + count[jolt + 3]

    return count[0]


# PART 1

def example1():
    lines = filter_blank_lines(SAMPLE_INPUT.split("\n"))
    result = solve(lines)
    expected = 35
    print(f"'sample-input' -> {result} (expected {expected})")
    assert result == expected

    lines = filter_blank_lines(SAMPLE_INPUT2.split("\n"))
    result = solve(lines)
    expected = 220
    print(f"'sample-input2' -> {result} (expected {expected})")
    assert result == expected
    print("= " * 32)


def part1(lines):
    result = solve(lines)
    print(f"result is {result}")
    print("= " * 32)


# PART 2


def example2():
    lines = filter_blank_lines(SAMPLE_INPUT.split("\n"))
    result = solve2(lines)
    expected = 8
    print(f"'sample-input' -> {result} (expected {expected})")
    assert result == expected

    lines = filter_blank_lines(SAMPLE_INPUT2.split("\n"))
    result = solve2(lines)
    expected = 19208
    print(f"'sample-input2' -> {result} (expected {expected})")
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
