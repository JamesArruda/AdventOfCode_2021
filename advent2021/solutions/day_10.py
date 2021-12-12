from typing import List
import bisect

PAIRS = {
    '(':')',
    '[':']',
    '{':'}',
    '<':'>',
}


def test_line(l: str) -> tuple[int, List[str]]:
    chunks = []
    for a in l:
        if a in PAIRS:
            chunks.append(a)
        else:
            if a != PAIRS[chunks[-1]]:
                return {')': 3, '}':1197, ']': 57, '>':25137}[a], []
            chunks.pop(-1)
    return 0, chunks


def score(chunks: List[str]) -> int:
    t = 0
    for c in chunks:
        t *= 5
        t += {'(': 1, '[': 2, '{':3, '<':4}[c]
    return t


def solve_day_10(input: str) -> tuple[int, int]:
    ans_1 = 0
    incom = []
    for l in input.split("\n"):
        n, chunks = test_line(l)
        if n != 0:
            ans_1 += n
        else:
            bisect.insort(
                incom,
                score(chunks[::-1]),
            )
    ans_2 = incom[len(incom) // 2]
    return ans_1, ans_2
