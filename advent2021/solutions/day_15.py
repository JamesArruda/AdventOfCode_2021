from typing import List, Dict
from advent2021.helpers.grids import (
    grid_from_list, cross_neighbors, Grid
)
import networkx as nx


def _make_graph(grid: Grid) -> nx.DiGraph:
    G = nx.DiGraph()
    for loc, val in grid.items():
        for neigh in cross_neighbors(grid, loc):
            val2 = grid[neigh]
            G.add_edge(loc, neigh, weight=val2)
    return G


def _enlarge_grid(grid: Grid, rows: int, cols:int) -> Grid:
    row_span = max(grid)[0] + 1
    col_span = max(grid)[1] + 1
    new_grid = {}
    for row in range(row_span * rows):
        for col in range(col_span * cols):
            increase = row // row_span + col // col_span
            base_row, base_col = row % row_span, col % col_span
            v = grid[base_row, base_col] + increase
            new_grid[row, col] = v if v <= 9 else v % 9
    return new_grid


def solve_day_15(input: str) -> tuple[int, int]:
    grid = grid_from_list(input.split("\n"), int)
    G = _make_graph(grid)
    ans_1 = nx.shortest_path_length(
        G,
        source=min(grid),
        target=max(grid),
        weight='weight',
    )
    grid = _enlarge_grid(grid, 5, 5)
    G = _make_graph(grid)
    ans_2 = nx.shortest_path_length(
        G,
        source=min(grid),
        target=max(grid),
        weight='weight',
    )
    return ans_1, ans_2

