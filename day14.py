#!/usr/bin/env python
from collections import Counter
from functools import cache


def main():

    lines = read_input()
    template = lines[0].strip()
    rules = dict(line.strip().split(" -> ") for line in lines[2:])

    part_1 = do_part_1(template, rules)
    print(f"{part_1=}")

    part_2 = do_part_2(template, rules)
    part_2_not_recursive = do_part_2_not_recursive(template, rules)
    assert part_2 == part_2_not_recursive
    print(f"{part_2=}")


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

    totals: Counter = Counter(polymer)
    counts = totals.most_common()
    most = counts[0][1]
    least = counts[-1][1]
    return most - least


def do_part_2(polymer, rules) -> int:
    num_steps = 40

    totals: Counter = Counter(polymer[-1:])

    # Define inline so we have access to rules
    @cache
    def count(x, y, num):
        if num == 0:
            return Counter([x])
        else:
            z = rules[x + y]
            return count(x, z, num - 1) + count(z, y, num - 1)

    for x, y in zip(polymer, polymer[1:]):
        totals += count(x, y, num_steps)

    counts = totals.most_common()
    most = counts[0][1]
    least = counts[-1][1]
    return most - least


def do_part_2_not_recursive(polymer, rules) -> int:
    num_steps = 40

    pairs = Counter(zip(polymer, polymer[1:]))

    for i in range(num_steps):
        new_pairs: Counter = Counter()
        for (x, y), num in pairs.items():
            z = rules[x + y]
            new_pairs[(x, z)] += num
            new_pairs[(z, y)] += num
        pairs = new_pairs

    totals: Counter = Counter(polymer[-1:])
    for (x, y), num in pairs.items():
        totals[x] += num

    counts = totals.most_common()
    most = counts[0][1]
    least = counts[-1][1]
    return most - least


def read_input() -> list[str]:
    with open("day14.txt") as f:
        return f.readlines()


if __name__ == "__main__":
    main()
