#!/usr/bin/env python3
#
#  Advent of Code 2020 - day 16
#
from pathlib import Path
from collections import defaultdict
import math
from pprint import pprint

INPUTFILE = "input.txt"

SAMPLE_INPUT = """
class: 1-3 or 5-7
row: 6-11 or 33-44
seat: 13-40 or 45-50

your ticket:
7,1,14

nearby tickets:
7,3,47
40,4,50
55,2,20
38,6,12
"""

SAMPLE_INPUT2 = """
class: 0-1 or 4-19
row: 0-5 or 8-19
seat: 0-13 or 16-19

your ticket:
11,12,13

nearby tickets:
3,9,18
15,1,5
5,14,9
"""

def sample_input(text):
    return text.strip("\n").split("\n")


# Utility functions

class Field():
    def __init__(self, name, cond):
        self.name = name
        self.cond = cond

    @classmethod
    def from_text(cls, line):
        name, rest = line.split(": ")
        items = [v.strip() for v in rest.split(" or ")]
        cond = []
        for item in items:
            cond.append([int(v) for v in item.split("-")])
        return cls(name, cond)

    def valid(self, val):
        return any([v[0] <= val <= v[1] for v in self.cond])


def maybe_valid(rules, val):
    return any([field.valid(val) for field in rules.values()])

def load_input(infile):
    lines = [line.strip("\n") for line in list(Path(infile).open())]
    while not lines[0]:
        lines = lines[1:]
    while not lines[-1]:
        lines = lines[:-1]
    return lines

def parse_input(lines):
    """Parse the input document, which contains validity rules for the various
    ticket fields, a representation of my ticket, and representations of a
    number of other observed tickets.
    Return a tuple of (rules, ticket, nearby_tickets)
    """
    section = parse_sections(lines)
    rules = parse_rules(section[0])
    my_ticket = parse_ticket(section[1][1])
    tickets = [parse_ticket(line) for line in section[2][1:]]
    return (rules, my_ticket, tickets)

def parse_rules(lines):
    fields = {}
    for line in lines:
        field = Field.from_text(line)
        fields[field.name] = field
    return fields

def parse_sections(lines):
    """Parse the input document into sections, separated by blank lines.
    A list of lists is returned.  Each item is the list of lines for a section.
    """
    secid = 0
    section = []
    for line in lines:
        if not line.strip():
            secid += 1
            continue
        if len(section) == secid:
            section.append([line])
        else:
            section[secid].append(line)
    return [v for v in section if v]

def parse_ticket(line):
    return [int(v) for v in line.split(",")]

# Solution

def solve(lines):
    """Solve the problem."""
    rules, _, tickets = parse_input(lines)
    invalid = []
    for ticket in tickets:
        for val in ticket:
            if not maybe_valid(rules, val):
                invalid.append(val)
    return sum(invalid)

def solve2(lines):
    """Solve the problem."""
    rules, ticket, tickets = parse_input(lines)
    valid = []
    for tkt in tickets:
        if all([maybe_valid(rules, val) for val in tkt]):
            valid.append(tkt)

    possible = defaultdict(set)
    fieldname = dict()
    for idx, val in enumerate(ticket):
        for field in rules.values():
            if all([field.valid(tkt[idx]) for tkt in valid]):
                possible[idx].add(field.name)
                print(f"field {idx} could be {field.name}")

    assigned = set()
    while len(assigned) < len(ticket):
        for idx, names in possible.items():
            if len(names) == 1:
                name = names.pop()
                assert name not in assigned
                fieldname[idx] = name
                assigned.add(name)
                print(f"field {idx} assigned to {name}")
        for idx in possible:
            possible[idx] -= assigned

    result = {}
    for idx, val in enumerate(ticket):
        result[fieldname[idx]] = val
    return result


# PART 1

def example1():
    """Run example for problem with input lines."""
    lines = sample_input(SAMPLE_INPUT)
    result = solve(lines)
    expected = 71
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
    lines = sample_input(SAMPLE_INPUT2)
    result = solve2(lines)
    expected = {"class": 12, "row": 11, "seat": 13}
    print(f"'sample-input' -> {result} (expected {expected})")
    assert result == expected
    print("= " * 32)


def part2(lines):
    ticket = solve2(lines)
    print("my ticket:")
    pprint(ticket)
    result = math.prod([v for k, v in ticket.items() if "departure" in k])
    print(f"result is {result}")
    print("= " * 32)


if __name__ == "__main__":
    example1()
    lines = load_input(INPUTFILE)
    part1(lines)
    example2()
    part2(lines)
