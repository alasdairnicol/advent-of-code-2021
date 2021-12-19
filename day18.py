#!/usr/bin/env python
from ast import literal_eval
import copy
import math
from typing import Generator, Tuple
from functools import reduce
from itertools import permutations


class Node:
    def __init__(self, left=None, right=None, value=None):
        self.left = left
        self.right = right
        self.value = value

    def __str__(self) -> str:
        return (
            str(self.value)
            if self.value is not None
            else f"[{self.left}, {self.right}]"
        )

    def __deepcopy__(self, memo) -> "Node":
        return Node(
            left=copy.deepcopy(self.left),
            right=copy.deepcopy(self.right),
            value=self.value,
        )

    @staticmethod
    def from_list(l) -> "Node":
        if isinstance(l, int):
            return Node(value=l)
        else:
            return Node(left=Node.from_list(l[0]), right=Node.from_list(l[1]))


def create_tree(l: list) -> Node:
    if isinstance(l, int):
        return Node(value=l)
    else:
        return Node(left=create_tree(l[0]), right=create_tree(l[1]))


def add_nodes(node1: Node, node2: Node) -> Node:
    node = Node(left=copy.deepcopy(node1), right=copy.deepcopy(node2))
    reduce_node(node)
    return node


def parse_lines(lines) -> list[Node]:
    return [Node.from_list(literal_eval(l)) for l in lines]


def walk_tree(node: Node, depth: int = 0) -> Generator[Tuple[Node, int], None, None]:
    yield node, depth
    if node.left:
        for n, node_depth in walk_tree(node.left, depth + 1):
            yield n, node_depth
    if node.right:
        for n, node_depth in walk_tree(node.right, depth + 1):
            yield n, node_depth


def reduce_once(node: Node) -> bool:
    node_list = list(walk_tree(node))

    # Find previous and next values
    next_nodes_dict: dict = {}
    previous_nodes_dict: dict = {}
    previous_node = None
    previous_i = None
    for i, (x, node_depth) in enumerate(node_list):
        if x.value is not None:
            if previous_node is not None:
                next_nodes_dict[previous_i] = x
                previous_nodes_dict[i] = previous_node
            previous_node = x
            previous_i = i

    for i, (x, node_depth) in enumerate(node_list):
        if node_depth == 4 and x.left:
            if i + 1 in previous_nodes_dict:
                previous_nodes_dict[i + 1].value += x.left.value
            if i + 2 in next_nodes_dict:
                next_nodes_dict[i + 2].value += x.right.value

            x.value = 0
            x.left = x.right = None
            return True

    for i, (x, node_depth) in enumerate(node_list):
        # Split?
        if x.value and x.value >= 10:
            x.left = Node(value=math.floor(x.value / 2))
            x.right = Node(value=math.ceil(x.value / 2))
            x.value = None
            return True

    return False


def reduce_node(node: Node) -> None:
    while reduce_once(node):
        pass


def calc_magnitude(node: Node) -> int:
    if node.value is not None:
        return node.value
    else:
        return 3 * calc_magnitude(node.left) + 2 * calc_magnitude(node.right)


def do_part_1(nodes: list[Node]) -> int:
    node = reduce(add_nodes, nodes)
    return calc_magnitude(node)


def do_part_2(nodes: list[Node]) -> int:
    return max(calc_magnitude(add_nodes(x, y)) for x, y in permutations(nodes, 2))


def main():
    lines = read_input()

    nodes = parse_lines(lines)
    part_1 = do_part_1(nodes)
    print(f"{part_1=}")

    part_2 = do_part_2(nodes)
    print(f"{part_2=}")


def read_input() -> list[str]:
    with open("day18.txt") as f:
        return f.readlines()


if __name__ == "__main__":
    main()
