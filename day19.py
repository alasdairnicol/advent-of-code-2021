#!/usr/bin/env python
from dataclasses import dataclass
from functools import reduce
import itertools
from typing import Optional, Tuple

Beacon = Tuple[int, int, int]
ScannerPosition = Tuple[int, int, int]

directions = [
    # facing x
    lambda x, y, z: (x, y, z),
    # facing -x
    lambda x, y, z: (-x, -y, z),
    # facing y
    lambda x, y, z: (y, -x, z),
    # facing -y
    lambda x, y, z: (-y, x, z),
    # facing z
    lambda x, y, z: (z, y, -x),
    # facing -z
    lambda x, y, z: (-z, y, x),
]

rotations = [
    # 0 deg
    lambda x, y, z: (x, y, z),
    # 90 deg
    lambda x, y, z: (x, -z, y),
    # 180 deg
    lambda x, y, z: (x, -y, -z),
    # 270 deg
    lambda x, y, z: (x, z, -y),
]

# Generate 24 transforms from 4 rotations around x axis * 6 directions (±x, ±y ±z)
transforms = [
    lambda x, y, z, r=r, d=d: d(*r(x, y, z)) for r in rotations for d in directions
]


@dataclass
class Scanner:
    relative_beacons: set[Beacon]
    absolute_beacons: set[Beacon]
    position: ScannerPosition


def parse_scanner(scanner_input: str) -> set[Beacon]:
    return set(
        tuple(int(x) for x in line.split(","))  # type: ignore
        for line in scanner_input.strip().split("\n")[1:]
    )


def compare_beacons(
    absolute_beacons: set[Beacon], relative_beacons: set[Beacon]
) -> Optional[Scanner]:
    """
    Compare a set of absolute_beacons with a set of relative_beacons.

    Apply transformations to the relative beacons, and if we manage to
    find a suitable transformation, return the matched Scanner instance.
    """
    for t in transforms:
        transformed_points = {t(x1, x2, x3) for (x1, x2, x3) in relative_beacons}

        for x0, y0, z0 in absolute_beacons:
            for xt, yt, zt in transformed_points:
                # translation vector
                (x, y, z) = (x0 - xt, y0 - yt, z0 - zt)
                translated_points = {
                    (x + t1, y + t2, z + t3) for t1, t2, t3 in transformed_points
                }
                if len(translated_points & absolute_beacons) >= 12:
                    return Scanner(
                        relative_beacons,
                        translated_points,
                        (x, y, z),
                    )
    return None


def assemble_scanners(
    beacons_dict: dict[int, set[Beacon]], debug: bool = False
) -> list[Scanner]:
    """
    Take a beacons dict containing relative positions of beacons
    and return a list of scanners with their position and absolute
    positions of beacons.
    """
    beacons_0 = beacons_dict.pop(0)

    scanner_0 = Scanner(beacons_0, beacons_0, (0, 0, 0))

    results = [scanner_0]

    queue = [beacons_0]

    while queue:
        known_beacons = queue.pop()

        for k, relative_beacons in list(beacons_dict.items()):
            if scanner := compare_beacons(known_beacons, relative_beacons):
                results.append(scanner)
                if debug:
                    print(f"matched {k}")
                beacons_dict.pop(k)
                queue.append(scanner.absolute_beacons)

    return results


def do_part_1(scanners: list[Scanner]) -> int:
    all_points = reduce(
        lambda x, y: x | y, [scanner.absolute_beacons for scanner in scanners]
    )
    return len(all_points)


def manhattan_distance(a: Beacon, b: Beacon) -> int:
    return abs(a[0] - b[0]) + abs(a[1] - b[1]) + abs(a[2] - b[2])


def do_part_2(scanners: list[Scanner]) -> int:
    return max(
        manhattan_distance(a.position, b.position)
        for a, b in itertools.combinations(scanners, 2)
    )


def main():
    beacons_dict = {i: parse_scanner(x) for i, x in enumerate(read_input())}

    scanners = assemble_scanners(beacons_dict)

    part_1 = do_part_1(scanners)
    print(f"{part_1=}")

    part_1 = do_part_2(scanners)
    print(f"{part_1=}")


def read_input() -> list[str]:
    with open("day19.txt") as f:
        return f.read().split("\n\n")


if __name__ == "__main__":
    main()
