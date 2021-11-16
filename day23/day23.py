#!/usr/bin/env python3
#
#  Advent of Code 2020 - day 23
#
from pathlib import Path

INPUT = ("538914762", 100)

SAMPLE_CASES = [
    (("389125467", 10), "92658374"),
    (("389125467", 100), "67384529"),
]


# Solution

def to_str(cups):
    return ''.join([str(v) for v in cups])

def make_move(cups, curr):
    ncups = len(cups)
    icurr = cups.index(curr)
    
    istart, iend = (icurr + 1) % ncups , (icurr + 3) % ncups
    # print(f"ncup: {ncups}  curr: {curr}  icurr: {icurr}  cups: {to_str(cups)}")
    # print(f"istart: {istart}  iend: {iend}")
    if istart == 0:
        removed = cups[:iend+1]
        cups = cups[iend+1:]
    elif iend < istart:
        removed = cups[istart:] + cups[:iend+1]
        cups = cups[iend+1:istart]
    else:
        removed = cups[istart:iend+1]
        cups = cups[:istart] + cups[iend+1:]

    # print(f"cups: {to_str(cups)}  removed: {to_str(removed)}")

    dest = curr - 1
    while dest and dest not in cups:
        dest -= 1
    if not dest:
        dest = max(cups)
    idest = cups.index(dest) + 1

    # print(f"dest: {dest}  idest: {idest}")
    # print(f"{to_str(cups[:idest])} {to_str(removed)} {to_str(cups[idest:])}")
    cups = cups[:idest] + removed + cups[idest:]
    icurr = (cups.index(curr) + 1) % ncups
    curr = cups[icurr]

    # print(f"cups: {to_str(cups)}  icurr: {icurr}  curr: {curr}")
    return cups, curr

def play_game(cups, moves):
    curr = cups[0]
    ncup = len(cups)
    for move in range(moves):
        cups, curr = make_move(cups, curr)
        icurr = cups.index(curr)
        idx = cups.index(1)
        start, end = max(icurr-5, 0), min(icurr+5, ncup-1)
        result = " ".join([str(cups[i]) for i in range(start, end+1)]) 
        start2, end2 = max(idx-5, 0), min(idx+5, ncup-1)
        final = " ".join([str(cups[i]) for i in range(start2, end2+1)]) 
        print(f"move: {move:5d}  curr: {curr:4d}  icurr: {cups.index(curr):4d}  idx:
                {idx:4d}  cups[{start}:{end+1}]: {result}  cups[{start2}:{end2+1}]: {final}")
    return cups

def solve(labels, moves):
    """Solve the problem."""
    cups = [int(v) for v in labels]
    final = play_game(cups, moves)
    idx = final.index(1)
    ncup = len(labels)
    result = "".join([str(final[(idx + 1 + i) % ncup]) for i in range(ncup - 1)]) 
    return result

def solve2(labels, moves):
    """Solve the problem."""
    cups = [int(v) for v in labels] + list(range(10, 10001))
    assert len(cups) == 10000
    assert 10 in cups
    final = play_game(cups, 100000)
    idx = final.index(1)
    result = cups[idx+1] * cups[idx+2]
    return result


# PART 1

def example1():
    """Run example for problem with input arguments."""
    print("EXAMPLE 1:")
    for arg, expected in SAMPLE_CASES:
        result = solve(*arg)
        print(f"'{arg}' -> {result} (expected {expected})")
        assert result == expected
    print("= " * 32)

def part1():
    print("PART 1:")
    result = solve(*INPUT)
    print(f"result is {result}")
    print("= " * 32)


# PART 2

def example2():
    """Run example for problem with input arguments."""
    print("EXAMPLE 2:")
    arg, _ = SAMPLE_CASES[0]
    result = solve2(arg[0], 1000)
    expected = 149245887792
    print(f"'{arg}' -> {result} (expected {expected})")
    assert result == expected
    print("= " * 32)

def part1():
    print("PART 1:")
    result = solve(*INPUT)
    print(f"result is {result}")
    print("= " * 32)



if __name__ == "__main__":
    example1()
    part1()
    example2()
    part2()
