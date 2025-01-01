#!/usr/bin/env python
from collections import Counter


def main():
    numbers = read_input()
    part_a = calc_minimum(numbers, lambda n, x: abs(n - x))
    part_b = calc_minimum(numbers, lambda n, x: abs(n - x) * (abs(n - x) + 1) // 2)
    print(f"{part_a=}")
    print(f"{part_b=}")


def calc_minimum(numbers: list[int], func) -> int:
    n_min = min(numbers)
    n_max = max(numbers)

    return min(sum([func(n, x) for x in numbers]) for n in range(n_min, n_max + 1))


def read_input() -> list[int]:
    with open("day07.txt") as f:
        return [int(x) for x in f.read().split(",")]


if __name__ == "__main__":
    main()
