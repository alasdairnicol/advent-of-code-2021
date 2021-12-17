#!/usr/bin/env python
from dataclasses import dataclass
import math
import re
from typing import Tuple


def parse_line(line):
    return [
        int(x)
        for x in re.match(
            "target area: x=([\d-]+)..([\d-]+), y=([\d-]+)..([\d-]+)", line
        ).groups()
    ]


@dataclass
class Target:
    x_min: int
    x_max: int
    y_min: int
    y_max: int


def test(target: Target, v_x: int, v_y: int) -> Tuple[bool, int]:
    x, y = 0, 0
    highest = 0
    while x <= target.x_max and y >= target.y_min:
        x += v_x
        y += v_y
        if v_y > 0:
            highest = y
        v_x = max(v_x - 1, 0)
        v_y -= 1
        if target.x_min <= x <= target.x_max and target.y_min <= y <= target.y_max:
            return True, highest
    return False, 0


def main():
    line = read_input()
    target = Target(*parse_line(line))

    part_1 = do_part_1(target, debug=True)
    print(f"{part_1=}")

    part_2 = do_part_2(target)
    print(f"{part_2=}")


def do_part_1(target: Target, debug: bool = False) -> int:
    # On the last step, it goes from y=0 to y=y_min
    last_step = -target.y_min
    trial_y = last_step - 1
    part_1 = (trial_y) * (trial_y + 1) // 2

    # We have calculated the highest possible height, which occurs
    # when v_y = last_step - 1.
    # Lets find an x velocity that lands in the y part
    # by guess for x that solves x_min <= x(x+1)/2 <= x_max
    guess = math.floor(math.sqrt(target.x_min * 2))
    for trial_x in range(guess - 1, guess + 2):
        result, highest = test(target, trial_x, trial_y)
        if result is True and highest == part_1:
            # We found the velocity
            if debug:
                print(
                    f"Found velocity ({trial_x}, {trial_y}) that reaches highest possible position {highest}"
                )
            break
    else:
        raise ValueError("Didn't find a suitable x velocity")

    return part_1


def do_part_2(target: Target) -> int:
    count = 0
    for v_x in range(1, target.x_max + 1):
        for v_y in range(target.y_min, -target.y_min):
            if test(target, v_x, v_y)[0]:
                count += 1
    return count


def read_input() -> str:
    with open("day17.txt") as f:
        return f.read().strip()


if __name__ == "__main__":
    main()
