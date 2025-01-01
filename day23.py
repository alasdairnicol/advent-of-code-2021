#!/usr/bin/env python
from collections import Counter
from dataclasses import dataclass
import functools
from typing import Generator, NewType, Optional, Tuple


Amphipod = NewType("Amphipod", str)

amphipods = [
    Amphipod("A"),
    Amphipod("B"),
    Amphipod("C"),
    Amphipod("D"),
]

energy_costs = {
    "A": 1,
    "B": 10,
    "C": 100,
    "D": 1000,
}

Queue = Tuple[Amphipod, ...]
Queues = Tuple[Queue, ...]

TopRow: Tuple[Tuple[str, str], ...]

# Moves from space below hallway to each possible space in hallway
# spaces directly above rooms are excluded
initial_moves = (
    (
        "cba",
        "cb",
        "cd",
        "cdef",
        "cdefgh",
        "cdefghij",
        "cdefghijk",
    ),
    (
        "edcba",
        "edcb",
        "ed",
        "ef",
        "efgh",
        "efghij",
        "efghijk",
    ),
    (
        "gfedcba",
        "gfedcb",
        "gfed",
        "gf",
        "gh",
        "ghij",
        "ghijk",
    ),
    (
        "ihgfedcba",
        "ihgfedcb",
        "ihgfed",
        "ihgf",
        "ih",
        "ij",
        "ijk",
    ),
)

# Moves from hallway to space above room for each amphipod type
second_moves = {
    ("a", "A"): "bc",
    ("a", "B"): "bcde",
    ("a", "C"): "bcdefg",
    ("a", "D"): "bcdefghi",
    ("b", "A"): "c",
    ("b", "B"): "cde",
    ("b", "C"): "cdefg",
    ("b", "D"): "cdefghi",
    ("d", "A"): "c",
    ("d", "B"): "e",
    ("d", "C"): "efg",
    ("d", "D"): "efghi",
    ("f", "A"): "edc",
    ("f", "B"): "e",
    ("f", "C"): "g",
    ("f", "D"): "ghi",
    ("h", "A"): "gfedc",
    ("h", "B"): "gfe",
    ("h", "C"): "g",
    ("h", "D"): "i",
    ("j", "A"): "ihgfedc",
    ("j", "B"): "ihgfe",
    ("j", "C"): "ihg",
    ("j", "D"): "i",
    ("k", "A"): "jihgfedc",
    ("k", "B"): "jihgfe",
    ("k", "C"): "jihg",
    ("k", "D"): "ji",
}


def parse_input_queues(
    lines: list[str], extra_lines: Optional[list[str]] = None
) -> Queues:
    if extra_lines is None:
        extra_lines = []
    lines = [lines[2]] + extra_lines + [lines[3]]
    rows = [x.strip("\n #").split("#") for x in lines]
    queues = tuple(zip(*rows))
    queues = simplify_queues(queues)
    return queues


def simplify_queue(queue: Queue, letter: Amphipod) -> Queue:
    while queue and queue[-1] == letter:
        queue = queue[:-1]
    return queue


def simplify_queues(queues: Queues) -> Queues:
    queues = tuple(simplify_queue(q, letter) for q, letter in zip(queues, amphipods))
    return queues


@dataclass
class State:
    queues: tuple
    top_row: tuple = ()
    total_cost: int = 0

    def is_complete(self) -> bool:
        return not any(self.queues) and not self.top_row

    def possible_moves(self) -> Generator[Tuple["State", int], None, None]:
        top_row_filled = set(x for x, y in self.top_row)
        empty_queues = set(
            letter for letter, queue in zip(amphipods, self.queues) if not queue
        )

        # Can any amphipods get home?
        for position, letter in self.top_row:
            if letter in empty_queues:
                destination = second_moves[(position, letter)]
                if set(destination) & top_row_filled:
                    continue

                yield State(
                    self.queues,
                    tuple((x, y) for (x, y) in self.top_row if x != position),
                ), energy_costs[letter] * len(destination)
                # Early return, no point considering any other moves
                return

        # Moves from rooms to hallway
        for i, queue in enumerate(self.queues):
            if queue:
                letter = queue[0]
                possible_destinations = initial_moves[i]
                for destination in possible_destinations:
                    if set(destination) & top_row_filled:
                        continue

                    new_queues = tuple(
                        q[1:] if n == i else q for n, q in enumerate(self.queues)
                    )
                    yield State(
                        new_queues,
                        tuple(sorted(self.top_row + ((destination[-1], letter),))),
                    ), energy_costs[letter] * len(destination)

    def fixed_cost(self) -> int:
        """
        The fixed costs are those of moving the amphipods to the top row,
        and from the space directly above the room into the final position
        in the room.

        Assumes self.queues is simplified, so that we don't count
        energy costs for amphipods that don't have to be moved.
        """
        # Keep track of the number of steps moved for each amphipod type
        counts: dict[Amphipod, int] = Counter()

        # Count the number of moves to get every amphipod to the space below the top row
        for queue in self.queues:
            for i, amphipod in enumerate(queue):
                counts[amphipod] += i

        # Count the number of amphipods of each type
        for amphipod in amphipods:
            num = sum(q.count(amphipod) for q in self.queues)
            # Number of steps to fill room is the triangular number
            # e.g. 3 amphipods costs 3+2+1 to fill room.
            counts[amphipod] += num * (num + 1) // 2

        return sum(counts[amphipod] * energy_costs[amphipod] for amphipod in amphipods)


@functools.cache
def find_least_possible_energy(
    queues: Queue, top_row: Tuple[str, str]
) -> Optional[int]:
    """
    Find the least possible energy, excluding fixed costs
    """
    state = State(queues, top_row, 0)
    if state.is_complete():
        return 0

    best = None
    for new_state, energy_cost in state.possible_moves():
        # print(energy_cost)
        result = find_least_possible_energy(new_state.queues, new_state.top_row)
        if result is not None:
            # print(f"before {best=}, {result=}")
            if best is None:
                if energy_cost is None:
                    raise
                best = result + energy_cost
                # print(f"Changing best from None to {best=}")
            else:
                best = min(result + energy_cost, best)
            # print(f"after {best=}")

    return best


def find_least_possible_total_energy(queues: Queues) -> int:
    """
    Find the least possible energy, including fixed costs
    """
    s = State(queues)
    search = find_least_possible_energy(queues, ())
    if search is None:
        raise ValueError("Couldn't solve input")
    return search + s.fixed_cost()


def main():
    lines = read_input()

    queues_1 = parse_input_queues(lines)
    part_1 = find_least_possible_total_energy(queues_1)
    print(f"{part_1=}")

    extra_lines = [
        "#D#C#B#A#",
        "#D#B#A#C#",
    ]
    queues_2 = parse_input_queues(lines, extra_lines=extra_lines)
    part_2 = find_least_possible_total_energy(queues_2)
    print(f"{part_2=}")


def read_input() -> list[str]:
    with open("day23.txt") as f:
        return f.readlines()


if __name__ == "__main__":
    main()
