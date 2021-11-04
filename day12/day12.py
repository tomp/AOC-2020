#!/usr/bin/env python3
#
#  Advent of Code 2020 - day 12
#
from pathlib import Path

INPUTFILE = "input.txt"

SAMPLE_INPUT = """
F10
N3
F7
R90
F11
"""


def sample_input():
    return filter_blank_lines(SAMPLE_INPUT.split("\n"))


# Utility functions

def load_input(infile):
    return filter_blank_lines(Path(infile).open())


def filter_blank_lines(lines):
    return [line.strip() for line in lines if line.strip()]


# Solution

def solve(lines):
    """Solve the problem."""
    px, py = 0, 0
    dx, dy = 1, 0
    for item in lines:
        cmd, val = item[0], int(item[1:])
        if cmd == "F":
            px += val * dx
            py += val * dy
        elif cmd == "N":
            py += val
        elif cmd == "E":
            px += val
        elif cmd == "S":
            py -= val
        elif cmd == "W":
            px -= val
        elif cmd == "R":
            if val == 90:
                dx, dy = dy, -dx 
            elif val == 180:
                dx, dy = -dx, -dy
            elif val == 270:
                dx, dy = -dy, dx 
            else:
                raise ValueError(f"cannot turn {cmd}{val}")
        elif cmd == "L":
            if val == 270:
                dx, dy = dy, -dx 
            elif val == 180:
                dx, dy = -dx, -dy
            elif val == 90:
                dx, dy = -dy, dx 
            else:
                raise ValueError(f"cannot turn {cmd}{val}")
    return abs(px) + abs(py)


def solve2(lines):
    """Solve the problem."""
    px, py = 0, 0
    wx, wy = 10, 1
    for item in lines:
        cmd, val = item[0], int(item[1:])
        if cmd == "F":
            px += val * wx
            py += val * wy
        elif cmd == "N":
            wy += val
        elif cmd == "E":
            wx += val
        elif cmd == "S":
            wy -= val
        elif cmd == "W":
            wx -= val
        elif cmd == "R":
            if val == 90:
                wx, wy = wy, -wx 
            elif val == 180:
                wx, wy = -wx, -wy
            elif val == 270:
                wx, wy = -wy, wx 
            else:
                raise ValueError(f"cannot turn {cmd}{val}")
        elif cmd == "L":
            if val == 270:
                wx, wy = wy, -wx 
            elif val == 180:
                wx, wy = -wx, -wy
            elif val == 90:
                wx, wy = -wy, wx 
            else:
                raise ValueError(f"cannot turn {cmd}{val}")
    return abs(px) + abs(py)


# PART 1

def example1():
    lines = sample_input()
    result = solve(lines)
    expected = 25
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
    expected = 286
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
