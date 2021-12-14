#!/usr/bin/env python
from collections import Counter
from dataclasses import dataclass
from typing import Literal, Tuple


def parse_rules(lines):
    return


def main():

    lines = read_input()
    template = lines[0].strip()
    rules = dict(line.strip().split(" -> ") for line in lines[2:])

    part_1 = do_part_1(template, rules)
    print(f"{part_1=}")

    # part_2 = do_part_2(template, rules)
    # print(f"{part_2=}")


def do_turn(polymer: str, rules: dict) -> str:
    out = polymer[0]
    for x, y in zip(polymer, polymer[1:]):
        out += rules.get(f"{x}{y}", "")
        out += y
    return out


def do_part_1(polymer, rules) -> int:
    for i in range(10):
        polymer = do_turn(polymer, rules)

    counter: Counter = Counter(polymer)
    counts = counter.most_common()
    most = counts[0][1]
    least = counts[-1][1]
    return most - least


def do_part_2(polymer, rules) -> int:
    return 0


def read_input() -> list[str]:
    with open("day14.txt") as f:
        return f.readlines()


if __name__ == "__main__":
    main()
