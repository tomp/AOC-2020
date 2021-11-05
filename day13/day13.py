#!/usr/bin/env python3
#
#  Advent of Code 2020 - day 13
#
from pathlib import Path
import math

INPUTFILE = "input.txt"

SAMPLE_INPUT = """
939
7,13,x,x,59,x,31,19
"""


def sample_input():
    return filter_blank_lines(SAMPLE_INPUT.split("\n"))


# Utility functions

def load_input(infile):
    return filter_blank_lines(Path(infile).open())

def parse_input(lines):
    depart = int(lines[0])
    ids = [int(v) for v in lines[1].split(",") if v != "x"]
    return depart, ids

def parse_input2(lines):
    ids = [(int(v), pos) for pos, v in enumerate(lines[1].split(",")) if v != "x"]
    return ids

def filter_blank_lines(lines):
    return [line.strip() for line in lines if line.strip()]

# Solution

def crt(cong):
    """Use the Chinese Remainder THeorem to solve the given system of
    congruences, cong = [(mod1, rem1), (mod2, rem2), ...] where
    val = rem1 mod mod1
    val = rem2 mod mod2
    ...
    The val satisfying the congruences is returned.
    """
    result = 0
    nprod = math.prod([v[0] for v in cong])
    print(f"nprod = {nprod}")
    for n, b in cong:
        if b < 0:
            b += n
        if b == 0:
            continue
        ni = nprod // n
        d, x, y = ext_euclid(n, ni)
        # print(f"{ni} * {y} mod {n} = {(y * ni) % n}")
        result += b * (y % n) * ni
    return result % nprod

def ext_euclid(a, b):
    """Use extended Euclid algorithm to find gcd of a and b, along with
    the coefficients of Bezout's identity, a*x + b*y = gcd(a, b)
    The tuple(gcd(a, b), x, y) is returned.
    """
    assert a > 0 and b > 0
    reverse = b > a
    if reverse:
        r0, s0, t0 = b, 1, 0
        r1, s1, t1 = a, 0, 1
    else:
        r0, s0, t0 = a, 1, 0
        r1, s1, t1 = b, 0, 1
    while r1 > 0:
        q = r0 // r1
        r2, s2, t2 = r0 - q*r1, s0 - q*s1, t0 - q*t1
        r0, s0, t0 = r1, s1, t1
        r1, s1, t1 = r2, s2, t2
    if reverse:
        return r0, t0, s0
    return r0, s0, t0

def solve(lines):
    """Solve the problem."""
    depart, ids = parse_input(lines)
    print("earliest departure:", depart)
    print("bus ids:", ids)
    buses = []
    for bus_id in ids:
        last_bus = depart % bus_id
        if last_bus > 0:
            buses.append((bus_id - last_bus, bus_id))
        else:
            buses.append((0, bus_id))
    buses.sort()
    delay, bus_id = buses[0]
    return bus_id * delay

def solve2(lines):
    """Solve the problem."""
    ids = parse_input2(lines)
    print("bus ids and positions:", ids)
    cong = [(n, -pos) for n, pos in ids]
    result = crt(cong)
    return result

# PART 1

def example1():
    lines = sample_input()
    result = solve(lines)
    expected = 295
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
    expected = 1068781
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
