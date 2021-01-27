#!/usr/bin/env python3
#
#  Advent of Code 2020 - Day N
#
from pathlib import Path

INPUTFILE = "input.txt"


def sample_input():
    return ""


# Utility functions


def load_input(infile):
    return list(filter_blank_lines(Path(infile).open()))


def filter_blank_lines(lines):
    for line in lines:
        line = line.strip()
        if line:
            yield line


# Solution


def solve(arg):
    """Solve the problem."""
    pass


# PART 1


def arg_example():
    cases = [("arg1", "expected1"), ("arg2", "expected2")]
    for arg, expected in cases:
        result = solve(arg)
        print(f"'{arg}' -> {result} (expected {expected})")
        assert result == expected
    print("= " * 32)


def lines_example():
    lines = sample_input()
    result = solve(lines)
    print(f"'sample-input' -> {result} (expected {expected})")
    assert result == expected
    print("= " * 32)


example = lines_example


def part1(lines):
    result = solve(lines)
    print(f"result is {result}")
    print("= " * 32)


# PART 2


def example2():
    pass


def part2(lines):
    pass


if __name__ == "__main__":
    example()
    # lines = load_input(INPUTFILE)
    # part1(lines)
    # example2()
    # part2(lines)
