import re
from itertools import combinations


def tokenize(num):
    tokens = re.findall(r"(\[|\]|\d+)", num)
    return [x if not x.isdigit() else int(x) for x in tokens]


def find_explode(num):
    # Exploding pairs will always consist of two regular numbers.
    level = 0
    cap, start, val = False, None, []
    for i, v in enumerate(num):
        if v == '[':
            level -= 1
            if level == -5 and not cap:
                cap = True
                start = i
        elif v == ']':
            if cap:
                assert len(val) == 2, val
                return start, start+len(val) + 2, val
            level += 1
        elif cap:
            val.append(v)
    return None, None, None


def increment_first(nums, by):
    # increments first, reverse the list to get what you want
    new = list(nums)
    for i, v in enumerate(new):
        if isinstance(v, int):
            new[i] = v + by
            break
    return new


def increment_last(nums, by):
    return increment_first(nums[::-1], by)[::-1]


def explode(num):
    a, b, v = find_explode(num)
    if a is None:
        return None
    left = num[:a]
    right = num[b:]
    left_new = increment_last(left, v[0])
    right_new = increment_first(right, v[1])
    return left_new + [0] + right_new


def _split(number):
    l = number // 2
    r = l if l+l == number else l + 1
    return [l, r]


def split(num):
    for i, n in enumerate(num):
        if isinstance(n, int) and n >= 10:
            add_in = ['[',] + _split(n) + [']']
            return num[:i] + add_in + num[i+1:]
    return None


def run_num(num):
    while True:
        res = explode(num)
        if res is not None:
            num = res
            continue
        res = split(num)
        if res is None:
            return num
        num = res


def magnitude(num):
    use = list(num)
    ct = 0
    while True:
        for i in range(len(use) - 1):
            a, b = use[i:i+2]
            if all(isinstance(x, int) for x in [a,b]):
                use = use[:i-1] + [3*a + 2 * b] + use[i+3:]
                break
        if len(use) == 1:
            return use[0]


def solve_day_18(input: str) -> tuple[int, int]:
    nums = [tokenize(num) for num in input.split("\n")]
    use_nums = [list(n) for n in nums]
    while len(use_nums) > 1:
        new = ["["] + use_nums[0] + use_nums[1] + ["]"]
        ans = run_num(new)
        use_nums = [ans] + use_nums[2:]
    ans = use_nums[0]
    ans_1 = magnitude(ans)
    best = 0
    for a, b in combinations(nums, 2):
        for u, v in [[a,b], [b,a]]:
            new = ["["] + u + v + ["]"]
            ans = run_num(new)
            mag = magnitude(ans)
            best = max(mag, best)
    ans_2 = best
    return ans_1, ans_2