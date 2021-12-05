from typing import List
from collections import Counter
import numpy as np


def _proc_line(line: str) -> tuple[np.ndarray, np.ndarray]:
    st, en = line.split(" -> ")
    st = list(map(int, st.split(",")))
    en = list(map(int, en.split(",")))
    return np.array(st), np.array(en)


def _along_line(st, en):
    """Generate integer point along the line from start to end.
    Assumes angle of line is 0, 45, or 90 degrees.
    """
    d = en - st
    v = np.sign(d)
    n_pts = np.abs(d[d!=0][0])
    for i in range(n_pts + 1):
        yield st + v * i


def solve_day_5(input: str) -> tuple[int, int]:
    data = [_proc_line(l) for l in input.split("\n")]
    pts_1, pts_2 = Counter(), Counter()
    for st, en in data:
        is_straight = (st == en).any()
        for pt in _along_line(st, en):
            pts_2[tuple(pt)] += 1
            if is_straight:
                pts_1[tuple(pt)] += 1
    ans_1 = sum(1 for v in pts_1.values() if v > 1)
    ans_2 = sum(1 for v in pts_2.values() if v > 1)
    return ans_1, ans_2