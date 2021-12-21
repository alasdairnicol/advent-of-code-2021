#!/usr/bin/env python
from os import read
from itertools import cycle
from typing import Mapping, Iterator


def roll(dice: Iterator[int]) -> int:
    return sum([next(dice), next(dice), next(dice)])


def main():
    lines = read_input()
    starting_pos_1 = int(lines[0].strip().rsplit(" ", 1)[1])
    starting_pos_2 = int(lines[1].strip().rsplit(" ", 1)[1])

    part_1 = do_part_1(starting_pos_1, starting_pos_2)
    print(f"{part_1=}")

    # part_2 = 10
    # print(f"{part_2=}")


def do_part_1(starting_pos_1: int, starting_pos_2: int) -> int:
    positions = [starting_pos_1, starting_pos_2]
    scores = [0, 0]

    dice = cycle(range(1, 101))
    roll_count = 0

    while True:
        new_pos = positions[0] + roll(dice)
        roll_count += 3
        if new_pos > 10:
            new_pos = new_pos % 10

        positions[0] = new_pos
        scores[0] += new_pos

        if scores[0] >= 1000:
            break

        positions = list(reversed(positions))
        scores = list(reversed(scores))

    losing_score = scores[1]

    return roll_count * losing_score


def read_input() -> list[str]:
    with open("day21.txt") as f:
        return f.readlines()


if __name__ == "__main__":
    main()
