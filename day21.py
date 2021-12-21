#!/usr/bin/env python
from collections import Counter
from dataclasses import dataclass
from itertools import cycle, product
from typing import Mapping, Iterator, Tuple


@dataclass
class Universe:
    positions: Tuple[int, int]
    scores: Tuple[int, int]
    player_1_next: bool

    def __hash__(self):
        return hash((self.positions, self.scores, self.player_1_next))


def roll(dice: Iterator[int]) -> int:
    return sum([next(dice), next(dice), next(dice)])


def calc_distribution(values: list[int], num_rolls: int) -> Mapping[int, int]:
    distribution: Mapping[int, int] = Counter()
    return Counter(sum(dice) for dice in product(values, repeat=num_rolls))


def main():
    lines = read_input()
    starting_pos_1 = int(lines[0].strip().rsplit(" ", 1)[1])
    starting_pos_2 = int(lines[1].strip().rsplit(" ", 1)[1])

    part_1 = do_part_1(starting_pos_1, starting_pos_2)
    print(f"{part_1=}")

    part_2 = do_part_2(starting_pos_1, starting_pos_2)
    print(f"{part_2=}")


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


def do_part_2(starting_pos_1: int, starting_pos_2: int) -> int:
    target_score = 21
    distribution = calc_distribution([1, 2, 3], 3)

    winning_universes = [0, 0]

    universe = Universe(
        (starting_pos_1, starting_pos_2),
        (0, 0),
        True,
    )

    universes = Counter([universe])

    while universes:
        # FIXME try choosing a better universe to process e.g. lowest score
        universe = list(universes.keys())[0]
        count = universes.pop(universe)

        for roll, distribution_count in distribution.items():
            new_pos = universe.positions[0] + roll
            if new_pos > 10:
                new_pos = new_pos % 10
            new_score = universe.scores[0] + new_pos
            new_count = count * distribution_count

            if new_score >= target_score:
                if universe.player_1_next:
                    winning_universes[0] += new_count
                else:
                    winning_universes[1] += new_count

            else:
                new_universe = Universe(
                    (universe.positions[1], new_pos),
                    (universe.scores[1], new_score),
                    not universe.player_1_next,
                )
                universes.update({new_universe: new_count})

    return max(winning_universes)


def read_input() -> list[str]:
    with open("day21.txt") as f:
        return f.readlines()


if __name__ == "__main__":
    main()
