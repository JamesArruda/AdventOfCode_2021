from typing import Dict, List, Generator
import numpy as np
from scipy.ndimage import label, find_objects


def _get_neighbors(
    d: Dict[tuple[int, int], int],
    pos: tuple[int, int],
) -> Generator[tuple[int, int], None, None]:
    for di, dj in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
        new = (pos[0]+di, pos[1]+dj)
        if new in d:
            yield new


def _is_lowest(
    d: Dict[tuple[int, int], int],
    pos: tuple[int, int],
) -> bool:
    v = min([d[loc] for loc in _get_neighbors(d, pos)])
    return v > d[pos]


def solve_day_9(input: str) -> tuple[int, int]:
    inp = [[int(x) for x in y] for y in input.split("\n")]
    X = np.array(inp)
    d = {(i,j): v for (i,j), v in np.ndenumerate(X)}
    mins = {pos: val for pos, val in d.items() if _is_lowest(d, pos)}
    ans_1 = sum(mins.values()) + len(mins)

    Y = X.copy()
    Y[Y == 9] = -1
    Y = Y + 1
    Z, n = label(Y)
    cts = [(Z==i).sum() for i in range(1, n+1)]
    cts = sorted(cts)
    ans_2 = cts[-1] * cts[-2] * cts[-3]
    
    return ans_1, ans_2
