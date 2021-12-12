#!/usr/bin/env python
from collections import defaultdict
from typing import Mapping, Tuple

GraphType = Mapping[str, set[str]]
Route = list[str]


def main():
    lines = read_input()
    graph = make_graph(lines)

    part_a = do_part_a(graph)
    print(f"{part_a=}")

    # part_b = do_part_b(grid)
    # print(f"{part_b=}")


def make_graph(lines: list[str]) -> GraphType:
    graph = defaultdict(set)
    for line in lines:
        v1, v2 = line.strip().split("-")
        graph[v1].add(v2)
        graph[v2].add(v1)
    return graph


def calc_routes(graph: GraphType, visited: Route) -> list[Route]:
    routes = []
    current = visited[-1]

    if current == "end":
        return [visited]

    for next_node in graph[current]:
        if next_node.islower() and next_node in visited:
            # Can't revisit a lower case node
            pass
        else:
            routes.extend(calc_routes(graph, visited + [next_node]))

    return routes


def do_part_a(graph: GraphType) -> int:
    routes = calc_routes(graph, visited=["start"])
    return len(routes)


def read_input() -> list[str]:
    with open("day12.txt") as f:
        return f.readlines()


if __name__ == "__main__":
    main()
