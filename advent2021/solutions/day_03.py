from typing import List
from collections import Counter

def _proc_input(input: str) -> List[tuple[str, int]]:
    return input.split("\n")


def solve_day_3(input: str) -> tuple[int, int]:
    data = _proc_input(input)
    cs = [Counter() for _ in data[0]]
    for line in data:
        for c, x in zip(cs, line):
            c[x] += 1
    gamma = int(''.join([c.most_common(1)[0][0] for c in cs]), base=2)
    epsilon = int(''.join([c.most_common(2)[-1][0] for c in cs]), base=2)
    ans_1 = gamma * epsilon

    conds = [
        lambda a, b: a >= b,
        lambda a, b: a < b,
    ]

    ans_2 = 1
    for cond in conds:
        use = list(data)
        for idx in range(len(use[0])):
            c = Counter([x[idx] for x in use])
            match = '1' if cond(c['1'], c['0']) else '0'
            use = [x for x in use if x[idx] == match]
            if len(use) == 1:
                break
        ans_2 *= int(use[0],base=2)
    return ans_1, ans_2