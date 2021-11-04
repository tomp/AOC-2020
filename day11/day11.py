#!/usr/bin/env python3
#
#  Advent of Code 2020 - day 11
#
from pathlib import Path

INPUTFILE = "input.txt"

SAMPLE_INPUT = """
L.LL.LL.LL
LLLLLLL.LL
L.L.L..L..
LLLL.LL.LL
L.LL.LL.LL
L.LLLLL.LL
..L.L.....
LLLLLLLLLL
L.LLLLLL.L
L.LLLLL.LL
"""

WALL = "+"
FLOOR = "."
EMPTY = "L"
OCC = "#"

DIRS = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]


def sample_input():
    return filter_blank_lines(SAMPLE_INPUT.split("\n"))


# Utility functions

def load_input(infile):
    return filter_blank_lines(Path(infile).open())


def filter_blank_lines(lines):
    return [line.strip() for line in lines if line.strip()]


# Solution

def load_seats(lines):
    """Return a matrix (list of lists) representing the seating area.
    A border of floor tiles is added, to make the logic for counting neighbors simpler.
    """
    rows, cols = len(lines) + 2, len(lines[0]) + 2
    result = [WALL * cols] + [WALL + row + WALL for row in lines] + [WALL * cols]
    return result

def count_occupied(seats):
    """Return the numer of occupied seats in the given seating chart."""
    result = 0
    for row in seats:
        result += row.count(OCC)
    return result

def propagate(seats):
    """Propagate the seating chart over one time period.
    The new seating chart is returned.
    """
    rows, cols = len(seats), len(seats[0])
    result = [WALL * cols]
    for r in range(1, rows - 1):
        row = [WALL]
        for c in range(1, cols - 1):
            current = seats[r][c]
            count = 0
            for dr, dc in DIRS:
                ir, ic = r + dr, c + dc
                if seats[ir][ic] == OCC:
                    count += 1
            if current == EMPTY and count == 0:
                row.append(OCC)
            elif current == OCC and count > 3:
                row.append(EMPTY)
            else:
                row.append(current)
        row.append(WALL)
        result.append("".join(row))
    result.append(WALL * cols)
    return result

def propagate2(seats):
    """Propagate the seating chart over one time period.
    The new seating chart is returned.
    """
    rows, cols = len(seats), len(seats[0])
    result = [WALL * cols]
    for r in range(1, rows - 1):
        row = [WALL]
        for c in range(1, cols - 1):
            current = seats[r][c]
            count = 0
            for dr, dc in DIRS:
                ir, ic = r + dr, c + dc
                while seats[ir][ic] == FLOOR:
                    ir, ic = ir + dr, ic + dc
                if seats[ir][ic] == OCC:
                    count += 1
            if current == EMPTY and count == 0:
                row.append(OCC)
            elif current == OCC and count > 4:
                row.append(EMPTY)
            else:
                row.append(current)
        row.append(WALL)
        result.append("".join(row))
    result.append(WALL * cols)
    return result

def same_seats(seats1, seats2):
    return all([row1 == row2 for row1, row2 in zip(seats1, seats2)])

def solve(lines, propagator):
    """Solve the problem."""
    seats = load_seats(lines)
    rows, cols = len(seats), len(seats[0])

    while True:
        old_seats = seats
        seats = propagator(old_seats)
        if same_seats(old_seats, seats):
            break

    print("\n".join(seats))
    print("-" * cols)
    return count_occupied(seats)


# PART 1


def example1():
    lines = sample_input()
    result = solve(lines, propagate)
    expected = 37
    print(f"'sample-input' -> {result} (expected {expected})")
    assert result == expected
    print("= " * 32)


def part1(lines):
    result = solve(lines, propagate)
    print(f"result is {result}")
    print("= " * 32)


# PART 2


def example2():
    lines = sample_input()
    result = solve(lines, propagate2)
    expected = 26
    print(f"'sample-input' -> {result} (expected {expected})")
    assert result == expected
    print("= " * 32)


def part2(lines):
    result = solve(lines, propagate2)
    print(f"result is {result}")
    print("= " * 32)


if __name__ == "__main__":
    example1()
    lines = load_input(INPUTFILE)
    part1(lines)
    example2()
    part2(lines)
