#!/usr/bin/env python


def main():
    lines = read_input()
    rows = [[int(x) for x in line.strip()] for line in lines]

    grid = {}
    for j, row in enumerate(rows):
        for i, height in enumerate(row):
            grid[(i, j)] = height

    part_a = do_part_a(grid)
    part_b = do_part_b(lines)
    print(f"{part_a=}")
    print(f"{part_b=}")


def neighbours(grid, x, y):
    """
    If item is on edge of grid, we can return 10
    """
    return [
        grid.get((x, y + 1), 10),
        grid.get((x + 1, y), 10),
        grid.get((x, y - 1), 10),
        grid.get((x - 1, y), 10),
    ]


def do_part_a(grid) -> int:
    total = 0
    lowest_points = [
        height
        for ((x, y), height) in grid.items()
        if height < min(neighbours(grid, x, y))
    ]
    risk_level = sum(lowest_points) + len(lowest_points)
    return risk_level


def do_part_b(grid) -> int:
    return 0


def read_input() -> list[str]:
    with open("day09.txt") as f:
        return f.readlines()


if __name__ == "__main__":
    main()
