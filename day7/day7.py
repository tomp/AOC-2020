#!/usr/bin/env python3
#
#  Advent of Code 2020 - day 7
#
from pathlib import Path
from collections import defaultdict
from pprint import pprint
import re


INPUTFILE = "input.txt"

SAMPLE_INPUT = """
light red bags contain 1 bright white bag, 2 muted yellow bags.
dark orange bags contain 3 bright white bags, 4 muted yellow bags.
bright white bags contain 1 shiny gold bag.
muted yellow bags contain 2 shiny gold bags, 9 faded blue bags.
shiny gold bags contain 1 dark olive bag, 2 vibrant plum bags.
dark olive bags contain 3 faded blue bags, 4 dotted black bags.
vibrant plum bags contain 5 faded blue bags, 6 dotted black bags.
faded blue bags contain no other bags.
dotted black bags contain no other bags.
"""

SAMPLE_INPUT2 = """
shiny gold bags contain 2 dark red bags.
dark red bags contain 2 dark orange bags.
dark orange bags contain 2 dark yellow bags.
dark yellow bags contain 2 dark green bags.
dark green bags contain 2 dark blue bags.
dark blue bags contain 2 dark violet bags.
dark violet bags contain no other bags.
"""


def sample_input():
    return list(filter_blank_lines(SAMPLE_INPUT.split("\n")))


def sample_input2():
    return list(filter_blank_lines(SAMPLE_INPUT2.split("\n")))


# Utility functions


def load_input(infile):
    return list(filter_blank_lines(Path(infile).open()))


def filter_blank_lines(lines):
    for line in lines:
        if line.strip():
            yield line.strip()


# Solution

RULE_RE = re.compile(r"(\w+ \w+) bags contain (\w.*\w)[.]")
BAGS_RE = re.compile(r"(\d+) (\w+ \w+) bags?")


def parse_rules(lines):
    contains = defaultdict(list)
    contained_by = defaultdict(list)
    for line in lines:
        if not line.strip():
            continue
        container, bags = parse_rule(line)
        for count, name in bags:
            contains[container].append((count, name))
            contained_by[name].append(container)
    return contained_by, contains


def parse_rule(line):
    m = RULE_RE.match(line.strip())
    if not m:
        raise ValueError(f"Cannot parse '{line}'")
    container, rest = m.groups()
    if rest == "no other bags":
        return container, []

    bags = []
    for bag in [v.strip() for v in rest.split(", ")]:
        m2 = BAGS_RE.match(bag)
        bags.append((int(m2.group(1)), m2.group(2)))
    return container, bags


def solve(lines, target="shiny gold"):
    """Solve the problem."""
    containers = set()
    contained_by, _ = parse_rules(lines)
    queue = list(contained_by[target])
    while queue:
        bag = queue.pop(0)
        # print(f"{bag}   {containers}")
        containers.add(bag)
        queue.extend(contained_by[bag])
    return len(containers)


def bag_size(contains, target="shiny gold"):
    total = 0
    for count, name in contains[target]:
        total += count * (bag_size(contains, name) + 1)
    return total


def solve2(lines, target="shiny gold"):
    """Solve the problem."""
    _, contains = parse_rules(lines)
    return bag_size(contains)


# PART 1


def example1():
    lines = sample_input()
    result = solve(lines)
    expected = 4
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
    expected = 32
    print(f"'sample-input' -> {result} (expected {expected})")
    assert result == expected

    lines = sample_input2()
    result = solve2(lines)
    expected = 126
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
