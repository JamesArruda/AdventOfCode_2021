import numpy as np
from scipy.spatial.transform import Rotation
from itertools import combinations
from collections import Counter
from typing import Dict, Generator, Tuple, Union
"""
I solved originally with brute force, but ended up changing to the concept
from the advent of code subreddit to do 'fingerprinting' on pairwise 
distances to direct the seach for possible overlaps.
The fingerprinting got lucky based on the problem set, so other algorithms
for matching are probably better in general.
"""

AlignData = Tuple[int, int, np.ndarray]
RotData = Tuple[str, int, int]


def proc_input(input: str) -> Dict[int, np.ndarray]:
    scanners = {}
    for l in input.split("\n"):
        if 'scanner' in l:
            n = int(l.split(" ")[2])
            scanners[n] = []
        elif l.strip():
            beacon = [int(x) for x in l.strip().split(",")]
            scanners[n].append(tuple(beacon))
    return {n: np.array(v) for n, v in scanners.items()}


def rotator(
    X:np.ndarray,
    dir:str,
    angle:int,
    x_angle:int,
) -> np.ndarray:
    r1 = Rotation.from_euler(dir, [angle], degrees=True)
    r2 = Rotation.from_euler('x', [x_angle], degrees=True)
    return Rotation.apply(r2 * r1, X).round().astype(int)


def all_rotations(
    X:np.ndarray,
) -> Generator[Tuple[np.ndarray, RotData], None, None]:
    opts = [("Y", [90, 270]), ("Z", [0, 90, 180, 270])]
    for dir, angles in opts:
        for angle in angles:
            for x_angle in [0, 90, 180, 270]:
                new = rotator(X, dir, angle, x_angle)
                yield new, (dir, angle, x_angle)

def test_align(
    A:np.ndarray,
    B:np.ndarray,
) -> Union[None, AlignData]:
    for idx in range(A.shape[0]):
        loc = A[idx, :]
        for idx2 in range(B.shape[0]):
            loc2 = B[idx2, :]
            delta = loc - loc2
            Bt = B + delta
            same = (Bt[:, None] == A).all(-1).any(-1)
            same = same.sum()
            if same >= 12:
                return idx, idx2, delta
    return None

def pair_test(
    At:np.ndarray,
    Bt:np.ndarray,
) -> Union[None, Tuple[AlignData, RotData]]:
    ans = None
    done = False
    rotB = None
    # for A, rotA in all_rotations(At):
    for B, rotB in all_rotations(Bt):
        ans = test_align(At, B)
        if ans is not None:
            done = True
            break
    if not done:
        return None
    return ans, rotB


def solve_day_19(input: str) -> tuple[int, int]:
    scanners = proc_input(input)
    # scanners = {k:set([tuple(x) for x in X]) for k,X in scanners.items()}

    # This is the fingerprinting
    coun = {}
    for n, sc in scanners.items():
        z = Counter()
        for a, b in combinations(sc, 2):
            z[np.abs(a-b).sum()] += 1
        coun[n] = z

    in_base = [0,]
    deltas = []

    idx = 0
    while len(in_base) < len(scanners):
        u = in_base[idx]
        while len(in_base) < len(scanners): # while True, but catches the end
            not_in_base = [i for i in range(len(scanners)) if i not in in_base]
            v = max(not_in_base, key=lambda x: len(coun[u] & coun[x]))
            # for 12 choose 2 distances to be the same, the overlap must be >= 66 
            if len(coun[u] & coun[v]) < 66:
                break
            res = pair_test(scanners[u], scanners[v])
            if res is None:
                break
            (idx_u, idx_v, delta), rotV = res
            deltas.append(delta)
            V = scanners[v]
            V = rotator(V, *rotV)
            scanners[v] = V + delta
            in_base.append(v)
        idx += 1
    z = np.vstack([v for v in scanners.values()])
    ans_1 = len(set([tuple(x) for x in z]))

    ans_2 = 0
    for a, b in combinations(deltas, r=2):
        d = sum(abs(x-y) for x,y in zip(a, b))
        ans_2 = max(ans_2, d)
    ans_2
    

    return ans_1, ans_2