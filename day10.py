#!/usr/bin/env python
from collections import defaultdict
from dataclasses import dataclass
from typing import Iterable, Union

closing = {
    ")": "(",
    "]": "[",
    "}": "{",
    ">": "<",
}

opening = {
    "(": ")",
    "[": "]",
    "{": "}",
    "<": ">",
}


illegal_scores = {
    ")": 3,
    "]": 57,
    "}": 1197,
    ">": 25137,
}


autocomplete_scores = {
    ")": 1,
    "]": 2,
    "}": 3,
    ">": 4,
}


@dataclass
class Error:
    char: str

    def score(self):
        return illegal_scores[self.char]


@dataclass
class Autocomplete:
    chars: str

    def score(self):
        total = 0
        for c in self.chars:
            total = 5 * total + autocomplete_scores[c]
        return total


def process_line(line: str) -> Union[Autocomplete, Error]:
    line = line.strip()
    stack = [""]
    for x in line:
        y = closing.get(x)
        if y:
            last = stack.pop()
            if y != last:
                return Error(x)
        else:
            stack.append(x)
    return Autocomplete("".join(opening[x] for x in reversed(stack[1:])))


def main():
    lines = read_input()
    processed = [process_line(line) for line in lines]
    part_a = do_part_a(processed)
    part_b = do_part_b(processed)
    print(f"{part_a=}")
    print(f"{part_b=}")


def do_part_a(processed: list[Union[Autocomplete, Error]]) -> int:
    scores = [x.score() for x in processed if isinstance(x, Error)]
    return sum(scores)


def do_part_b(processed: list[Union[Autocomplete, Error]]) -> int:
    scores = [x.score() for x in processed if isinstance(x, Autocomplete)]
    scores.sort()
    median = scores[len(scores) // 2]
    return median


def read_input() -> list[str]:
    with open("day10.txt") as f:
        return f.readlines()


if __name__ == "__main__":
    main()
