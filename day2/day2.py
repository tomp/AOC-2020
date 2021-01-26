#!/usr/bin/env python3
#
#  Advent of Code 2020 - Day N
#
from pathlib import Path
from collections import Counter
import re

LINE_RE = re.compile(r"(\d+)-(\d+) (\w): (\w+)$")

INPUTFILE = 'input.txt'

def sample_input():
    return filter_blank_lines("""
1-3 a: abcde
1-3 b: cdefg
2-9 c: ccccccccc
""".split("\n"))

# Utility functions

def load_input(infile):
    return filter_blank_lines(Path(infile).open())

def filter_blank_lines(lines):
    for line in lines:
        line = line.strip()
        if line:
            yield line

# Solution

def is_valid(line: str) -> bool:
    m = LINE_RE.match(line)
    if m:
        lo, hi, ch, password = m.groups()
        c = Counter(password)
        return int(lo) <= c[ch] <= int(hi)
    

def is_valid2(line: str) -> bool:
    m = LINE_RE.match(line)
    if m:
        lo, hi, ch, password = m.groups()
        return (password[int(lo)-1] == ch) != (password[int(hi)-1] == ch)
    

def solve(lines, is_valid) -> int:
    """Solve the problem."""
    count = 0
    for line in lines:
        if is_valid(line):
            count += 1
    return count

# PART 1

def example():
    passwords = list(sample_input())
    expected = 2
    result = solve(passwords, is_valid)
    print("'sample-input' -> {} (expected {})".format(result, expected))
    assert result == expected
    print('= ' * 32)

def part1(lines):
    result = solve(lines, is_valid)
    print("result is {}".format(result))
    print('= ' * 32)


# PART 2

def example2():
    passwords = list(sample_input())
    expected = 1
    result = solve(passwords, is_valid2)
    print("'sample-input' -> {} (expected {})".format(result, expected))
    assert result == expected
    print('= ' * 32)

def part2(lines):
    result = solve(lines, is_valid2)
    print("result is {}".format(result))
    print('= ' * 32)

if __name__ == '__main__':
    example()
    lines = list(load_input(INPUTFILE))
    part1(lines)
    example2()
    part2(lines)
