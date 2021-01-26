#!/usr/bin/env python3
#
#  Advent of Code 2020 - day 3
#
from pathlib import Path

INPUTFILE = 'input.txt'

SAMPLE_LINES = """
..##.......
#...#...#..
.#....#..#.
..#.#...#.#
.#...##..#.
..#.##.....
.#.#.#....#
.#........#
#.##...#...
#...##....#
.#..#...#.#
""".split("\n")

TREE = "#"

def sample_input():
    return list(filter_blank_lines(SAMPLE_LINES))

# Utility functions

def load_input(infile):
    return list(filter_blank_lines(Path(infile).open()))

def filter_blank_lines(lines):
    for line in lines:
        line = line.strip()
        if line:
            yield line

# Solution

def solve(lines, slope):
    """Solve the problem."""
    dcol, drow = slope
    ncol = len(lines[0])
    row, col = 0, 0
    trees = 0
    while row < len(lines):
        print(f"({row}, {col}): '{lines[row][col]}'")
        if lines[row][col] == TREE:
            trees += 1
        row, col = row + drow, (col + dcol) % ncol
    return trees

def solve2(lines, slopes):
    """Solve the problem."""
    result = 1
    for slope in slopes:
        result *= solve(lines, slope)
    return result


# PART 1

def lines_example():
    lines = sample_input()
    slope = 3, 1
    expected = 7
    result = solve(lines, slope)
    print(f"'sample-input' -> {result} (expected {expected})")
    assert result == expected
    print('= ' * 32)

example = lines_example

def part1(lines):
    slope = 3, 1
    result = solve(lines, slope)
    print("result is {}".format(result))
    print('= ' * 32)


# PART 2

def lines_example2():
    lines = sample_input()
    slopes = [(1, 1), (3, 1), (5, 1), (7, 1), (1, 2)]
    expected = 336
    result = solve2(lines, slopes)
    print(f"'sample-input' -> {result} (expected {expected})")
    assert result == expected
    print('= ' * 32)

example2 = lines_example2

def part2(lines):
    slopes = [(1, 1), (3, 1), (5, 1), (7, 1), (1, 2)]
    result = solve2(lines, slopes)
    print("result is {}".format(result))
    print('= ' * 32)

if __name__ == '__main__':
    example()
    lines = load_input(INPUTFILE)
    part1(lines)
    example2()
    part2(lines)
