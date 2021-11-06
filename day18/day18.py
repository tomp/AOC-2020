#!/usr/bin/env python3
#
#  Advent of Code 2020 - day 18
#
from pathlib import Path
import re

INPUTFILE = "input.txt"

SAMPLE_CASES = [
    ("1 + 2 * 3 + 4 * 5 + 6", 71),
    ("1 + (2 * 3) + (4 * (5 + 6))", 51),
    ("2 * 3 + (4 * 5)", 26),
    ("5 + (8 * 3 + 9 + 3 * 4 * 3)", 437),
    ("5 * 9 * (7 * 3 * 3 + 9 * 3 + (8 + 6 * 4))", 12240),
    ("((2 + 4 * 9) * (6 + 9 * 8 + 6) + 6) + 2 + 4 * 2", 13632),
]

SAMPLE_CASES2 = [
    ("1 + 2 * 3 + 4 * 5 + 6", 231),
    ("1 + (2 * 3) + (4 * (5 + 6))", 51),
    ("2 * 3 + (4 * 5)", 46),
    ("5 + (8 * 3 + 9 + 3 * 4 * 3)", 1445),
    ("5 * 9 * (7 * 3 * 3 + 9 * 3 + (8 + 6 * 4))", 669060),
    ("((2 + 4 * 9) * (6 + 9 * 8 + 6) + 6) + 2 + 4 * 2", 23340),
]

PLUS = "+"
TIMES = "*"
LPAREN = "("
RPAREN = ")"

OPERATORS = [PLUS, TIMES]
SYMBOLS = OPERATORS + [LPAREN, RPAREN]

PREC1 = {
    LPAREN: 0,
    PLUS: 1,
    TIMES: 1,
}

PREC2 = {
    LPAREN: 0,
    TIMES: 1,
    PLUS: 2,
}

TOKEN_RE = re.compile(r" *(\d+|[+*()])")


# Utility functions

def load_input(infile):
    return filter_blank_lines(Path(infile).open())

def filter_blank_lines(lines):
    return [line.strip() for line in lines if line.strip()]


# Solution

def parse_expression(expr):
    """A list of tokens is returned.  A token may be an integer
    or a symbol.
    """
    tokens = []
    idx = 0
    m = TOKEN_RE.match(expr[idx:])
    while m:
        token = m.group(1)
        idx += len(m.group(0))
        if token not in SYMBOLS:
            tokens.append(int(token))
        else:
            tokens.append(token)
        m = TOKEN_RE.match(expr[idx:])
    return tokens

def is_val(token):
    return isinstance(token, int)

def is_op(token):
    return token in OPERATORS

def apply_op(op, larg, rarg):
    """Apply the given binary operator to the two arguments.
    The result value is returned
    """
    if op == PLUS:
        return larg + rarg
    if op == TIMES:
        return larg * rarg
    raise ValueError(f"unrecognized operator '{op}'")

def evaluate(expr, prec=PREC1):
    """Evaluate the given arithmetic expression.
    The integer value of the expression is returned.
    """
    tokens = parse_expression(expr)

    opstack = []
    output = []
    while tokens:
        token = tokens.pop(0)
        if is_val(token):
            output.append(token)
            # print(f"token: {token} // output: {output} // ops: {opstack}")
            continue

        if token in OPERATORS:
            while opstack and prec[opstack[-1]] >= prec[token]:
                op = opstack.pop()
                val2 = output.pop()
                val1 = output.pop()
                output.append(apply_op(op, val1, val2))
            opstack.append(token)
            # print(f"token: {token} // output: {output} // ops: {opstack}")
            continue

        if token == LPAREN:
            opstack.append(token)
            # print(f"token: {token} // output: {output} // ops: {opstack}")
            continue

        if token == RPAREN:
            op = opstack.pop()
            while op != LPAREN:
                val2 = output.pop()
                val1 = output.pop()
                output.append(apply_op(op, val1, val2))
                op = opstack.pop()
            # print(f"token: {token} // output: {output} // ops: {opstack}")
            continue

    while opstack:
        op = opstack.pop()
        val2 = output.pop()
        val1 = output.pop()
        output.append(apply_op(op, val1, val2))
        # print(f"------   // output: {output} // ops: {opstack}")

    return output.pop()


# PART 1

def example1():
    """Run example for problem with input arguments."""
    for arg, expected in SAMPLE_CASES:
        result = evaluate(arg)
        print(f"'{arg}' -> {result} (expected {expected})")
        assert result == expected
    print("= " * 32)


def part1(lines):
    result = sum([evaluate(line) for line in lines])
    print(f"result is {result}")
    print("= " * 32)


# PART 2

def example2():
    """Run example for problem with input arguments."""
    for arg, expected in SAMPLE_CASES2:
        result = evaluate(arg, prec=PREC2)
        print(f"'{arg}' -> {result} (expected {expected})")
        assert result == expected
    print("= " * 32)


def part2(lines):
    result = sum([evaluate(line, prec=PREC2) for line in lines])
    print(f"result is {result}")
    print("= " * 32)


if __name__ == "__main__":
    example1()
    lines = load_input(INPUTFILE)
    part1(lines)
    example2()
    part2(lines)
