#!/usr/bin/env python
from dataclasses import dataclass, field
from itertools import zip_longest
from typing import Iterable


@dataclass
class BingoCard:
    numbers: list[int]
    seen: set[int] = field(default_factory=set)

    @property
    def rows(self) -> list[list[int]]:
        return list(grouper(self.numbers, 5))

    @property
    def columns(self) -> list[list[int]]:
        return [self.numbers[x:None:5] for x in range(5)]

    def is_finished(self) -> bool:
        return any(
            all(x in self.seen for x in line) for line in self.rows + self.columns
        )

    def mark_number(self, number: int) -> None:
        self.seen.add(number)

    def score(self, last_seen: int) -> int:
        unmarked_numbers = [x for x in self.numbers if x not in self.seen]
        return sum(unmarked_numbers) * last_seen


# From Itertools recipes in Python docs
# https://docs.python.org/3/library/itertools.html#itertools-recipes
def grouper(iterable, n, fillvalue=None) -> Iterable:
    "Collect data into non-overlapping fixed-length chunks or blocks"
    # grouper('ABCDEFG', 3, 'x') --> ABC DEF Gxx
    args = [iter(iterable)] * n
    return zip_longest(*args, fillvalue=fillvalue)


def generate_cards(lines: list[str]) -> list[BingoCard]:
    cards = []
    for card_lines in grouper(lines, 6, fillvalue=""):
        card_numbers = [int(x) for x in "".join(card_lines).split()]
        cards.append(BingoCard(card_numbers))
    return cards


def main():
    lines = read_input()
    numbers = [int(x) for x in lines[0].split(",")]
    cards = generate_cards(lines[2:])

    part_a = do_part_a(cards, numbers)
    part_b = do_part_b(cards, numbers)
    print(f"{part_a=}")
    print(f"{part_b=}")


def do_part_a(cards: list[BingoCard], numbers: list[int]) -> int:
    for n in numbers:
        for card in cards:
            card.mark_number(n)
            if card.is_finished():
                return card.score(n)
    raise AssertionError("Reached end of numbers without completing a card")


def do_part_b(cards: list[BingoCard], numbers: list[int]) -> int:
    completed_cards = []
    for n in numbers:
        for card in cards:
            if card not in completed_cards:
                card.mark_number(n)
                if card.is_finished():
                    completed_cards.append(card)
                    if len(completed_cards) == len(cards):
                        final_score = card.score(n)
                        return final_score
    raise AssertionError("Reached end of numbers without completing a card")


def read_input() -> list[str]:
    with open("day04.txt") as f:
        return f.readlines()


if __name__ == "__main__":
    main()
