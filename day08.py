#!/usr/bin/env python
def main():
    lines = read_input()
    part_a = do_part_a(lines)
    part_b = do_part_b(lines)
    print(f"{part_a=}")
    print(f"{part_b=}")


def do_part_a(lines: list[str]) -> int:
    output_digits = [line.split(" | ")[1].split() for line in lines]

    num_unique_digits = [
        len([d for d in digits if len(d) in (2, 3, 4, 7)]) for digits in output_digits
    ]

    return sum(num_unique_digits)


def calc_signal_output(line: str) -> int:
    digits = {}  # map digits to sets of segments

    signal_str, output_str = line.split(" | ")
    signal = {frozenset(x) for x in signal_str.split()}

    two_segments = [x for x in signal if len(x) == 2]
    three_segments = [x for x in signal if len(x) == 3]
    four_segments = [x for x in signal if len(x) == 4]
    five_segments = [x for x in signal if len(x) == 5]
    six_segments = [x for x in signal if len(x) == 6]
    seven_segments = [x for x in signal if len(x) == 7]

    # Digits with a unique number of segements
    digits[1] = two_segments[0]
    digits[4] = four_segments[0]
    digits[7] = three_segments[0]
    digits[8] = seven_segments[0]

    # Nine contains all the segments of four
    digits[9] = next(x for x in six_segments if digits[4] < x)

    # Zero contains same segments as one and is not nine
    digits[0] = next(x for x in six_segments if digits[1] < x and x != digits[9])

    # Six is the last number with six segments
    digits[6] = next(x for x in six_segments if x not in (digits[0], digits[9]))

    # Three contains all the segements of one
    digits[3] = next(x for x in five_segments if digits[1] < x)

    # Five is contained by six
    digits[5] = next(x for x in five_segments if x < digits[6])

    # Two is the last digit  with five segments
    digits[2] = next(x for x in five_segments if x not in (digits[3], digits[5]))

    segments_to_digits = {v: k for k, v in digits.items()}

    output_digits = [segments_to_digits[frozenset(x)] for x in output_str.split()]

    output = sum([x * y for x, y in zip(output_digits, [1000, 100, 10, 1])])
    return output


def do_part_b(lines: list[str]) -> int:
    return sum([calc_signal_output(line) for line in lines])


def read_input() -> list[str]:
    with open("day08.txt") as f:
        return f.readlines()


if __name__ == "__main__":
    main()
