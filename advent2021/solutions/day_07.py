from typing import List, Callable
from collections import Counter
# This problem asks for the median and mean
# x-locations of the data, but since it wants
# the custom cost value, we can't get away
# that easy.

def _proc_input(input: str) -> List[int]:
    return list(map(int, input.split(",")))


def _first_cost(pt:int, n:int) -> int:
    return abs(pt - n)


def _second_cost(pt:int, n:int) -> int:
    d = abs(pt - n)
    return d * (d+1) // 2


def _compare(
    point_counts: Counter,
    center: int,
    cost: Callable[[int, int], int],
) -> int:
    s = 0
    for pt, num in point_counts.items():
        s += num * cost(pt, center)
    return s


def solve_day_7(input: str) -> tuple[int, int]:
    pos = Counter(_proc_input(input))
    st, en = min(pos), max(pos)
    center_1 = min(
        range(st, en+1),
        key=lambda x: _compare(pos, x, _first_cost)
    )
    center_2 = min(
        range(st, en+1),
        key=lambda x: _compare(pos, x, _second_cost)
    )
    ans_1 = _compare(pos, center_1, _first_cost)
    ans_2 = _compare(pos, center_2, _second_cost)
    return ans_1, ans_2