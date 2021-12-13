#!/usr/bin/env python
from dataclasses import dataclass
from typing import Literal, Tuple

Dot = tuple[int, int]
Dots = set[Dot]


@dataclass
class Fold:
    axis: str
    number: int


def parse_fold(line: str) -> Fold:
    word = line.rsplit(" ", maxsplit=1)[1]
    axis, line_number = word.split("=")
    return Fold(axis, int(line_number))


def parse_input(input_str: str) -> tuple[Dots, list[Fold]]:
    dots_str, folds_str = input_str.split("\n\n")
    dots = {
        (int(x), int(y)) for x, y in (line.split(",") for line in dots_str.split("\n"))
    }
    folds = [parse_fold(line) for line in folds_str.strip().split("\n")]
    return dots, folds


def fold_paper(dots: Dots, fold: Fold) -> Dots:
    return {fold_dot(dot, fold) for dot in dots}


def fold_dot(dot: Dot, fold: Fold) -> Dot:
    print
    if fold.axis == "x":
        new_dot = (
            dot[0] if dot[0] <= fold.number else 2 * fold.number - dot[0],
            dot[1],
        )
    else:
        new_dot = (
            dot[0],
            dot[1] if dot[1] <= fold.number else 2 * fold.number - dot[1],
        )
    return new_dot


def main():

    lines = read_input()
    dots, folds = parse_input(read_input())

    part_1 = do_part_1(dots, folds[0])
    print(f"{part_1=}")

    part_2 = do_part_2(dots, folds)
    print(f"part_2=\n{part_2}")


def do_part_1(dots: Dots, first_fold: Fold) -> int:
    dots = fold_paper(dots, first_fold)
    return len(dots)


def do_part_2(dots: Dots, folds: list[Fold]) -> str:
    for fold in folds:
        dots = fold_paper(dots, fold)

    x_min = min(x for (x, y) in dots)
    x_max = max(x for (x, y) in dots)
    y_min = min(y for (x, y) in dots)
    y_max = max(y for (x, y) in dots)

    return "\n".join(
        "".join("#" if (x, y) in dots else " " for x in range(x_min, x_max + 1))
        for y in range(y_min, y_max + 1)
    )


def read_input() -> str:
    with open("day13.txt") as f:
        return f.read()


if __name__ == "__main__":
    main()
