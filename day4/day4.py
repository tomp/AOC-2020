#!/usr/bin/env python3
#
#  Advent of Code 2020 - day 4
#
from pathlib import Path
import re

INPUTFILE = "input.txt"

REQD_FIELDS = ["byr", "iyr", "eyr", "hgt", "hcl", "ecl", "pid"]
REQD_COUNT = len(REQD_FIELDS)

HAIR_COLOR_RE = re.compile(r"#[0-9a-f]{6}$")
PID_RE = re.compile(r"\d{9}$")

EYE_COLORS = ["amb", "blu", "brn", "gry", "grn", "hzl", "oth"]


SAMPLE_TEXT = """
ecl:gry pid:860033327 eyr:2020 hcl:#fffffd
byr:1937 iyr:2017 cid:147 hgt:183cm

iyr:2013 ecl:amb cid:350 eyr:2023 pid:028048884
hcl:#cfa07d byr:1929

hcl:#ae17e1 iyr:2013
eyr:2024
ecl:brn pid:760753108 byr:1931
hgt:179cm

hcl:#cfa07d eyr:2025 pid:166559648
iyr:2011 ecl:brn hgt:59in

"""

SAMPLE2_INVALID_TEXT = """
eyr:1972 cid:100
hcl:#18171d ecl:amb hgt:170 pid:186cm iyr:2018 byr:1926

iyr:2019
hcl:#602927 eyr:1967 hgt:170cm
ecl:grn pid:012533040 byr:1946

hcl:dab227 iyr:2012
ecl:brn hgt:182cm pid:021572410 eyr:2020 byr:1992 cid:277

hgt:59cm ecl:zzz
eyr:2038 hcl:74454a iyr:2023
pid:3556412378 byr:2007
"""

SAMPLE2_VALID_TEXT = """
pid:087499704 hgt:74in ecl:grn iyr:2012 eyr:2030 byr:1980
hcl:#623a2f

eyr:2029 ecl:blu cid:129 byr:1989
iyr:2014 pid:896056539 hcl:#a97842 hgt:165cm

hcl:#888785
hgt:164cm byr:2001 iyr:2015 cid:88
pid:545766238 ecl:hzl
eyr:2022

iyr:2010 hgt:158cm hcl:#b6652a ecl:blu byr:1944 eyr:2021 pid:093154719
"""


def sample_input():
    return SAMPLE_TEXT.split("\n")


# Utility functions


def load_input(infile):
    return list(Path(infile).open())


def filter_blank_lines(lines):
    for line in lines:
        line = line.strip()
        if line:
            yield line


# Solution
def parse_passports(lines):
    passports = []
    passport = {}
    for line in lines:
        line = line.strip()
        if not line:
            if passport:
                passports.append(passport)
                passport = {}
            continue
        for field in line.split():
            key, value = field.split(":")
            passport[key] = value
    if passport:
        passports.append(passport)
    return passports


def field_is_valid(key, value):
    if key == "byr":
        return int(value) >= 1920 and int(value) <= 2002
    if key == "iyr":
        return int(value) >= 2010 and int(value) <= 2020
    if key == "eyr":
        return int(value) >= 2020 and int(value) <= 2030
    if key == "hgt":
        if value.endswith("cm"):
            return int(value[:-2]) >= 150 and int(value[:-2]) <= 193
        if value.endswith("in"):
            return int(value[:-2]) >= 59 and int(value[:-2]) <= 76
        return False
    if key == "hcl":
        return bool(HAIR_COLOR_RE.match(value))
    if key == "ecl":
        return value in EYE_COLORS
    if key == "pid":
        return bool(PID_RE.match(value))
    return False


def solve(lines):
    """Solve the problem."""
    passports = parse_passports(lines)
    print(f"parsed {len(passports)} passports from {len(lines)} input lines")

    valid = 0
    i = 0
    for p in passports:
        i += 1
        count = 0
        for key in p.keys():
            if key in REQD_FIELDS:
                count += 1
        if count == REQD_COUNT:
            valid += 1
    return valid


def solve2(lines):
    """Solve the problem."""
    passports = parse_passports(lines)
    print(f"parsed {len(passports)} passports from {len(lines)} input lines")

    valid = 0
    i = 0
    for p in passports:
        i += 1
        count = 0
        for key, value in p.items():
            if field_is_valid(key, value):
                count += 1
        if count == REQD_COUNT:
            valid += 1
    return valid


# PART 1


def lines_example():
    lines = sample_input()
    result = solve(lines)
    expected = 2
    print(f"'sample-input' -> {result} (expected {expected})")
    assert result == expected
    print("= " * 32)


example = lines_example


def part1(lines):
    result = solve(lines)
    print("result is {}".format(result))
    print("= " * 32)


# PART 2


def example2():
    lines = SAMPLE2_INVALID_TEXT.split("\n")
    result = solve2(lines)
    expected = 0
    print(f"'invalid-input' -> {result} (expected {expected})")
    assert result == expected

    lines = SAMPLE2_VALID_TEXT.split("\n")
    result = solve2(lines)
    expected = 4
    print(f"'valid-input' -> {result} (expected {expected})")
    assert result == expected

    print("= " * 32)


def part2(lines):
    result = solve2(lines)
    print("result is {}".format(result))
    print("= " * 32)


if __name__ == "__main__":
    example()
    lines = load_input(INPUTFILE)
    part1(lines)
    example2()
    part2(lines)
