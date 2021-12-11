#!/usr/bin/env python
from dataclasses import dataclass
import math
from typing import Mapping, Tuple

Point = Tuple[int, int]
GridMapping = Mapping[Point, int]


class Grid:
    def __init__(self, grid: GridMapping):
        self.grid = grid
        self.width = max(i for i, j in grid) + 1
        self.height = max(j for i, j in grid) + 1

    @classmethod
    def from_lines(cls, lines: list[str]):
        grid = {}
        rows = [[int(x) for x in line.strip()] for line in lines]
        for j, row in enumerate(rows):
            for i, height in enumerate(row):
                grid[(i, j)] = height

        return cls(grid)

    def as_string(self) -> str:
        return (
            "\n".join(
                " ".join(str(self.grid[(i, j)]) for i in range(self.width))
                for j in range(self.height)
            )
            + "\n"
        )

    def neighbours(self, x: int, y: int) -> set[Point]:
        points = {
            (x, y + 1),
            (x + 1, y + 1),
            (x + 1, y),
            (x + 1, y - 1),
            (x, y - 1),
            (x - 1, y - 1),
            (x - 1, y),
            (x - 1, y + 1),
        }
        return {p for p in points if p in self.grid}


def do_turn(grid: Grid) -> Tuple[Grid, int]:
    # Add one to everything
    new_grid = {k: v + 1 for k, v in grid.grid.items()}
    flashed = set()

    while flashing := {k for k, v in new_grid.items() if v > 9 and k not in flashed}:
        for x, y in flashing:
            for x, y in grid.neighbours(x, y):
                new_grid[x, y] += 1
        flashed |= flashing

    # Set flashed to zero
    for k in flashed:
        new_grid[k] = 0

    return Grid(new_grid), len(flashed)


def main():
    lines = read_input()
    grid = Grid.from_lines(lines)

    part_a = do_part_a(grid, debug=True)
    print(f"{part_a=}")


def do_part_a(grid: Grid, debug: bool = False) -> int:
    num_steps = 100
    total_flashes = 0

    for i in range(1, num_steps + 1):
        grid, flashes = do_turn(grid)
        total_flashes += flashes

        if debug and i % 10 == 0:
            print(f"After step {i}: {total_flashes} flashes")
            print(grid.as_string())

    return total_flashes


def do_part_b(grid: Grid) -> int:
    pass


def read_input() -> list[str]:
    with open("day11.txt") as f:
        return f.readlines()


if __name__ == "__main__":
    main()
