#!/usr/bin/env python
from collections import Counter
from typing import Mapping, Tuple

Point = Tuple[int, int]
Grid = Mapping[Point, int]


def make_grid(lines: list[list[int]], repeat=1) -> Grid:
    num_lines = len(lines)
    grid = {}
    for j, line in enumerate(lines):
        for i, x in enumerate(line):
            for x_repeat in range(repeat):
                for y_repeat in range(repeat):
                    val = x + x_repeat + y_repeat
                    if val > 9:
                        val -= 9
                    grid[(i + num_lines * x_repeat, j + num_lines * y_repeat)] = val

    return grid


def get_neighbours(point: Point) -> list[Point]:
    x, y = point
    return [
        (x, y + 1),
        (x + 1, y),
        (x, y - 1),
        (x - 1, y),
    ]


def main():

    lines = read_input()
    grid_1 = make_grid(lines)
    part_1 = calc_minimum_risk(grid_1)
    print(f"{part_1=}")

    grid_2 = make_grid(lines, repeat=5)
    part_2 = calc_minimum_risk(grid_2)
    print(f"{part_2=}")


def calc_minimum_risk(grid: Grid) -> int:
    minimum_costs = {
        (0, 0): 0,
    }

    todo = {(0, 0)}

    while todo:
        point = todo.pop()
        cost = minimum_costs[point]

        for neighbour in get_neighbours(point):

            risk = grid.get(neighbour)
            if risk is None:
                continue

            if neighbour not in minimum_costs or cost + risk < minimum_costs[neighbour]:
                minimum_costs[neighbour] = cost + risk
                todo.add(neighbour)

    max_x = max([x for x, y in grid])
    max_y = max_x  # specified in question
    return minimum_costs[(max_x, max_y)]


def read_input() -> list[list[int]]:
    with open("day15.txt") as f:
        return [[int(x) for x in line.strip()] for line in f.readlines()]


if __name__ == "__main__":
    main()
