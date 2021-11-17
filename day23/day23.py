#!/usr/bin/env python3
#
#  Advent of Code 2020 - day 23
#
from typing import Optional
from pathlib import Path
from dataclasses import dataclass

INPUT = ("538914762", 100)

SAMPLE_CASES = [
    (("389125467", 10), "92658374"),
    (("389125467", 100), "67384529"),
]


# Solution

@dataclass
class LinkedList:

    value: int
    left: Optional["LinkedList"] = None
    right: Optional["LinkedList"] = None

    def __str__(self, curr_value: int = None) -> str:
        values = []
        if self.value != curr_value:
            values.append(f"{self.value}")
        else:
            values.append(f"({self.value})")
        p = self.right
        while p and p != self:
            if p.value != curr_value:
                values.append(f"{p.value}")
            else:
                values.append(f"({p.value})")
            p = p.right
        return " ".join(values)

    def size(self) -> int:
        result = 1
        p = self.right
        while p and p != self:
            result += 1
            p = p.right
        return result

    @classmethod
    def from_labels(cls, labels: str, size=0) -> "LinkedList":
        firstNode = LinkedList(int(labels[0]))
        lastNode = firstNode
        for ch in labels[1:]:
            node = LinkedList(int(ch))
            node.left = lastNode
            lastNode.right = node
            lastNode = node

        for value in range(len(labels)+1, size+1):
            node = LinkedList(value)
            node.left = lastNode
            lastNode.right = node
            lastNode = node

        node.right = firstNode
        firstNode.left = node
        return firstNode

    def cut(self, ncut: int) -> "LinkedList":
        if ncut < 1:
            return None
        result = self.right
        result.left = None
        p = result
        for _ in range(ncut-1):
            if not p or p.right == self:
                break
            p = p.right
        after = p.right
        p.right = None
        after.left = self
        self.right = after
        return result

    def insert(self, fragment: "LinkedList"):
        after = self.right
        self.right = fragment
        fragment.left = self
        p = fragment.right
        while p.right and p.right != fragment:
            p = p.right
        p.right = after
        after.left = p


def play_game(cups: LinkedList, moves: int) -> LinkedList:
    curr = cups
    ncup = cups.size()

    node = dict()
    node[curr.value] = curr
    p = curr.right
    while p != curr:
        node[p.value] = p
        p = p.right

    for move in range(moves):
        three = curr.cut(3)

        if curr.value > 1:
            destVal = curr.value - 1
        else:
            destVal = ncup
        while (destVal == three.value or 
               destVal == three.right.value or
               destVal == three.right.right.value):
            if destVal > 1:
                destVal = destVal - 1
            else:
                destVal = ncup

        dest = node[destVal]
        dest.insert(three)
        curr = curr.right
    return node[1]

def solve(labels: str, moves: int) -> str:
    """Solve the problem."""
    cups = LinkedList.from_labels(labels)
    final = play_game(cups, moves)
    result = str(final).replace(" ", "")[1:]
    return result

def solve2(labels: str, moves: int = 10000000) -> int:
    """Solve the problem."""
    cups = LinkedList.from_labels(labels, size=1000000)
    assert cups.size() == 1000000
    final = play_game(cups, 10000000)
    result = final.right.value * final.right.right.value
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
    result = solve2(arg[0])
    expected = 149245887792
    print(f"'{arg}' -> {result} (expected {expected})")
    assert result == expected
    print("= " * 32)

def part2():
    print("PART 2:")
    result = solve2(INPUT[0])
    print(f"result is {result}")
    print("= " * 32)



if __name__ == "__main__":
    example1()
    part1()
    example2()
    part2()
