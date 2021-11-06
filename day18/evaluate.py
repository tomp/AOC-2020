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

PLUS = "+"
TIMES = "*"
MINUS = "-"
DIV = "/"
EXP = "^"
LPAREN = "("
RPAREN = ")"

OPERATORS = [PLUS, MINUS, TIMES, DIV, EXP]
SYMBOLS = OPERATORS + [LPAREN, RPAREN]

PREC = {
        LPAREN: 0,
        PLUS: 1,
        MINUS: 1,
        TIMES: 2,
        DIV: 2,
        EXP: 3,
}

TOKEN_RE = re.compile(r" *(\d+|[-+*/^()])")


def parse_expression(expr):
    """A list of tokens is returned.  A token may be an integer
    or a symbol.
    """
    tokens = []
    idx = 0
    print(expr[idx:])
    m = TOKEN_RE.match(expr[idx:])
    while m:
        token = m.group(1)
        idx += len(m.group(0))
        if token not in SYMBOLS:
            tokens.append(int(token))
        else:
            tokens.append(token)
        print(expr[idx:])
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
    if op == MINUS:
        return larg - rarg
    if op == TIMES:
        return larg * rarg
    if op == DIV:
        return larg // rarg
    if op == EXP:
        return pow(larg, rarg)
    raise ValueError(f"unrecognized operator '{op}'")

def evaluate(expr):
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
            print(f"token: {token} // output: {output} // ops: {opstack}")
            continue

        if token in OPERATORS:
            while opstack and PREC[opstack[-1]] >= PREC[token]:
                op = opstack.pop()
                val2 = output.pop()
                val1 = output.pop()
                output.append(apply_op(op, val1, val2))
            opstack.append(token)
            print(f"token: {token} // output: {output} // ops: {opstack}")
            continue

        if token == LPAREN:
            opstack.append(token)
            print(f"token: {token} // output: {output} // ops: {opstack}")
            continue

        if token == RPAREN:
            op = opstack.pop()
            while op != LPAREN:
                val2 = output.pop()
                val1 = output.pop()
                output.append(apply_op(op, val1, val2))
                op = opstack.pop()
            print(f"token: {token} // output: {output} // ops: {opstack}")
            continue

    while opstack:
        op = opstack.pop()
        val2 = output.pop()
        val1 = output.pop()
        output.append(apply_op(op, val1, val2))
        print(f"------   // output: {output} // ops: {opstack}")

    return output.pop()
