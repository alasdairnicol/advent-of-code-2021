#!/usr/bin/env python
from dataclasses import dataclass, field
import math
from typing import Tuple


def hex_string_to_bits(hex_string: str) -> str:
    return "".join("{:04b}".format(int(x, 16)) for x in hex_string)


@dataclass
class Packet:
    version: int
    packet_type: int
    value: int = 0
    sub_packets: list = field(default_factory=list)

    def evaluate(self) -> int:
        if self.packet_type == 0:
            return sum(p.evaluate() for p in self.sub_packets)
        elif self.packet_type == 1:
            return math.prod(p.evaluate() for p in self.sub_packets)
        elif self.packet_type == 2:
            return min(p.evaluate() for p in self.sub_packets)
        elif self.packet_type == 3:
            return max(p.evaluate() for p in self.sub_packets)
        elif self.packet_type == 4:
            return self.value
        elif self.packet_type == 5:
            p1, p2 = (p.evaluate() for p in self.sub_packets)
            return 1 if p1 > p2 else 0
        elif self.packet_type == 6:
            p1, p2 = (p.evaluate() for p in self.sub_packets)
            return 1 if p1 < p2 else 0
        elif self.packet_type == 7:
            p1, p2 = (p.evaluate() for p in self.sub_packets)
            return 1 if p1 == p2 else 0

        # Should never get here
        raise ValueError("Invalid packet_type")

    def sum_version_numbers(self) -> int:
        return self.version + sum([p.sum_version_numbers() for p in self.sub_packets])


def decode_packet(remainder: str) -> Tuple[Packet, str]:
    version_bits, type_bits, remainder = remainder[:3], remainder[3:6], remainder[6:]
    packet_version = int(version_bits, 2)
    packet_type = int(type_bits, 2)

    if packet_type == 4:
        # literal value
        literal_bits = ""
        packet_length = 6  # version, type
        continue_bit = "1"
        while continue_bit == "1":
            continue_bit, bits, remainder = remainder[0], remainder[1:5], remainder[5:]
            literal_bits += bits
            packet_length += 5

        literal_value = int(literal_bits, 2)
        return Packet(packet_version, packet_type, literal_value), remainder
    else:
        # operator packet
        length_type_id = remainder[0]
        if length_type_id == "0":
            total_length_bits, remainder = remainder[1:16], remainder[16:]
            total_length = int(total_length_bits, 2)
            target_length = len(remainder) - total_length

            sub_packets = []
            while len(remainder) > target_length:
                sub_packet, remainder = decode_packet(remainder)
                sub_packets.append(sub_packet)

            return (
                Packet(packet_version, packet_type, sub_packets=sub_packets),
                remainder,
            )

        else:
            num_packet_bits, remainder = remainder[1:12], remainder[12:]
            num_packets = int(num_packet_bits, 2)

            sub_packets = []

            for x in range(num_packets):
                sub_packet, remainder = decode_packet(remainder)
                sub_packets.append(sub_packet)

            return (
                Packet(packet_version, packet_type, sub_packets=sub_packets),
                remainder,
            )


def main():
    hex_string = read_input()
    bit_string = hex_string_to_bits(hex_string)
    packet, _ = decode_packet(bit_string)

    part_1 = packet.sum_version_numbers()
    print(f"{part_1=}")

    part_2 = packet.evaluate()
    print(f"{part_2=}")


def read_input() -> str:
    with open("day16.txt") as f:
        return f.read().strip()


if __name__ == "__main__":
    main()
