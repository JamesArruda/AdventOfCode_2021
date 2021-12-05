from typing import List
import numpy as np
import re


def _proc_input(input: str) -> tuple[List[int], List[np.ndarray]]:
    nums, _, *boards = input.split("\n")
    nums = list(map(int, nums.split(",")))
    the_boards = [[]]
    for l in boards:
        if not l:
            the_boards.append([])
            continue
        the_boards[-1].append(list(map(int, re.split(r"\s+", l.strip()))))
    the_boards = [np.array(x) for x in the_boards]
    return nums, the_boards


def _solver(nums: List[int], the_boards: List[np.ndarray], quit: bool) -> int:
    last = None
    winners = set()
    for n in nums:
        for i, b in enumerate(the_boards):
            if i in winners:
                continue
            b[b==n] = -1
            if -5 in b.sum(0) or -5 in b.sum(1):
                winners.add(i)
                last = b[b>=0].sum()*n
                if quit:
                    return last
    return last


def solve_day_4(input: str) -> tuple[int, int]:
    nums, the_boards = _proc_input(input)
    ans_1 = _solver(nums, [x.copy() for x in the_boards], True)
    ans_2 = _solver(nums, the_boards, False)
    return ans_1, ans_2