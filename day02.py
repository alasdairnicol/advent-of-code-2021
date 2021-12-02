#!/usr/bin/env python
import itertools


def main():
    lines = read_input()
    part_a = do_part_a(lines)
    part_b = do_part_b(lines)
    print(f"{part_a=}")
    print(f"{part_b=}")


def do_part_a(lines: list[str]) -> int:
    horizontal, depth = 0, 0
    for line in lines:
        instruction, num_str = line.split()
        num = int(num_str)
        if instruction == "forward":
            horizontal += num
        elif instruction == "down":
            depth += num
        else:
            depth -= num

    return horizontal * depth


def do_part_b(lines: list[str]) -> int:
    horizontal, depth, aim = 0, 0, 0
    for line in lines:
        instruction, num_str = line.split()
        num = int(num_str)
        if instruction == "forward":
            horizontal += num
            depth += num * aim
        elif instruction == "down":
            aim += num
        else:
            aim -= num

    return horizontal * depth


def read_input() -> list[str]:
    with open("day02.txt") as f:
        return f.readlines()


if __name__ == "__main__":
    main()
