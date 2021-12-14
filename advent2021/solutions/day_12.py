from typing import Dict, Set, List, Callable
from collections import Counter, defaultdict
Path = List[str]
HashPath = tuple[str,...]
Graph = Dict[str, Set[str]]


def _proc_input(input: str) -> Graph:
    graph = defaultdict(set)
    for line in input.split("\n"):
        u, v = line.split("-")
        graph[u].add(v)
        graph[v].add(u)
    return graph


def is_small(x: str) -> bool:
    return x == x.lower()


def node_test_1(node: str, path: Path) -> bool:
    if is_small(node) and node in path:
        return False
    return True


def node_test_2(node: str, path: Path) -> bool:
    if node == 'start':
        return False
    if not is_small(node):
        return True
    amt = path.count(node)
    if amt == 0:
        return True
    smalls = Counter([p for p in path if is_small(p)])
    if 2 not in smalls.values():
        return True
    return False
    

def find_path(
    G: Graph,
    path: Path,
    results: Set[HashPath],
    test: Callable[[str, Path], bool],
) -> None:
    curr = path[-1]
    if curr == 'end':
        results.add(tuple(path))
        return
    for node in G[curr]:
        if test(node, path):
            find_path(G, list(path) + [node], results, test)


def solve_day_12(input: str) -> tuple[int, int]:
    graph = _proc_input(input)
    results = set()
    find_path(graph, ['start'], results, node_test_1)
    ans_1 = len(results)
    results = set()
    find_path(graph, ['start'], results, node_test_2)
    ans_2 = len(results)
    return ans_1, ans_2