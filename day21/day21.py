#!/usr/bin/env python3
#
#  Advent of Code 2020 - day 21
#
from pathlib import Path
from collections import defaultdict
from dataclasses import dataclass
from pprint import pprint

INPUTFILE = "input.txt"

SAMPLE_INPUT = """
mxmxvkd kfcds sqjhc nhms (contains dairy, fish)
trh fvjkl sbzzf mxmxvkd (contains dairy)
sqjhc fvjkl (contains soy)
sqjhc mxmxvkd sbzzf (contains fish)
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

@dataclass
class Food:

    ingredients: list[str]
    allergens: list[str]

    @classmethod
    def from_text(cls, line):
        body, rest = line.split("(contains ")
        ingredients = [v.strip() for v in body.split()]
        allergens = [word.strip() for word in rest.rstrip(")").split(",")]
        return Food(ingredients, allergens)


def parse_input(lines):
    foods = []
    for line in lines:
        if not line:
            continue
        foods.append(Food.from_text(line))
    return foods

def allergen_candidates(foods):
    candidates = defaultdict(set) # ingredients that could contain each allergen
    for food in foods:
        for item in food.allergens:
            if item in candidates:
                candidates[item] &= set(food.ingredients)
            else:
                candidates[item] |= set(food.ingredients)
    return candidates

def solve(lines):
    """Solve the problem."""
    foods = parse_input(lines)
    
    all_ingredients = set()
    for food in foods:
        all_ingredients |= set(food.ingredients)

    candidates = allergen_candidates(foods)

    safe = all_ingredients
    for items in candidates.values():
        safe -= items

    count = 0
    for food in foods:
        count += sum([1 for v in food.ingredients if v in safe])
    return count

def solve2(lines):
    """Solve the problem."""
    foods = parse_input(lines)
    candidates = allergen_candidates(foods)
    allergen_count = len(candidates)

    allergen = dict()
    assigned = set()
    while len(assigned) < allergen_count:
        completed = len(assigned)
        for k, v in candidates.items():
            if len(v) == 1:
                ingredient = v.pop()
                assert ingredient not in assigned
                allergen[k] = ingredient
                assigned.add(ingredient)
        if len(assigned) == completed:
            raise RuntimeError("We're stuck")
        for v in candidates.values():
            v -= assigned

    return ",".join([v for _, v in sorted(allergen.items())])


# PART 1

def example1():
    """Run example for problem with input lines."""
    lines = filter_blank_lines(SAMPLE_INPUT.split("\n"))
    result = solve(lines)
    expected = 5
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
    lines = filter_blank_lines(SAMPLE_INPUT.split("\n"))
    result = solve2(lines)
    expected = "mxmxvkd,sqjhc,fvjkl"
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
