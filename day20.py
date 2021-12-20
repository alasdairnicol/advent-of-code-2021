#!/usr/bin/env python
from typing import Mapping, Tuple

Point = Tuple[int, int]
Points = Mapping[Point, str]


def parse_input(input_string: str) -> Tuple[str, Points]:
    algorithm, grid_string = input_string.split("\n\n")

    points = {}
    for j, line in enumerate(grid_string.split("\n")):
        for i, val in enumerate(line):
            points[(i, j)] = val

    return algorithm, points


def get_pixels(x: int, y: int) -> list[Point]:
    return [
        (x - 1, y - 1),
        (x + 0, y - 1),
        (x + 1, y - 1),
        (x - 1, y + 0),
        (x + 0, y + 0),
        (x + 1, y + 0),
        (x - 1, y + 1),
        (x + 0, y + 1),
        (x + 1, y + 1),
    ]


def enhance(points: Points, algorithm: str, default: str) -> Tuple[Points, str]:
    new_points = {}
    min_x = min(x for x, y in points.keys())
    max_x = max(x for x, y in points.keys())
    min_y = min(y for x, y in points.keys())
    max_y = max(y for x, y in points.keys())

    for x in range(min_x - 1, max_x + 2):
        for y in range(min_y - 1, max_y + 2):
            pixels = get_pixels(x, y)
            pixel_values = [points.get(p, default) for p in pixels]
            binary_number = int(
                "".join("1" if p == "#" else "0" for p in pixel_values), 2
            )
            new_value = algorithm[binary_number]
            new_points[(x, y)] = new_value

    default_pixel_values = [default] * 9
    binary_number = int(
        "".join("1" if p == "#" else "0" for p in default_pixel_values), 2
    )
    default = algorithm[binary_number]

    return new_points, default


def repeated_enhance(points: Points, algorithm: str, num_times: int) -> int:
    default = "."
    for x in range(num_times):
        points, default = enhance(points, algorithm, default)

    return len([v for v in points.values() if v == "#"])


def main():
    algorithm, points = parse_input(read_input())
    # To start with, every other point is off
    default = "."

    part_1 = repeated_enhance(points, algorithm, 2)
    print(f"{part_1=}")

    part_2 = repeated_enhance(points, algorithm, 50)
    print(f"{part_2=}")


def read_input() -> str:
    with open("day20.txt") as f:
        return f.read().strip()


if __name__ == "__main__":
    main()
