#!/usr/bin/env python3
#
#  Advent of Code 2020 - Day N
#
from pathlib import Path
from itertools import combinations


INPUTFILE = 'input.txt'


def sample_input():
    return [1721, 979, 366, 299, 675, 1456]

# Utility functions

def load_input(infile):
    lines = []
    with Path(infile).open() as fp:
        for line in fp:
            line = line.strip()
            if line:
                lines.append(line)
        return lines

def split_nonblank_lines(text):
    lines = []
    for line in text.splitlines():
        line = line.strip()
        if line:
            lines.append(line)
    return lines

# Solution

def solve(numbers: list[int]) -> tuple:
    """Solve the problem."""
    for a, b in combinations(numbers, 2):
        if a + b == 2020:
            return a * b
    return 0

def solve2(numbers: list[int]) -> tuple:
    """Solve the problem."""
    for a, b, c in combinations(numbers, 3):
        if a + b + c == 2020:
            return a * b * c
    return 0

# PART 1

def example():
    items = sample_input()
    expected = 514579
    result = solve(items)
    print("part 1: 'sample-input' -> {} (expected {})".format(result, expected))
    assert result == expected

def part1(items):
    result = solve(items)
    print("result is {}".format(result))
    print('= ' * 32)


# PART 2

def example2():
    items = sample_input()
    expected = 241861950
    result = solve2(items)
    print("part 2: 'sample-input' -> {} (expected {})".format(result, expected))
    assert result == expected
    print('= ' * 32)

def part2(lines):
    result = solve2(items)
    print("result is {}".format(result))
    print('= ' * 32)

if __name__ == '__main__':
    example()
    items = [int(v) for v in load_input(INPUTFILE)]
    part1(items)
    example2()
    part2(items)
