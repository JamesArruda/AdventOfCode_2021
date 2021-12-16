from advent2021.helpers.grids import (
    grid_from_list, cross_neighbors, Grid,
    Pos, shortest_path_length
)


def _graph_neighbors(grid: Grid, pos: Pos):
    for loc in cross_neighbors(grid, pos):
        yield loc, grid[loc]


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
    ans_1 = shortest_path_length(
        grid,
        min(grid),
        max(grid),
        _graph_neighbors,
    )
    grid = _enlarge_grid(grid, 5, 5)
    ans_2 = shortest_path_length(
        grid,
        min(grid),
        max(grid),
        _graph_neighbors,
    )
    return ans_1, ans_2

