#!/usr/bin/env python
from dataclasses import dataclass
from typing import Mapping, Tuple, Literal

Point = Tuple[int, int]


@dataclass
class Turn:
    easts: set[Point]
    souths: set[Point]
    width: int
    height: int
    count: int = 0

    def __eq__(self, other) -> bool:
        return (
            isinstance(other, Turn)
            and self.easts == other.easts
            and self.souths == other.souths
        )

    def next_turn(self) -> "Turn":
        occupied = self.easts | self.souths
        new_easts = {
            ((x + 1) % self.width, y)
            if ((x + 1) % self.width, y) not in occupied
            else (x, y)
            for (x, y) in self.easts
        }
        occupied = new_easts | self.souths
        new_souths = {
            (x, (y + 1) % self.height)
            if (x, (y + 1) % self.height) not in occupied
            else (x, y)
            for (x, y) in self.souths
        }

        return Turn(new_easts, new_souths, self.width, self.height, self.count + 1)

    def get_val(self, i: int, j: int) -> Literal[">", "v", "."]:
        if (i, j) in self.easts:
            return ">"
        elif (i, j) in self.souths:
            return "v"
        else:
            return "."

    def as_string(self) -> str:
        return "\n".join(
            "".join(self.get_val(i, j) for i in range(self.width))
            for j in range(self.height)
        )

    @classmethod
    def from_lines(cls, lines: list[str]) -> "Turn":
        easts = set()
        souths = set()
        for j, line in enumerate(lines):
            for i, val in enumerate(line.strip()):
                if val == ">":
                    easts.add((i, j))
                elif val == "v":
                    souths.add((i, j))

        return cls(easts, souths, len(lines[0].strip()), len(lines), 0)


def do_part_b() -> None:
    """There's no part 2 today!"""
    return None


def main():
    lines = read_input()

    part_a = do_part_a(lines)
    print(f"{part_a=}")

    do_part_b()


def do_part_a(lines) -> int:
    previous_turn = None
    turn = Turn.from_lines(lines)

    while previous_turn != turn:
        previous_turn, turn = turn, turn.next_turn()

    return turn.count


def read_input() -> list[str]:
    with open("day25.txt") as f:
        return f.readlines()


if __name__ == "__main__":
    main()
