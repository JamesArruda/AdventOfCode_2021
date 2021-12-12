# procedure: find the '1', then '7', that tells us the top segment
def proc_line(line: str) -> int:
    unique_n = [6, 2, 5, 4, 3, 7]
    tests = line.split("|")[0].strip().split(" ")
    final = line.split("|")[1].strip().split(" ")
    tests = {n: [x for x in tests if len(x) == n] for n in unique_n}
    res = {
        1: tests[2][0],
        7: tests[3][0],
        8: tests[7][0],
        4: tests[4][0],
    }
    res[3] = [x for x in tests[5] if set(res[1]) < set(x)][0]
    tests[5].remove(res[3])
    res[6] = [x for x in tests[6] if not set(res[1]) < set(x)][0]
    res[9] = [x for x in tests[6] if set(res[3]) < set(x)][0]
    res[0] = [x for x in tests[6] if x not in [res[6], res[9]]][0]
    res[5] = [x for x in tests[5] if set(x) < set(res[6])][0]
    tests[5].remove(res[5])
    res[2] = tests[5][0]
    rev = {frozenset(v):k for k,v in res.items()}
    return int(''.join([str(rev[frozenset(k)]) for k in final]))


def solve_day_8(input: str) -> tuple[int, int]:
    n_used = [6, 2, 5, 5, 4, 5, 6, 3, 7, 6]
    all_cts = 0
    find = [1, 4, 7, 8]
    find = [n_used[f] for f in find]
    for line in input.split("\n"):
        after = line.split("|")[-1].strip().split(" ")
        all_cts += sum(1 for x in after if len(x) in find)
    ans_1 = all_cts
    ans_2 = sum(proc_line(line) for line in input.split("\n"))
    return ans_1, ans_2
