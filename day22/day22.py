#!/usr/bin/env python3
#
#  Advent of Code 2020 - day 22
#
from pathlib import Path

INPUTFILE = "input.txt"

SAMPLE_INPUT = """
Player 1:
9
2
6
3
1

Player 2:
5
8
4
7
10
"""


# Utility functions

def sample_input():
    return SAMPLE_INPUT.strip("\n").split("\n")

def load_input(infile):
    return [line.strip() for line in Path(infile).open()]

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


# Solution

class Player:

    def __init__(self, name, cards):
        assert isinstance(cards, list)
        self.name = name
        self.cards = cards

    @property
    def deck(self):
        return ",".join([str(card) for card in self.cards])

    @property
    def state(self):
        return (self.name, self.deck)

    def play_card(self):
        if not self.cards:
            return None
        card = self.cards.pop(0)
        return card

    def add_cards(self, *new_cards):
        self.cards.extend(new_cards)

    def has_cards(self):
        return bool(self.cards)

    @property
    def score(self):
        return sum([(i + 1) * v for i, v in enumerate(reversed(self.cards))])


def parse_input(lines):
    sects = parse_sections(lines)
    player1 = parse_player("Player1", sects[0])
    player2 = parse_player("Player2", sects[1])
    return player1, player2

def parse_player(name, lines):
    cards = []
    for line in lines:
        if line.startswith("Player"):
            continue
        if line:
            cards.append(int(line))
    return Player(name, cards)

def play_game(player1, player2, recursive=False, game=1):
    """Play out a single game of combat."""
    print(f"\nGAME {game}")
    history = set()
    round = 0
    while player1.has_cards() and player2.has_cards():
        round += 1
        print(f"-- Round {round} --")
        print(f"{player1.name}'s deck: {player1.deck}")
        print(f"{player2.name}'s deck: {player2.deck}")

        if recursive:
            if player1.state in history or player2.state in history:
                print(f"*** infinite game detected ***")
                winner = player1
                break
            history.add(player1.state)
            history.add(player2.state)

        card1 = player1.play_card()
        print(f"{player1.name} plays: {card1}")
        card2 = player2.play_card()
        print(f"{player2.name} plays: {card2}")
        assert card1 != card2

        if recursive:
            if len(player1.cards) >= card1 and len(player2.cards) >= card2:
                subgame_winner = play_game(
                    Player(player1.name, player1.cards[:card1]),
                    Player(player2.name, player2.cards[:card2]),
                    recursive,
                    game + 1
                )
                if subgame_winner.name == player1.name:
                    winner = player1
                else:
                    winner = player2
            elif card1 > card2:
                winner = player1
            else:
                winner = player2
        else:
            if card1 > card2:
                winner = player1
            else:
                winner = player2

        if winner.name == player1.name:
            winner.add_cards(card1, card2)
        else:
            winner.add_cards(card2, card1)

        print(f"{winner.name} wins round {round} of game {game}!")
        print()
    print(f"{winner.name} wins game {game}!")
    return winner

def solve(lines):
    """Solve the problem."""
    player1, player2 = parse_input(lines)
    winner = play_game(player1, player2)
    return winner.score

def solve2(lines):
    """Solve the problem."""
    player1, player2 = parse_input(lines)
    winner = play_game(player1, player2, recursive=True)
    return winner.score


# PART 1

def example1():
    """Run example for problem with input lines."""
    print("EXAMPLE 1:")
    lines = SAMPLE_INPUT.split("\n")
    result = solve(lines)
    expected = 306
    print(f"'sample-input' -> {result} (expected {expected})")
    assert result == expected
    print("= " * 32)


def part1(lines):
    print("PART 1:")
    result = solve(lines)
    print(f"result is {result}")
    print("= " * 32)


# PART 2

def example2():
    """Run example for problem with input lines."""
    print("EXAMPLE 2:")
    lines = SAMPLE_INPUT.split("\n")
    result = solve2(lines)
    expected = 291
    print(f"'sample-input' -> {result} (expected {expected})")
    assert result == expected
    print("= " * 32)


def part2(lines):
    print("PART 2:")
    result = solve2(lines)
    print(f"result is {result}")
    print("= " * 32)


if __name__ == "__main__":
    example1()
    lines = load_input(INPUTFILE)
    part1(lines)
    example2()
    part2(lines)
