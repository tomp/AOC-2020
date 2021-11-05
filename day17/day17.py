#!/usr/bin/env python3
#
#  Advent of Code 2020 - day 17
#
from pathlib import Path
from collections import defaultdict

INPUTFILE = "input.txt"

SAMPLE_INPUT = """
.#.
..#
###
"""

NEIGHBORS = [
    (0, 0, -1),
    (0, 0, 1),

    (0, -1, 0),
    (0, -1, -1),
    (0, -1, 1),

    (0, 1, 0),
    (0, 1, -1),
    (0, 1, 1),

    (-1, 0, 0),
    (-1, 0, -1),
    (-1, 0, 1),

    (-1, -1, 0),
    (-1, -1, -1),
    (-1, -1, 1),

    (-1, 1, 0),
    (-1, 1, -1),
    (-1, 1, 1),

    (1, 0, 0),
    (1, 0, -1),
    (1, 0, 1),

    (1, -1, 0),
    (1, -1, -1),
    (1, -1, 1),

    (1, 1, 0),
    (1, 1, -1),
    (1, 1, 1),
]

NEIGHBORS4 = [
    (0, 0, -1, 0),
    (0, 0, 1, 0),

    (0, -1, 0, 0),
    (0, -1, -1, 0),
    (0, -1, 1, 0),

    (0, 1, 0, 0),
    (0, 1, -1, 0),
    (0, 1, 1, 0),

    (-1, 0, 0, 0),
    (-1, 0, -1, 0),
    (-1, 0, 1, 0),

    (-1, -1, 0, 0),
    (-1, -1, -1, 0),
    (-1, -1, 1, 0),

    (-1, 1, 0, 0),
    (-1, 1, -1, 0),
    (-1, 1, 1, 0),

    (1, 0, 0, 0),
    (1, 0, -1, 0),
    (1, 0, 1, 0),

    (1, -1, 0, 0),
    (1, -1, -1, 0),
    (1, -1, 1, 0),

    (1, 1, 0, 0),
    (1, 1, -1, 0),
    (1, 1, 1, 0),

    (0, 0, 0, -1),
    (0, 0, -1, -1),
    (0, 0, 1, -1),

    (0, -1, 0, -1),
    (0, -1, -1, -1),
    (0, -1, 1, -1),

    (0, 1, 0, -1),
    (0, 1, -1, -1),
    (0, 1, 1, -1),

    (-1, 0, 0, -1),
    (-1, 0, -1, -1),
    (-1, 0, 1, -1),

    (-1, -1, 0, -1),
    (-1, -1, -1, -1),
    (-1, -1, 1, -1),

    (-1, 1, 0, -1),
    (-1, 1, -1, -1),
    (-1, 1, 1, -1),

    (1, 0, 0, -1),
    (1, 0, -1, -1),
    (1, 0, 1, -1),

    (1, -1, 0, -1),
    (1, -1, -1, -1),
    (1, -1, 1, -1),

    (1, 1, 0, -1),
    (1, 1, -1, -1),
    (1, 1, 1, -1),

    (0, 0, 0, 1),
    (0, 0, -1, 1),
    (0, 0, 1, 1),

    (0, -1, 0, 1),
    (0, -1, -1, 1),
    (0, -1, 1, 1),

    (0, 1, 0, 1),
    (0, 1, -1, 1),
    (0, 1, 1, 1),

    (-1, 0, 0, 1),
    (-1, 0, -1, 1),
    (-1, 0, 1, 1),

    (-1, -1, 0, 1),
    (-1, -1, -1, 1),
    (-1, -1, 1, 1),

    (-1, 1, 0, 1),
    (-1, 1, -1, 1),
    (-1, 1, 1, 1),

    (1, 0, 0, 1),
    (1, 0, -1, 1),
    (1, 0, 1, 1),

    (1, -1, 0, 1),
    (1, -1, -1, 1),
    (1, -1, 1, 1),

    (1, 1, 0, 1),
    (1, 1, -1, 1),
    (1, 1, 1, 1),
]

def sample_input():
    return filter_blank_lines(SAMPLE_INPUT.split("\n"))


# Utility functions

def load_input(infile):
    return filter_blank_lines(Path(infile).open())

def filter_blank_lines(lines):
    return [line.strip() for line in lines if line.strip()]


# Solution

def neighbors(grid, xyz):
    """Return the number of active neghbors for cel xyz on the given grid.
    grid is a dict mapping coordinates to 0 (inactive) or 1 (active).
    xyz is a list or tuple of three integer coordinates.
    """
    x, y, z = xyz
    result = 0
    for dx, dy, dz in NEIGHBORS:
        if grid[(x+dx, y+dy, z+dz)]:
            result += 1
    return result

def parse_input(lines):
    grid = defaultdict(int)
    for r, row in enumerate(lines):
        for c, ch in enumerate(row):
            if ch == "#":
                grid[(c, -r, 0)] = 1
    return grid

def bounds(grid):
    """Return a list of tuples reporting the min and max value of each coordinate
    in the given grid.
    """
    xmin, ymin, zmin = list(grid.keys())[0]
    xmax, ymax, zmax = xmin, ymin, zmin 
    for x, y, z in grid:
        xmin = min(xmin, x)
        ymin = min(ymin, y)
        zmin = min(zmin, z)
        xmax = max(xmax, x)
        ymax = max(ymax, y)
        zmax = max(zmax, z)
    return [(xmin, xmax), (ymin, ymax), (zmin, zmax)]

def print_grid(grid):
    (xmin, xmax), (ymin, ymax), (zmin, zmax) = bounds(grid)
    for z in range(zmin, zmax+1):
        print(f"z={z}")
        for y in range(ymax, ymin-1, -1):
            row = ["#" if grid[(x, y, z)] else "." for x in range(xmin, xmax+1)]
            print("".join(row))
        print()

def propagate(grid):
    """Propagate the given grid for a single cycle.
    The propagated grid is returned.  (The input grid is untouched.)
    """
    result = defaultdict(int)
    (xmin, xmax), (ymin, ymax), (zmin, zmax) = bounds(grid)
    for x in range(xmin-1, xmax+2):
        for y in range(ymin-1, ymax+2):
            for z in range(zmin-1, zmax+2):
                state = grid[(x, y, z)]
                n = neighbors(grid, (x, y, z))
                if state == 1 and (n == 2 or n == 3):
                    result[(x, y, z)] = 1
                elif state == 0 and n == 3:
                    result[(x, y, z)] = 1
    return result

def solve(lines):
    """Solve the problem."""
    grid = parse_input(lines)
    print("Before any cycles:")
    print_grid(grid)

    for iter in range(1, 7):
        print()
        grid = propagate(grid)
        print(f"After {iter} cycles:")
        print()
        print_grid(grid)

    return sum(grid.values())


# Part 2 code

def neighbors4(grid, xyzw):
    """Return the number of active neghbors for cel xyz on the given grid.
    grid is a dict mapping coordinates to 0 (inactive) or 1 (active).
    xyz is a list or tuple of three integer coordinates.
    """
    x, y, z, w = xyzw
    result = 0
    for dx, dy, dz, dw in NEIGHBORS4:
        if grid[(x+dx, y+dy, z+dz, w+dw)]:
            result += 1
    return result

def parse_input4(lines):
    grid = defaultdict(int)
    for r, row in enumerate(lines):
        for c, ch in enumerate(row):
            if ch == "#":
                grid[(c, -r, 0, 0)] = 1
    return grid

def bounds4(grid):
    """Return a list of tuples reporting the min and max value of each coordinate
    in the given grid.
    """
    xmin, ymin, zmin, wmin = list(grid.keys())[0]
    xmax, ymax, zmax, wmax = xmin, ymin, zmin, wmin
    for x, y, z, w in grid:
        xmin = min(xmin, x)
        ymin = min(ymin, y)
        zmin = min(zmin, z)
        wmin = min(wmin, w)
        xmax = max(xmax, x)
        ymax = max(ymax, y)
        zmax = max(zmax, z)
        wmax = max(wmax, w)
    return [(xmin, xmax), (ymin, ymax), (zmin, zmax), (wmin, wmax)]

def print_grid4(grid):
    (xmin, xmax), (ymin, ymax), (zmin, zmax), (wmin, wmax) = bounds4(grid)
    for w in range(wmin, wmax+1):
        for z in range(zmin, zmax+1):
            print(f"z={z}, w={w}")
            for y in range(ymax, ymin-1, -1):
                row = ["#" if grid[(x, y, z, w)] else "." for x in range(xmin, xmax+1)]
                print("".join(row))
            print()

def propagate4(grid):
    """Propagate the given grid for a single cycle.
    The propagated grid is returned.  (The input grid is untouched.)
    """
    result = defaultdict(int)
    (xmin, xmax), (ymin, ymax), (zmin, zmax), (wmin, wmax) = bounds4(grid)
    for x in range(xmin-1, xmax+2):
        for y in range(ymin-1, ymax+2):
            for z in range(zmin-1, zmax+2):
                for w in range(wmin-1, wmax+2):
                    state = grid[(x, y, z, w)]
                    n = neighbors4(grid, (x, y, z, w))
                    if state == 1 and (n == 2 or n == 3):
                        result[(x, y, z, w)] = 1
                    elif state == 0 and n == 3:
                        result[(x, y, z, w)] = 1
    return result

def solve2(lines):
    """Solve the problem."""
    grid = parse_input4(lines)
    print("Before any cycles:")
    print_grid4(grid)

    for iter in range(1, 7):
        print()
        grid = propagate4(grid)
        print(f"After {iter} cycles:")
        print()
        print_grid4(grid)

    return sum(grid.values())

# PART 1

def example1():
    """Run example for problem with input lines."""
    lines = sample_input()
    result = solve(lines)
    expected = 112
    print(f"'sample-input' -> {result} (expected {expected})")
    assert result == expected
    print("= " * 32)


def part1(lines):
    result = solve(lines)
    print(f"result is {result}")
    print("= " * 32)


# PART 2

def example2():
    """Run example for problem with input lines."""
    lines = sample_input()
    result = solve2(lines)
    expected = 848
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
