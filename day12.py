#!/usr/bin/env python
from collections import defaultdict
from typing import Mapping

GraphType = Mapping[str, set[str]]
Route = list[str]


def main():
    lines = read_input()
    graph = make_graph(lines)

    part_a = do_part_a(graph)
    print(f"{part_a=}")

    part_b = do_part_b(graph)
    print(f"{part_b=}")


def make_graph(lines: list[str]) -> GraphType:
    graph = defaultdict(set)
    for line in lines:
        v1, v2 = line.strip().split("-")
        graph[v1].add(v2)
        graph[v2].add(v1)
    return graph


def can_visit(visited: Route, next_node: str, can_revisit_one_minor_node=False):
    if next_node == "start":
        return False

    if next_node.islower() and next_node in visited:
        if not can_revisit_one_minor_node:
            return False

    return True


def calc_routes(
    graph: GraphType, visited: Route, can_revisit_one_minor_node=False
) -> list[Route]:
    routes = []
    current = visited[-1]

    if current == "end":
        return [visited]

    if can_revisit_one_minor_node and current.islower() and visited.count(current) == 2:
        can_revisit_one_minor_node = False

    for next_node in graph[current]:
        if can_visit(visited, next_node, can_revisit_one_minor_node):
            routes.extend(
                calc_routes(graph, visited + [next_node], can_revisit_one_minor_node)
            )

    return routes


def do_part_a(graph: GraphType) -> int:
    routes = calc_routes(graph, visited=["start"])
    return len(routes)


def do_part_b(graph: GraphType) -> int:
    routes = calc_routes(graph, visited=["start"], can_revisit_one_minor_node=True)
    return len(routes)


def read_input() -> list[str]:
    with open("day12.txt") as f:
        return f.readlines()


if __name__ == "__main__":
    main()
