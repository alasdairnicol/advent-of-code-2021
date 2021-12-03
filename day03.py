#!/usr/bin/env python
import itertools


def main():
    lines = read_input()
    numbers = [int(line, 2) for line in lines]
    num_bits = max(len(line.strip()) for line in lines)

    part_a = do_part_a(numbers, num_bits)
    part_b = do_part_b(numbers, num_bits)
    print(f"{part_a=}")
    print(f"{part_b=}")


def do_part_a(numbers: list[int], num_bits: int) -> int:
    gamma = sum(get_gamma_bit(numbers, bit) * 2 ** bit for bit in range(num_bits))
    epsilon = gamma ^ 2 ** num_bits - 1
    return gamma * epsilon


def do_part_b(numbers: list[int], num_bits: int) -> int:
    o2 = get_gas_number(numbers, num_bits, o2=True)
    co2 = get_gas_number(numbers, num_bits, o2=False)
    print(o2, co2)
    return o2 * co2


def get_gas_number(numbers, num_bits, o2=True):
    bit = num_bits

    while len(numbers) > 1:
        bit -= 1
        gamma_bit = get_gamma_bit(numbers, bit)
        if bool(gamma_bit) ^ o2:
            numbers = [x for x in numbers if x & 2 ** bit]
        else:
            numbers = [x for x in numbers if x & 2 ** bit ^ 2 ** bit]

    return numbers[0]


def get_gamma_bit(numbers: list[int], bit: int) -> int:
    num_ones = len([x for x in numbers if x & 2 ** bit])
    if num_ones >= len(numbers) - num_ones:
        return 1
    else:
        return 0


def read_input() -> list[str]:
    with open("day03.txt") as f:
        return f.readlines()


if __name__ == "__main__":
    main()
