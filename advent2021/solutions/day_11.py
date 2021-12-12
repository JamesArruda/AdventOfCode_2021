from typing import List
from advent2021.helpers import grid_from_list, all_neighbors


def solve_day_11(input: str) -> tuple[int, int]:
    # steps:
    grid = grid_from_list(input.split("\n"), int)
    total_fired = 0
    grid_values = [grid.copy()]
    for i in range(1000):
        # 1: Add energy
        grid = {k: v + 1 for k, v in grid.items()}
        # 2: See who hit 10
        fired = set([k for k, v in grid.items() if v >= 10])
        new_fired = fired
        while new_fired:
            # 3: Update energy
            for pos in new_fired:
                for new in all_neighbors(grid, pos):
                    grid[new] += 1
            # 4: See who hit 10, but isn't in fired
            new_fired = set([k for k, v in grid.items() if v >= 10]) - fired
            fired.update(new_fired)
        if i < 100:
            total_fired += len(fired)
        # set the high ones to zero
        grid = {k: v if v <= 9 else 0 for k, v in grid.items()}
        grid_values.append(grid.copy())
        if all(v==0 for v in grid.values()):
            ans_2 = i + 1
            break
    return total_fired, ans_2