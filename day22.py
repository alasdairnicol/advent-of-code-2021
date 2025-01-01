#!/usr/bin/env python
from dataclasses import dataclass
import itertools
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

    def volume(self) -> int:
        return (
            (self.x_max + 1 - self.x_min)
            * (self.y_max + 1 - self.y_min)
            * (self.z_max + 1 - self.z_min)
        )


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

    part_2 = do_part_2(cuboids)
    print(f"{part_2=}")


def is_overlapping(c1: Cuboid, c2: Cuboid) -> bool:
    return (
        any(
            [
                (c2.x_min <= c1.x_min <= c2.x_max),
                (c2.x_min <= c1.x_max <= c2.x_max),
                (c1.x_min <= c2.x_min <= c1.x_max),
                (c1.x_min <= c2.x_min <= c1.x_max),
            ]
        )
        and any(
            [
                (c2.y_min <= c1.y_min <= c2.y_max),
                (c2.y_min <= c1.y_max <= c2.y_max),
                (c1.y_min <= c2.y_min <= c1.y_max),
                (c1.y_min <= c2.y_min <= c1.y_max),
            ]
        )
        and any(
            [
                (c2.z_min <= c1.z_min <= c2.z_max),
                (c2.z_min <= c1.z_max <= c2.z_max),
                (c1.z_min <= c2.z_min <= c1.z_max),
                (c1.z_min <= c2.z_min <= c1.z_max),
            ]
        )
    )


def subtract(c1: Cuboid, c2: Cuboid) -> list[Cuboid]:
    xs = sorted([c1.x_min, c1.x_max + 1, c2.x_min, c2.x_max + 1])
    x_ranges = [(x1, x2 - 1) for x1, x2 in zip(xs, xs[1:]) if x1 != x2]

    ys = sorted([c1.y_min, c1.y_max + 1, c2.y_min, c2.y_max + 1])
    y_ranges = [(y1, y2 - 1) for y1, y2 in zip(ys, ys[1:]) if y1 != y2]

    zs = sorted([c1.z_min, c1.z_max + 1, c2.z_min, c2.z_max + 1])
    z_ranges = [(z1, z2 - 1) for z1, z2 in zip(zs, zs[1:]) if z1 != z2]

    out = []

    for (x1, x2), (y1, y2), (z1, z2) in itertools.product(x_ranges, y_ranges, z_ranges):

        in_c1 = all(
            [
                c1.x_min <= x1,
                c1.x_max >= x2,
                c1.y_min <= y1,
                c1.y_max >= y2,
                c1.z_min <= z1,
                c1.z_max >= z2,
            ]
        )
        in_c2 = all(
            [
                c2.x_min <= x1,
                c2.x_max >= x2,
                c2.y_min <= y1,
                c2.y_max >= y2,
                c2.z_min <= z1,
                c2.z_max >= z2,
            ]
        )

        if in_c1 and not in_c2:
            out.append(
                Cuboid(
                    True,
                    x1,
                    x2,
                    y1,
                    y2,
                    z1,
                    z2,
                )
            )
    return out


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


def do_part_2(cuboids: list[Cuboid]) -> int:

    total = 0

    for i, cuboid in enumerate(cuboids):
        if not cuboid.on:
            continue
        grid = [cuboid]
        for future_cuboid in cuboids[i + 1 :]:
            if not is_overlapping(cuboid, future_cuboid):
                continue
            new_grid = []
            for c in grid:
                remainder = subtract(c, future_cuboid)
                new_grid.extend(remainder)
            grid = new_grid

        total += sum(c.volume() for c in grid)

    return total


def read_input() -> list[str]:
    with open("day22.txt") as f:
        return f.readlines()


if __name__ == "__main__":
    main()
