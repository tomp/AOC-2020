#!/usr/bin/env python3
#
#  Advent of Code 2020 - day 5
#
from pathlib import Path

INPUTFILE = "input.txt"


# Utility functions

def load_input(infile):
    return list(filter_blank_lines(Path(infile).open()))


def filter_blank_lines(lines):
    for line in lines:
        line = line.strip()
        if line:
            yield line


# Solution

def decode_pass(line):
    row = int(line[:7].replace('F', '0').replace('B', '1'), 2)
    seat = int(line[7:].replace('L', '0').replace('R', '1'), 2)
    return (row * 8) + seat


def solve(lines):
    """Solve the problem."""
    result = 0
    for line in lines:
        seat_id = decode_pass(line)
        result = max(result, seat_id)
    return result


def solve2(lines):
    """Solve the problem."""
    seat_ids = sorted([decode_pass(line) for line in lines])
    result = 0
    last_seat = 0
    for seat in seat_ids:
        if seat > last_seat + 1:
            result = seat - 1
        last_seat = seat
    return result


# PART 1


def arg_example():
    cases = [
       ("FBFBBFFRLR", 357),
       ("BFFFBBFRRR", 567),
       ("FFFBBBFRRR", 119),
       ("BBFFBBFRLL", 820),
    ]
    for arg, expected in cases:
        result = decode_pass(arg)
        print(f"'{arg}' -> {result} (expected {expected})")
        assert result == expected
    print("= " * 32)

example = arg_example


def part1(lines):
    result = solve(lines)
    print(f"result is {result}")
    print("= " * 32)


# PART 2


def part2(lines):
    result = solve2(lines)
    print(f"result is {result}")
    print("= " * 32)


if __name__ == "__main__":
    example()
    lines = load_input(INPUTFILE)
    part1(lines)
    part2(lines)
