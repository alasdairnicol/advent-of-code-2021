#!/usr/bin/env python
from collections import Counter


def main():
    fish = read_input()
    part_a = calc_fish_after_days(fish, 80)
    part_b = calc_fish_after_days(fish, 256)
    print(f"{part_a=}")
    print(f"{part_b=}")


def do_day(totals: dict[int, int]) -> dict[int, int]:
    new = {k - 1: v for k, v in totals.items()}
    negs = new.pop(-1, 0)
    if negs:
        new[6] = new.get(6, 0) + negs
        new[8] = negs

    return new


def calc_fish_after_days(fish: list[int], days: int) -> int:
    totals = dict(Counter(fish))

    for _ in range(days):
        totals = do_day(totals)

    return sum(totals.values())


def read_input() -> list[int]:
    with open("day06.txt") as f:
        return [int(x) for x in f.read().split(",")]


if __name__ == "__main__":
    main()
