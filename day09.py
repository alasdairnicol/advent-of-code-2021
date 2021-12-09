#!/usr/bin/env python
import math
from typing import Mapping, Tuple

Point = Tuple[int, int]
Grid = Mapping[Point, int]


def main():
    lines = read_input()
    rows = [[int(x) for x in line.strip()] for line in lines]

    grid = {}
    for j, row in enumerate(rows):
        for i, height in enumerate(row):
            grid[(i, j)] = height

    part_a = do_part_a(grid)
    part_b = do_part_b(grid)
    print(f"{part_a=}")
    print(f"{part_b=}")


def neighbours(x: int, y: int) -> set[Point]:
    return {
        (x, y + 1),
        (x + 1, y),
        (x, y - 1),
        (x - 1, y),
    }


def get_basin(grid: Grid, x: int, y: int) -> set[Point]:
    basin = set()
    queue = [(x, y)]
    while queue:
        (x, y) = queue.pop()
        basin.add((x, y))
        queue.extend(
            [n for n in neighbours(x, y) if grid.get(n, 9) < 9 and n not in basin]
        )

    return basin


def get_lowest_points(grid: Grid) -> set[Point]:
    return {
        (x, y)
        for (x, y) in grid
        if grid[(x, y)] < min([grid.get((x, y), 10) for (x, y) in neighbours(x, y)])
    }


def do_part_a(grid: Grid) -> int:
    lowest_points = get_lowest_points(grid)
    risk_level = sum([grid[(x, y)] + 1 for (x, y) in lowest_points])
    return risk_level


def do_part_b(grid: Grid) -> int:
    lowest_points = get_lowest_points(grid)
    basin_sizes = [len(get_basin(grid, x, y)) for (x, y) in lowest_points]
    return math.prod(sorted(basin_sizes, reverse=True)[:3])


def read_input() -> list[str]:
    with open("day09.txt") as f:
        return f.readlines()


if __name__ == "__main__":
    main()
