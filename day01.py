#!/usr/bin/env python
import itertools


def main():
    depths = list(read_input())
    part_a = num_increasing_values(depths)
    part_b = num_increasing_values(depths, window_length=3)
    print(f"{part_a=}")
    print(f"{part_b=}")


def num_increasing_values(depths, window_length=1):
    """
    We don't need to sum the sliding window. For a sliding window of
    length i, just count the number of positions x for which
    depth[x+i] > depth[x]

    To see this, consider a sliding window of length 3:

    199 A
    200 A B
    208 A B C
    210   B C
    ...

    Comparing A = [199, 200, 208] with B = [200, 208, 210], both lists
    contain 200 and 208, so we only need to compare 199 and 210.
    """
    return sum(1 if b > a else 0 for a, b in zip(depths, depths[window_length:]))


def read_input():
    with open("day01.txt") as f:
        return (int(x) for x in f.readlines())


if __name__ == "__main__":
    main()
