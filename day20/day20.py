#!/usr/bin/env python3
#
#  Advent of Code 2020 - day 20
#
from pathlib import Path
from copy import deepcopy
from collections import defaultdict
import re
import math
import pdb

INPUTFILE = "input.txt"

HEADER_RE = re.compile(r"Tile (\d+):")

MONSTER_RE1 = re.compile(r"..................#.")
MONSTER_RE2 = re.compile(r"#....##....##....###")
MONSTER_RE3 = re.compile(r".#..#..#..#..#..#...")

MONSTER = [
    "                  # ",
    "#    ##    ##    ###",
    " #  #  #  #  #  #   ",
]
MONSTER_LEN = len(MONSTER[0])
MONSTER_PIXELS = 15

PIXEL_CODE = {".": "0", "#": "1"}
PIXEL = {"0": ".", "1": "#"}

ROT0, ROT90, ROT180, ROT270 = 0, 90, 180, 270

VERTICAL, HORIZONTAL = "vertical", "horizontal"

TOP_LEFT = "top-left"
TOP_RIGHT = "top-right"
BOTTOM_LEFT = "bottom-left"
BOTTOM_RIGHT = "bottom-right"

TOP, RIGHT, BOTTOM, LEFT = 0, 1, 2, 3

NEIGHBOR_EDGE = [2, 3, 0, 1]

SAMPLE_INPUT = """
Tile 2311:
..##.#..#.
##..#.....
#...##..#.
####.#...#
##.##.###.
##...#.###
.#.#.#..##
..#....#..
###...#.#.
..###..###

Tile 1951:
#.##...##.
#.####...#
.....#..##
#...######
.##.#....#
.###.#####
###.##.##.
.###....#.
..#.#..#.#
#...##.#..

Tile 1171:
####...##.
#..##.#..#
##.#..#.#.
.###.####.
..###.####
.##....##.
.#...####.
#.##.####.
####..#...
.....##...

Tile 1427:
###.##.#..
.#..#.##..
.#.##.#..#
#.#.#.##.#
....#...##
...##..##.
...#.#####
.#.####.#.
..#..###.#
..##.#..#.

Tile 1489:
##.#.#....
..##...#..
.##..##...
..#...#...
#####...#.
#..#.#.#.#
...#.#.#..
##.#...##.
..##.##.##
###.##.#..

Tile 2473:
#....####.
#..#.##...
#.##..#...
######.#.#
.#...#.#.#
.#########
.###.#..#.
########.#
##...##.#.
..###.#.#.

Tile 2971:
..#.#....#
#...###...
#.#.###...
##.##..#..
.#####..##
.#..####.#
#..#.#..#.
..####.###
..#.#.###.
...#.#.#.#

Tile 2729:
...#.#.#.#
####.#....
..#.#.....
....#..#.#
.##..##.#.
.#.####...
####.#.#..
##.####...
##..#.##..
#.##...##.

Tile 3079:
#.#.#####.
.#..######
..#.......
######....
####.#..#.
.#...#.##.
#.#####.##
..#.###...
..#.......
..#.###...

"""


def sample_input():
    return SAMPLE_INPUT.strip("\n").split("\n")

# Utility functions

def load_input(infile):
    return [line.strip() for line in Path(infile).open()]

# Solution

def parse_input(lines):
    """Return a dict mapping tile id to a 10x10 array,
    representing the tile.
    """
    sections = parse_sections(lines)
    tiles = []
    for sect in sections:
        tile = Tile.from_text(sect)
        tiles.append(tile)
    return Mosaic(tiles)

def parse_sections(lines):
    result = []
    sect = []
    for line in lines:
        line = line.strip()
        if not line:
            if sect:
                result.append(sect)
            sect = []
        else:
            sect.append(line)
    if sect:
        result.append(sect)
    return result


class Mosaic():
    def __init__(self, tiles):
        self.tiles = {tile.id: tile.dup() for tile in tiles}
        self.tile_count = len(self.tiles)
        self.tile_size = tiles[0].tile_size
        self.top_left = None
        self._find_neighbors()

    def _find_neighbors(self):
        """Update the given tiles (in place) with links to each of their 2,
        3, or 4 neighbors.
        """
        # identify tiles with shared edges
        edges = defaultdict(list)
        for tile in self.tiles.values():
            for edge in tile.edges:
                 edges[edge].append(tile.id)
        for linked_tiles in edges.values():
            assert len(linked_tiles) <= 2

        for tile in self.tiles.values():
            tile.neighbors = []
            tile.nayb_count = 0
            for edge in tile.edges:
                linked_tiles = edges[edge]
                if len(linked_tiles) == 1:
                    tile.neighbors.append(None)
                elif tile.id == linked_tiles[0]:
                    tile.neighbors.append(self.tiles[linked_tiles[1]])
                    tile.nayb_count += 1
                else:
                    tile.neighbors.append(self.tiles[linked_tiles[0]])
                    tile.nayb_count += 1

    def tile_grid(self):
        """Return a grid (list of lists) of all the tiles."""
        assert self.top_left

        rows = []
        left_tile = self.top_left
        while left_tile:
            tile = left_tile
            row = [tile]
            while tile.neighbors[RIGHT]:
                tile = tile.neighbors[RIGHT]
                row.append(tile)
            rows.append(row)
            left_tile = left_tile.neighbors[BOTTOM]
        return rows

    def pixels(self):
        rows = []
        for grid_row in self.tile_grid():
            for r in range(1, self.tile_size-1):
                rows.append("".join([tile.pixels[r][1:-1] for tile in grid_row]))
        return rows
    
    def draw(self):
        print("\n".join(self.pixels()))

    @property
    def corners(self):
        return [tile for tile in self.tiles.values() if tile.nayb_count == 2]

    def set_top_left(self, tile_id):
        tile = self.tiles[tile_id]
        assert tile.nayb_count == 2

        # print(f"==== set_top_left({tile_id})")
        # print("#### ROW")
        # print(f"Tile {tile.id}  {[v.id if v else '----' for v in tile.neighbors]}")

        # orient the top-left tile
        while tile.neighbors[TOP] or tile.neighbors[LEFT]:
            tile.rotate(ROT90)
        self.top_left = tile
        # print(f"---> {tile.id}  {[v.id if v else '----' for v in tile.neighbors]}")

        left_tile = self.top_left
        last_row = []
        while left_tile:
            tile = left_tile
            this_row = [left_tile]
            col = 0
            while tile.neighbors[RIGHT]:
                nayb = tile.neighbors[RIGHT]
                col += 1
                # print(f"Tlle {nayb.id}  {[v.id if v else '----' for v in nayb.neighbors]}")
                tile_pos = nayb.nayb_position(tile.id)
                rot = ((LEFT - tile_pos) % 4) * 90
                nayb.rotate(rot)
                # print(f"---> {nayb.id}  {[v.id if v else '----' for v in nayb.neighbors]}")

                if not last_row and nayb.neighbors[TOP] is not None:
                    nayb.flip(VERTICAL)
                    # print(f"---> {nayb.id}  {[v.id if v else '----' for v in nayb.neighbors]}")
                elif last_row and nayb.neighbors[TOP] != last_row[col]:
                    nayb.flip(VERTICAL)
                    # print(f"---> {nayb.id}  {[v.id if v else '----' for v in nayb.neighbors]}")
                    assert nayb.neighbors[TOP].neighbors[BOTTOM].id == nayb.id
                tile = nayb
                this_row.append(tile)
            last_row = this_row
            nayb = left_tile.neighbors[BOTTOM]
            if nayb:
                # print("#### ROW")
                # print(f"Tlle {nayb.id}  {[v.id if v else '----' for v in nayb.neighbors]}")
                tile_pos = nayb.nayb_position(left_tile.id)
                rot = ((TOP - tile_pos) % 4) * 90
                nayb.rotate(rot)
                # print(f"---> {nayb.id}  {[v.id if v else '----' for v in nayb.neighbors]}")
                if left_tile.neighbors[LEFT] is None and nayb.neighbors[LEFT] is not None:
                    nayb.flip(HORIZONTAL)
                    # print(f"---> {nayb.id}  {[v.id if v else '----' for v in nayb.neighbors]}")
            left_tile = nayb

        # for row in self.tile_grid():
        #     print(" ".join([f"{tile.id:4d}" for tile in row]))


class Tile():
    """A Tile object is a representaion of a 10x10 tile.
    It provides methods for matching tile edges, rotating the tile,
    and displaying the tile.
    """
    tiles = dict()

    def __init__(self, tile_id, matrix, neighbors=None):
        assert len(matrix[0]) == len(matrix)
        self.id = tile_id
        self.matrix = matrix
        self.edges = edge_codes(self.matrix)
        self.neighbors = []
        self.nayb_count = None
        if neighbors:
            self.neighbors = neighbors
            self.nayb_count = sum([1 for v in self.neighbors if v])

    def dup(self):
        return Tile(self.id, self.matrix, self.neighbors)

    @classmethod
    def from_text(cls, lines):
        m = HEADER_RE.match(lines[0])
        tile_id = int(m.group(1))
        matrix = [ [PIXEL_CODE[ch] for ch in line] for line in lines[1:] ]
        return cls(tile_id, matrix)

    @property
    def tile_size(self):
        return len(self.matrix)

    @property
    def pixels(self):
        return ["".join([PIXEL[v] for v in row]) for row in self.matrix]

    def draw(self):
        print("\n".join(self.pixels))

    def flip(self, axis) -> None:
        """Flip this tile, in place.  The edge list and neighbors are
        updated to follow.
        """
        if axis == VERTICAL:
            self.matrix = self.matrix[::-1]
            top, right, bottom, left = self.edges
            self.edges = (bottom, right, top, left)
            top, right, bottom, left = self.neighbors
            self.neighbors = (bottom, right, top, left)
        elif axis == HORIZONTAL:
            self.matrix = [row[::-1] for row in self.matrix]
            top, right, bottom, left = self.edges
            self.edges = (top, left, bottom, right)
            top, right, bottom, left = self.neighbors
            self.neighbors = (top, left, bottom, right)
        else:
            raise ValueError(f"unsupported flip axis '{axis}'")

    def rotate(self, rot) -> None:
        """Rotate this tile, in place.  The edge list and neighbors are
        updated to follow.
        """
        if rot == ROT0:
            return
        elif rot == ROT90:
            matrix = []
            for i in range(self.tile_size):
                matrix.append(
                    [self.matrix[j][i] for j in range(self.tile_size-1,-1,-1)]
                )
            self.matrix = matrix
            self.edges = rotate_list(self.edges, 1)
            self.neighbors = rotate_list(self.neighbors, 1)
        elif rot == ROT180:
            matrix = []
            for row in self.matrix[::-1]:
                matrix.append(row[::-1])
            self.matrix = matrix
            self.edges = rotate_list(self.edges, 2)
            self.neighbors = rotate_list(self.neighbors, 2)
        elif rot == ROT270:
            matrix = []
            for i in range(self.tile_size-1, -1, -1):
                matrix.append(
                    [row[i] for row in self.matrix]
                )
            self.matrix = matrix
            self.edges = rotate_list(self.edges, 3)
            self.neighbors = rotate_list(self.neighbors, 3)
        else:
            raise ValueError(f"unsupported rotation '{rot}'")

    def nayb_positions(self):
        return [i for i, v in enumerate(self.neighbors) if v]

    def nayb_position(self, nayb_id):
        for i, nayb in enumerate(self.neighbors):
            if nayb and nayb.id == nayb_id:
                return i
        raise ValueError(
            f"tile {nayb_id} not in tile {self.id} neighbors: "
            f"(', '.join([v.id if v else "" for v in self.neighbors]))"
        )


def rotate_list(items, count):
    count = count % len(items)
    return items[-count:] + items[:-count]

def codes(edge):
    """Return forward and backward codes for the given tile edge, a list
    of the characters ("0" or "1") on an edge of the matrix.
    """
    fwd = int("".join(edge), 2)
    back = int("".join(reversed(edge)), 2)
    return fwd, back

def edge_codes(matrix):
    """Return a code for each of the four tile edges, by converting the
    sequenece of 0's and 1's into an integer.  The code can be calculated
    in either direction, and in general, that would matter.  For this AoC
    problem, the tiles were defnined so that there's only one possible
    adjacent tile for each tile, and so we only need to consider the
    lower of the forward and backward code values.
    A tuple of edge codes (top, right, bottom, left) is returned.
    """
    top = codes(matrix[0])
    bottom = codes(matrix[-1][::-1])
    right = codes([row[-1] for row in matrix])
    left = codes([row[0] for row in matrix[::-1]])
    return min(*top), min(*right), min(*bottom), min(*left)

def assemble_tiles(tiles, topleft):
    """Assemble the tiles into a mosaic, with the given tile as the top left
    corner tile.
    """
    return []

def find_monsters(rows):
    row_len = len(rows[0])
    matches = []
    r = 2
    while r < len(rows):
        pos = 0
        while pos <= row_len:
            m = MONSTER_RE3.search(rows[r], pos)
            if not m:
                break
            # print(f"<match 3 @ {r},{m.start()}>")
            start = m.start()
            if MONSTER_RE2.match(rows[r-1], start) and MONSTER_RE1.match(rows[r-2], start):
                matches.append((r, start))
                print(f"*** MATCH @ {r}, {start}")
            pos = start + 1
        r += 1
    return matches


def solve(lines):
    """Solve the problem."""
    moz = parse_input(lines)
    return math.prod([tile.id for tile in moz.corners])

def solve2(lines):
    """Solve the problem."""
    moz  = parse_input(lines)

    # assemble the tiles using each of the corners as the top left corner
    # and search each of those for the sea monsters
    result = 100 * moz.tile_count  # total number of pixels

    moz.set_top_left(moz.corners[0].id)
    pixels = moz.pixels()
    total_pixels = sum([row.count('#') for row in pixels])
    print(f"total pixels: {total_pixels}")

    for corner in moz.corners:
        moz.set_top_left(corner.id)
        pixels = moz.pixels()
        print("\n".join(pixels))
        matches = find_monsters(pixels)
        if matches:
            print(f"==> {len(matches)} SEA MONSTERS FOUND")
            result = min(result, total_pixels - (MONSTER_PIXELS * len(matches)))
        else:
            print("==> no matches")

        pixels = [row[::-1] for row in pixels]
        print("\n".join(pixels))
        matches = find_monsters(pixels)
        if matches:
            print(f"==> {len(matches)} SEA MONSTERS FOUND")
            result = min(result, total_pixels - (MONSTER_PIXELS * len(matches)))
        else:
            print("==> no matches")

        pixels = pixels[::-1]
        print("\n".join(pixels))
        matches = find_monsters(pixels)
        if matches:
            print(f"==> {len(matches)} SEA MONSTERS FOUND")
            result = min(result, total_pixels - (MONSTER_PIXELS * len(matches)))
        else:
            print("==> no matches")

        pixels = [row[::-1] for row in pixels]
        print("\n".join(pixels))
        matches = find_monsters(pixels)
        if matches:
            print(f"==> {len(matches)} SEA MONSTERS FOUND")
            result = min(result, total_pixels - (MONSTER_PIXELS * len(matches)))
        else:
            print("==> no matches")

    return result


# PART 1

def example1():
    """Run example for problem with input lines."""
    lines = SAMPLE_INPUT.split("\n")
    result = solve(lines)
    expected = 20899048083289
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
    lines = SAMPLE_INPUT.split("\n")
    result = solve2(lines)
    expected = 273
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
