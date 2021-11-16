#!/usr/bin/env python3
#
#  Advent of Code 2020 - day 24
#
from pathlib import Path
from collections import defaultdict

INPUTFILE = "input.txt"

SAMPLE_INPUT = """
sesenwnenenewseeswwswswwnenewsewsw
neeenesenwnwwswnenewnwwsewnenwseswesw
seswneswswsenwwnwse
nwnwneseeswswnenewneswwnewseswneseene
swweswneswnenwsewnwneneseenw
eesenwseswswnenwswnwnwsewwnwsene
sewnenenenesenwsewnenwwwse
wenwwweseeeweswwwnwwe
wsweesenenewnwwnwsenewsenwwsesesenwne
neeswseenwwswnwswswnw
nenwswwsewswnenenewsenwsenwnesesenew
enewnwewneswsewnwswenweswnenwsenwsw
sweneswneswneneenwnewenewwneswswnese
swwesenesewenwneswnwwneseswwne
enesenwswwswneneswsenwnewswseenwsese
wnwnesenesenenwwnenwsewesewsesesew
nenewswnwewswnenesenwnesewesw
eneswnwswnwsenenwnwnwwseeswneewsenese
neswnwewnwnwseenwseesewsenwsweewe
wseweeenwnesenwwwswnew
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

DIR = {
    "e":  (2, 0),
    "se": (1, -2),
    "sw": (-1, -2),
    "w":  (-2, 0),
    "nw": (-1, 2),
    "ne": (1, 2),
}

def follow_path(line):
    """Follow the path described by the input line, and return the coordinates
    (x, y) of the tile that path leads to.  Assume we always start at (0, 0).
    """
    x, y = 0, 0
    path = line
    while path:
        if path.startswith("n") or path.startswith("s"):
            dx, dy = DIR[path[:2]]
            path = path[2:]
        else:
            dx, dy = DIR[path[:1]]
            path = path[1:]
        x, y = x + dx, y + dy
    return x, y


def set_tiles(lines):
    """Flip the tiles specified by the input lines, to initiate the exhibit.
    A dict is returned that maps tile coords (x,y tuple) to a boolean,
    which is True if that tile is black.
    """
    tiles = defaultdict(bool)
    for n, line in enumerate(lines):
        if line.strip():
            x, y = follow_path(line)
            tiles[(x, y)] ^= True
            print(f"{x}, {y}  ({n:3d})")
    return tiles

def propagate_tiles(tiles):
    """Evolve the tiles for one iteration.  The input is a dict mapping
    tile coordinates to a boolean (True, if tile is black).
    The dict representing the new state of the tiles is returned.
    """
    result = defaultdict(bool)
    tile_queue = [coords for coords, v in tiles.items() if v]
    considered = set(tile_queue) # the tiles we're looking at this round
    while tile_queue:
        x, y = tile_queue.pop(0)
        result[(x,y)] = apply_rule(tiles, x, y)
        if tiles[(x, y)]:
            for dx, dy in DIR.values():
                if (x + dx, y + dy) not in considered:
                    tile_queue.append((x + dx, y + dy))
                    considered.add((x + dx, y + dy))
    return result

def apply_rule(tiles, x, y):
    is_black = tiles[(x, y)]
    black_neighbors = sum([1 for dx, dy in DIR.values() if tiles[(x+dx, y+dy)]])
    if is_black and black_neighbors == 0 or black_neighbors > 2:
        return False # white
    if not is_black and black_neighbors == 2:
        return True # black
    return is_black # no change

def solve(lines):
    """Solve the problem."""
    tiles = defaultdict(bool)
    for n, line in enumerate(lines):
        if line.strip():
            x, y = follow_path(line)
            tiles[(x, y)] ^= True
    count = sum([1 for v in tiles.values() if v])
    return count


def solve2(lines):
    """Solve the problem."""
    tiles = defaultdict(bool)
    for n, line in enumerate(lines):
        if line.strip():
            x, y = follow_path(line)
            tiles[(x, y)] ^= True
    for day in range(1, 101):
        tiles = propagate_tiles(tiles)
        count = sum([1 for v in tiles.values() if v])
        print(f"Day {day}: {count}")
    return count


# PART 1

def example1():
    """Run example for problem with input lines."""
    print("EXAMPLE 1:")
    lines = filter_blank_lines(SAMPLE_INPUT.split("\n"))
    result = solve(lines)
    expected = 10
    print(f"'sample-input' -> {result} (expected {expected})")
    assert result == expected
    print("= " * 32)


def part1(lines):
    print("PART 1:")
    result = solve(lines)
    print(f"result is {result}")
    expected = 495
    assert result == expected
    print("= " * 32)


# PART 2

def example2():
    """Run example for problem with input lines."""
    print("EXAMPLE 2:")
    lines = filter_blank_lines(SAMPLE_INPUT.split("\n"))
    result = solve2(lines)
    expected = 2208
    print(f"'sample-input' -> {result} (expected {expected})")
    assert result == expected
    print("= " * 32)


def part2(lines):
    print("PART 1:")
    result = solve2(lines)
    print(f"result is {result}")
    print("= " * 32)



if __name__ == "__main__":
    example1()
    lines = load_input(INPUTFILE)
    part1(lines)
    example2()
    part2(lines)
