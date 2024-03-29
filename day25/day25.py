#!/usr/bin/env python3
#
#  Advent of Code 2020 - day 25
#
from pathlib import Path

INPUTFILE = "input.txt"

SAMPLE_INPUT = """
5764801
17807724
"""

# Utility functions

## Use these if blank lines should be discarded.
def sample_input():
    return filter_blank_lines(SAMPLE_INPUT.split("\n"))

def load_input(infile):
    return filter_blank_lines(Path(infile).open())

def filter_blank_lines(lines):
    return [line.strip() for line in lines if line.strip()]


# Solution

MODULUS = 20201227
SUBJECT = 7

def transform(subject, loop_size):
    """Tranform the subject number fllowing https://adventofcode.com/2020/day/25
    The integer result is returned.
    """
    result = 1
    for _ in range(loop_size):
        result = (result * subject) % MODULUS
    return result


def brute_force_loop_size(public_key):
    """Determine what loop_size transforms 7 to the given public_key.
    The integer loop size is returned.
    """
    key = 1
    count = 0
    for _ in range(MODULUS):
        count += 1
        key = (key * SUBJECT) % MODULUS
        if key == public_key:
            return count
    return None

def solve(lines):
    """Solve the problem."""
    card_key, door_key = [int(v) for v in lines]
    card_loop = brute_force_loop_size(card_key)
    return transform(door_key, card_loop)


# PART 1

#!! DELETE THE example1 FUNCTION YOU'RE NOT GOING TO USE

def example1():
    """Run example for problem with input arguments."""
    print("EXAMPLE 1:")
    for arg, expected in SAMPLE_CASES:
        result = solve(arg)
        print(f"'{arg}' -> {result} (expected {expected})")
        assert result == expected
    print("= " * 32)


def example1():
    """Run example for problem with input lines."""
    print("EXAMPLE 1:")
    lines = filter_blank_lines(SAMPLE_INPUT.split("\n"))
    result = solve(lines)
    expected = 14897079
    print(f"'sample-input' -> {result} (expected {expected})")
    assert result == expected
    print("= " * 32)


def part1(lines):
    print("PART 1:")
    result = solve(lines)
    print(f"result is {result}")
    print("= " * 32)


# PART 2



if __name__ == "__main__":
    example1()
    lines = load_input(INPUTFILE)
    part1(lines)
    # example2()
    # part2(lines)
