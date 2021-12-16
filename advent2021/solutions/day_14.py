from typing import List, Dict, Counter as Ctr
from collections import Counter
Pairs = Ctr[str]
Rules = Dict[str, str]


def _run(pairs: Pairs, rules: Rules) -> Pairs:
    c = Counter()
    for p, n in pairs.items():
        insert = rules[p]
        p1 = p[0] + insert
        p2 = insert + p[1]
        c[p1] += n
        c[p2] += n
    return c


def _proc_results(pairs: Pairs) -> int:
    res = Counter()
    for (a,b), n in pairs.items():
        res[a] += n
        res[b] += n
    mc = res.most_common()
    return (mc[0][1] - mc[-1][1]) // 2


def solve_day_14(input: str) -> tuple[int, int]:
    template, _, *rule_strs = input.split("\n")
    rules = {
        x.split(" -> ")[0]: x.split(" -> ")[1]
        for x in rule_strs
    }
    use = Counter(
        template[i:i+2]
        for i in range(len(template)-1)
    )
    for i in range(40):
        use = _run(use, rules)
        if i == 9:
            ans_1 = _proc_results(use)
    ans_2 = _proc_results(use)
    return ans_1, ans_2