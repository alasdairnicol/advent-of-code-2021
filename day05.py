#!/usr/bin/env python
from collections import Counter
from typing import Mapping, Tuple
import re

EndPoints = Tuple[Tuple[int, int], Tuple[int, int]]

regex = re.compile(r"^(\d+),(\d+) -> (\d+),(\d+)")


def parse_line(line: str) -> EndPoints:
    m = regex.match(line)
    if not m:
        raise ValueError(f"Failed to match line {line}")
    x1, y1, x2, y2 = (int(n) for n in m.groups())
    return (x1, y1), (x2, y2)


def main():
    lines = [parse_line(line) for line in read_input()]
    part_a = do_part_a(lines)
    part_b = do_part_b(lines)
    print(f"{part_a=}")
    print(f"{part_b=}")


def do_part_a(lines: list[EndPoints]) -> int:
    grid = calc_grid(lines, include_diagonals=False)
    intersected_points = [key for key, count in grid.items() if count > 1]
    return len(intersected_points)


def do_part_b(lines: list[EndPoints]) -> int:
    grid = calc_grid(lines, include_diagonals=True)
    intersected_points = [key for key, count in grid.items() if count > 1]
    return len(intersected_points)


def calc_grid(lines: list[EndPoints], include_diagonals: bool) -> Mapping:
    grid: Counter = Counter()

    for (x1, y1), (x2, y2) in lines:
        if x1 < x2:
            x_step = 1
        elif x1 == x2:
            x_step = 0
        else:
            x_step = -1

        if y1 < y2:
            y_step = 1
        elif y1 == y2:
            y_step = 0
        else:
            y_step = -1

        if (x_step != 0 and y_step != 0) and not include_diagonals:
            # Skip diagonal line
            continue

        length = max(abs(n) for n in (x2 - x1, y2 - y1))

        grid.update((x1 + n * x_step, y1 + n * y_step) for n in range(length + 1))
    return grid


def read_input() -> list[str]:
    with open("day05.txt") as f:
        return f.readlines()


if __name__ == "__main__":
    main()
