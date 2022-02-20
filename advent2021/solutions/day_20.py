from itertools import product
from typing import Dict, Tuple, Set
Loc = Tuple[int, int]
Grid = Dict[Loc, str]
"""The repeating `infinite_on` was because the infinite 
grid would be all off or all on, and inspection of the code
showed that in those conditions the full 0 or 8 neighbors
off/on just flipped the middle.
"""

def neighbor_num(
    grid:Grid,
    loc:Loc,
    infinite_on:bool=False,
) -> Tuple[int, Set[Loc]]:
    v = ''
    alts = set()
    # This order matters to get the 'top left to bottom right'
    # for making the binary number
    for drow, dcol in product([-1, 0, 1], repeat=2):
        new = (loc[0] + drow, loc[1] + dcol)
        if new not in grid:
            alts.add(new)
        inf = '#' if infinite_on else '.'
        v += '1' if grid.get(new, inf) == '#' else '0'
    return int(v,2), alts


def run_update(
    grid:Grid,
    code:str,
    infinite_on:bool,
):
    new_grid = {}
    new_add = set()
    for loc in grid:
        v, alts = neighbor_num(grid, loc, infinite_on)
        new_add.update(alts)
        new_v = code[v]
        new_grid[loc] = new_v
    # everything new is part of the 'infinite'
    # which currently has the value of `infinite_on`
    for a in new_add:
        grid[a] = '#' if infinite_on else '.'
        v, alts = neighbor_num(grid, a, infinite_on)
        new_v = code[v]
        new_grid[a] = new_v
    return new_grid



def solve_day_20(input: str) -> tuple[int, int]:
    # (0, 0) is 'up' for the purposes of this
    code, blank, *lines = input.split("\n")

    grid = {}
    for i, row in enumerate(lines):
        for j, v in enumerate(row):
            grid[i,j] = v

    infinite_on = False
    for i in range(50):
        grid = run_update(grid, code, infinite_on)
        infinite_on = not infinite_on
        if i == 1:
            ans_1 = sum(1 for v in grid.values() if v=="#")
    ans_2 = sum(1 for v in grid.values() if v=="#")
    return ans_1, ans_2