#!/usr/bin/env python3
#
#  Advent of Code 2020 - day 19
#
from pathlib import Path
from pprint import pprint

INPUTFILE = "input.txt"

SAMPLE_INPUT = """
0: 4 1 5
1: 2 3 | 3 2
2: 4 4 | 5 5
3: 4 5 | 5 4
4: "a"
5: "b"

ababbb
bababa
abbbab
aaabbb
aaaabbb
"""

SAMPLE_INPUT2 = """
42: 9 14 | 10 1
9: 14 27 | 1 26
10: 23 14 | 28 1
1: "a"
11: 42 31
5: 1 14 | 15 1
19: 14 1 | 14 14
12: 24 14 | 19 1
16: 15 1 | 14 14
31: 14 17 | 1 13
6: 14 14 | 1 14
2: 1 24 | 14 4
0: 8 11
13: 14 3 | 1 12
15: 1 | 14
17: 14 2 | 1 7
23: 25 1 | 22 14
28: 16 1
4: 1 1
20: 14 14 | 1 15
3: 5 14 | 16 1
27: 1 6 | 14 18
14: "b"
21: 14 1 | 1 14
25: 1 1 | 1 14
22: 14 14
8: 42
26: 14 22 | 1 20
18: 15 15
7: 14 5 | 1 21
24: 14 1

aaaaabbaabaaaaababaa
aaaabbaabbaaaaaaabbbabbbaaabbaabaaa
aaabbbbbbaaaabaababaabababbabaaabbababababaaa
aabbbbbaabbbaaaaaabbbbbababaaaaabbaaabba
ababaaaaaabaaab
ababaaaaabbbaba
abbbbabbbbaaaababbbbbbaaaababb
baabbaaaabbaaaababbaababb
babbbbaabbbbbabbbbbbaabaaabaaa
bbabbbbaabaabba
bbbababbbbaaaaaaaabbababaaababaabab
bbbbbbbaaaabbbbaaabbabaaa
"""


"""
# ORIGINAL (sorted)
aaaaabbaabaaaaababaa
aaaabbaaaabbaaa
aaaabbaabbaaaaaaabbbabbbaaabbaabaaa
aaabbbbbbaaaabaababaabababbabaaabbababababaaa
aabbbbbaabbbaaaaaabbbbbababaaaaabbaaabba
ababaaaaaabaaab
ababaaaaabbbaba
abbbbabbbbaaaababbbbbbaaaababb
abbbbbabbbaaaababbaabbbbabababbbabbbbbbabaaaa
baabbaaaabbaaaababbaababb
babaaabbbaaabaababbaabababaaab
babbbbaabbbbbabbbbbbaabaaabaaa
bbabbbbaabaabba
bbbababbbbaaaaaaaabbababaaababaabab
bbbbbbbaaaabbbbaaabbabaaa
"""

"""
# EXPECTED FAILURES (sorted)
aaaabbaaaabbaaa
abbbbbabbbaaaababbaabbbbabababbbabbbbbbabaaaa
babaaabbbaaabaababbaabababaaab
"""

"""
# EXPECTED MATCHES (sorted)
aaaaabbaabaaaaababaa
aaaabbaabbaaaaaaabbbabbbaaabbaabaaa
aaabbbbbbaaaabaababaabababbabaaabbababababaaa
aabbbbbaabbbaaaaaabbbbbababaaaaabbaaabba
ababaaaaaabaaab
ababaaaaabbbaba
abbbbabbbbaaaababbbbbbaaaababb
baabbaaaabbaaaababbaababb
babbbbaabbbbbabbbbbbaabaaabaaa
bbabbbbaabaabba
bbbababbbbaaaaaaaabbababaaababaabab
bbbbbbbaaaabbbbaaabbabaaa
"""


# Utility functions

def load_input(infile):
    return [v.strip() for v in Path(infile).open()]

def filter_blank_lines(lines):
    return [line.strip() for line in lines if line.strip()]


# Solution

def parse_rule(line):
    num, rest = line.split(": ")
    if rest[0] == '"':
        val = rest.strip('"')
        return num, val, None, None
     
    if "|" not in rest:
        return num, None, rest.strip().split(), None

    alt1, alt2 = rest.strip().split(" | ")
    return num, None, alt1.split(), alt2.split()

def parse_input(lines):
    """Parse input doc and return a dict representing the rules, and a list
    of messages to validate.
    """
    rule = dict()
    messages = None
    for line in lines:
        if messages is not None:
            if line:
                messages.append(line)
            continue
        if not line.strip():
            messages = []
            continue
        idx, val, seq1, seq2 = parse_rule(line)
        rule[idx] = (val, seq1, seq2)

    return rule, messages

def match_rule(rule, message, num, idx, step=0):
    """Returns an integer, reporting the new message position, if we
    successfully matched the message, or 0 if we did not match it.
    """
    step += 1
    if idx >= len(message):
        print(f"[{step:02d}] --> 0")
        return 0
    print(f"[{step:02d}] match_rule: {num} @{idx}  '{message[idx:]}'")
    val, seq1, seq2 = rule[num]
    if val:
        if message[idx] == val:
            print(f"[{step:02d}] {val} --> {idx+1}")
            return idx + 1
        print(f"[{step:02d}] {val} --> 0")
        return 0
    if seq1:
        new_idx = match_seq(rule, message, seq1, idx, step)
        if new_idx:
            print(f"[{step:02d}] --> {new_idx}")
            return new_idx
    if seq2:
        new_idx = match_seq(rule, message, seq2, idx, step)
        if new_idx:
            print(f"[{step:02d}] --> {new_idx}")
            return new_idx
    print(f"[{step:02d}] --> 0")
    return 0

def match_seq(rule, message, seq, idx, step):
    """Returns an integer, reporting how many characters were matched."""
    print(f"[{step:02d}] match_seq: {seq} @{idx}")
    for num in seq:
        idx = match_rule(rule, message, num, idx, step)
        if idx == 0:
            return 0
    return idx

def validate(rule, message):
    """Validate the given message against the rules.
    Return True if it's valid, else False.
    """
    print("- " * 32)
    print(f"validate: '{message}'")
    result = match_rule(rule, message, "0", 0)
    if result == len(message):
        print(f"MATCH  '{message}'")
        return True
    print(f"failed  '{message}'")
    return False


def solve(lines):
    """Solve the problem."""
    rule, messages = parse_input(lines)
    print("RULES:")
    pprint(rule)
    print("MESSAGES:")
    print("\n".join(messages))
    result = 0
    for message in messages:
        if validate(rule, message):
            result += 1
    return result


def solve2(lines):
    """Solve the problem."""
    rule, messages = parse_input(lines)
    rule['8'] = (None, ['42'], ['42', '8'])
    rule['11'] = (None, ['42', '31'], ['42', '11', '31'])
    print("RULES:")
    pprint(rule)
    print("MESSAGES:")
    print("\n".join(messages))
    result = 0
    for message in messages:
        if validate(rule, message):
            result += 1
    return result


# PART 1

def example1():
    """Run example for problem with input lines."""
    print("\nEXAMPLE 1")
    lines = SAMPLE_INPUT.strip("\n").split("\n")
    result = solve(lines)
    expected = 2
    print(f"'sample-input' -> {result} (expected {expected})")
    assert result == expected
    print("= " * 32)


def part1(lines):
    print("\nPART 1")
    result = solve(lines)
    print(f"result is {result}")
    assert result == 149
    print("= " * 32)


# PART 2

def example2():
    """Run example for problem with input lines."""
    print("\nEXAMPLE 2")
    lines = SAMPLE_INPUT2.strip("\n").split("\n")
    result = solve2(lines)
    expected = 12
    print(f"'sample-input' -> {result} (expected {expected})")
    assert result == expected
    print("= " * 32)


def part2(lines):
    print("\nPART 2")
    result = solve2(lines)
    print(f"result is {result}")
    print("= " * 32)


if __name__ == "__main__":
    example1()
    lines = load_input(INPUTFILE)
    part1(lines)
    example2()
    part2(lines)
