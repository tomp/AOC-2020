#!/usr/bin/env python3
#
#  Advent of Code 2020 - day 15
#
from pathlib import Path

INPUTFILE = "input.txt"

SAMPLE_INPUT = """
"""

def sample_input():
    return filter_blank_lines(SAMPLE_INPUT.split("\n"))


# Utility functions

def load_input(infile):
    return filter_blank_lines(Path(infile).open())

def filter_blank_lines(lines):
    return [line.strip() for line in lines if line.strip()]


# Solution

def solve(starters, turns=2020):
    """Solve the problem."""
    hist = dict()
    for turn, val in enumerate(starters):
        if val not in hist:
            nextval = 0
        else:
            nextval = turn + 1 - hist[val]
        hist[val] = turn + 1
        # print(f"{turn+1:04d}: {val:3d} ({nextval})")

    for turn in range(len(starters) + 1, turns + 1):
        val = nextval
        if val not in hist:
            nextval = 0
        else:
            nextval = turn - hist[val]
        hist[val] = turn
        # print(f"{turn:04d}: {val:3d}  {nextval}")
        lastval = val
    return lastval


# PART 1

def example1():
    """Run example for problem with input arguments."""
    cases = [
        ([0, 3, 6], 436),
        ([1, 3, 2], 1),
        ([2, 1, 3], 10),
        ([1, 2, 3], 27),
        ([2, 3, 1], 78),
        ([3, 2, 1], 438),
        ([3, 1, 2], 1836),
    ]
    for arg, expected in cases:
        result = solve(arg)
        print(f"'{arg}' -> {result} (expected {expected})")
        assert result == expected
    print("= " * 32)

def part1(lines):
    starters = [int(v) for v in lines[0].split(",")]
    print(f"input is {starters}")
    result = solve(starters)
    print(f"result is {result}")
    print("= " * 32)


# PART 2

def example2():
    """Run example for problem with input arguments."""
    cases = [
        ([0, 3, 6], 175594),
        ([1, 3, 2], 2578),
        ([2, 1, 3], 3544142),
        ([1, 2, 3], 261214),
        ([2, 3, 1], 6895259),
        ([3, 2, 1], 18),
        ([3, 1, 2], 362),
    ]
    for arg, expected in cases:
        result = solve(arg, 30000000)
        print(f"'{arg}' -> {result} (expected {expected})")
        assert result == expected
    print("= " * 32)

def part2(lines):
    starters = [int(v) for v in lines[0].split(",")]
    print(f"input is {starters}")
    result = solve(starters, 30000000)
    print(f"result is {result}")
    print("= " * 32)


if __name__ == "__main__":
    example1()
    lines = load_input(INPUTFILE)
    part1(lines)
    example2()
    part2(lines)
