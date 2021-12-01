import numpy as np
from typing import List, Tuple


def _proc_input(input: str):
    return list(map(int, input.split("\n")))


def solve_day_1(input: str) -> Tuple[int, int]:
    data = _proc_input(input)

    ans_1 = (np.diff(data) > 0).sum()
    window = np.convolve(
        data,
        np.ones(3),
        'valid',
    )
    ans_2 = (np.diff(window) > 0).sum()
    return ans_1, ans_2
