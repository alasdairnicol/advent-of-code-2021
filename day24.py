#!/usr/bin/env python
from functools import partial
from typing import Literal, Tuple, TypedDict

Key = Literal["w", "x", "y", "z"]
Commands = list[partial]
# map a score z to the lowest and highest digits that generate it
Turns = dict[int, list[tuple[int, ...]]]


class Variables(TypedDict):
    w: int
    x: int
    y: int
    z: int


def get_val(variables: Variables, val: str) -> int:
    try:
        return variables[val]  # type: ignore
    except KeyError:
        return int(val)


def add(a: Key, b: str, variables: Variables) -> None:
    b_val = get_val(variables, b)
    variables[a] += b_val


def multiply(a: Key, b: str, variables: Variables) -> None:
    b_val = get_val(variables, b)
    variables[a] *= b_val


def divide(a: Key, b: str, variables: Variables) -> None:
    b_val = get_val(variables, b)
    variables[a] //= b_val


def mod(a: Key, b: str, variables: Variables) -> None:
    b_val = get_val(variables, b)
    variables[a] %= b_val


def equal(a: Key, b: str, variables: Variables) -> None:
    a_val = get_val(variables, a)
    b_val = get_val(variables, b)
    variables[a] = 1 if a_val == b_val else 0


operations = {
    "add": add,
    "mul": multiply,
    "div": divide,
    "mod": mod,
    "eql": equal,
}


def process_commands(lines: list[str]) -> Commands:

    commands = [line.split() for line in lines]
    # Command 0 takes input
    assert commands[0] == ["inp", "w"]
    # Command 1 sets x to 0
    assert commands[1] == ["mul", "x", "0"]
    # Command 2 sets x to z
    assert commands[2] == ["add", "x", "z"]
    # Commands 3 to 7 do not use y
    for i in range(3, 8):
        assert "y" not in commands[i]
    # Command 8 sets y to 0
    assert commands[8] == ["mul", "y", "0"]

    actions = []

    # Skip the first three commands that set x and z
    for i, command in enumerate(commands[:]):
        # We can ignore these commands because we set
        # y=0 and x=z for every iteration
        if i in (0, 1, 2, 8):
            continue
        op, *args = command

        actions.append(partial(operations[op], *args))

    return actions


def calc_output(commands: Commands, w: int, z: int) -> Variables:
    variables: Variables = {
        "w": w,  # from input
        "x": z,  # instruction 2 in every group of commands
        "y": 0,  # instruction 8 in every group of commands
        "z": z,  # from previous digit
    }

    for command in commands:
        command(variables)

    return variables


def find_numbers(commands: list[Commands]) -> Tuple[int, int]:

    previous_turns: Turns = {
        # z value: lowest, highest
        0: [(), ()],
    }

    for i in range(14):
        turns: Turns = {}
        for w in range(1, 10):
            for z, (lowest, highest) in previous_turns.items():
                variables = calc_output(commands[i], w, z)
                if variables["z"] not in turns:
                    turns[variables["z"]] = [lowest + (w,), highest + (w,)]
                else:
                    turns[variables["z"]][1] = highest + (w,)

        previous_turns = turns

    lowest, highest = turns[0]  # type: ignore
    return int("".join(str(d) for d in lowest)), int("".join(str(d) for d in highest))


def main():
    lines = read_input()

    grouped_lines = [lines[x + 0 : x + 18] for x in range(0, len(lines), 18)]
    commands = [process_commands(g) for g in grouped_lines]

    part_b, part_a = find_numbers(commands)

    print(f"{part_a=}")
    print(f"{part_b=}")


def read_input() -> list[str]:
    with open("day24.txt") as f:
        return f.readlines()


if __name__ == "__main__":
    main()
