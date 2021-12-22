#!/usr/bin/env python
from dataclasses import dataclass
import re


@dataclass
class Cuboid:
    on: bool
    x_min: int
    x_max: int
    y_min: int
    y_max: int
    z_min: int
    z_max: int


def parse_line(line: str) -> Cuboid:
    if match := re.match(
        r"(on|off) x=(-?\d+)..(-?\d+),y=(-?\d+)..(-?\d+),z=(-?\d+)..(-?\d+)", line
    ):
        on = match.groups()[0] == "on"
        bounds = (int(x) for x in match.groups()[1:])
        return Cuboid(on, *bounds)
    else:
        raise ValueError("Invalid line")


def main():
    lines = read_input()

    cuboids = [parse_line(line) for line in lines]

    part_1 = do_part_1(cuboids)
    print(f"{part_1=}")

    part_2 = do_part_2()
    print(f"{part_2=}")


def do_part_1(cuboids: list[Cuboid]) -> int:
    grid = set()

    for cuboid in cuboids:
        for x in range(max([cuboid.x_min, -50]), min([cuboid.x_max, 50]) + 1):
            for y in range(max([cuboid.y_min, -50]), min([cuboid.y_max, 50]) + 1):
                for z in range(max([cuboid.z_min, -50]), min([cuboid.z_max, 50]) + 1):
                    if cuboid.on:
                        grid.add((x, y, z))
                    else:
                        grid -= {(x, y, z)}

    return len(grid)


def do_part_2() -> int:
    return 10


def read_input() -> list[str]:
    with open("day22.txt") as f:
        return f.readlines()


if __name__ == "__main__":
    main()
