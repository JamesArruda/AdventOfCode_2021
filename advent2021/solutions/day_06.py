from typing import List
# Solve the Lantern fish scale (heh) problem by
# keeping track of only the group sizes of an age.

def _proc_input(input: str) -> List[int]:
    return list(map(int, input.split(",")))


def _solver(ages: List[int], n_days: int) -> int:
    days_left = [0]*9
    for a in ages:
        days_left[a] += 1

    for day in range(n_days):
        to_add = days_left[0]
        days_left = days_left[1:] + [to_add]
        days_left[6] += to_add
    return sum(days_left)


def solve_day_6(input: str) -> tuple[int, int]:
    ages = _proc_input(input)
    ans_1 = _solver(ages, 80)
    ans_2 = _solver(ages, 256)
    return ans_1, ans_2