#!/usr/bin/env python
from collections import Counter
import re

regex = re.compile(r"^(\d+),(\d+) -> (\d+),(\d+)")


def parse_line(line):
    x1, y1, x2, y2 = (int(n) for n in regex.match(line).groups())
    return x1, y1, x2, y2


def main():
    grid = Counter()
    lines = read_input()
    for line in lines:
        x1, y1, x2, y2 = parse_line(line)
        if x1 == x2:
            # vertical line
            j1, j2 = sorted([y1, y2])
            grid.update((x1, y) for y in range(j1, j2 + 1))
        elif y1 == y2:
            # horizontal line
            i1, i2 = sorted([x1, x2])
            grid.update((x, y1) for x in range(i1, i2 + 1))
        else:
            # diagonal line
            pass
    intersected_points = [key for key, count in grid.items() if count > 1]
    print(len(intersected_points))


def read_input() -> list[str]:
    with open("day05.txt") as f:
        return f.readlines()


if __name__ == "__main__":
    main()
