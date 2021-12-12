from typing import Generator, Any, Dict, List, Callable

Pos = tuple[int, int]
Grid = Dict[Pos, Any]
Neigh = List[tuple[int, int]]

DIAGS = [(1,1), (-1,1), (1,-1), (-1,-1)]
CROSS = [(1,0), (0,1), (-1,0), (0,-1)]


def grid_from_list(input: List[str], convert: Callable) -> Grid:
    grid = {}
    for row, cols in enumerate(input):
        for col, value in enumerate(cols):
            grid[(row, col)] = convert(value)
    return grid


def grid_to_list(grid: Grid) -> List[List[Any]]:
    output = []
    n_rows = max(k[0] for k in grid)
    n_cols = max(k[1] for k in grid)
    for r in range(n_rows):
        output.append([])
        for c in range(n_cols):
            v = grid[r, c]
            output[-1].append(v)
    return output


def _get_neighbors(
    grid: Grid,
    pos: Pos,
    neigh: Neigh,
) -> Generator[Pos, None, None]:
    for di, dj in neigh:
        new = (pos[0] + di, pos[1] + dj)
        if new in grid:
            yield new


def diag_neighbors(grid: Grid,
    pos: Pos,
) -> Generator[Pos, None, None]:
    yield from _get_neighbors(grid, pos, DIAGS)


def cross_neighbors(grid: Grid,
    pos: Pos,
) -> Generator[Pos, None, None]:
    yield from _get_neighbors(grid, pos, CROSS)


def all_neighbors(grid: Grid,
    pos: Pos,
) -> Generator[Pos, None, None]:
    yield from _get_neighbors(grid, pos, DIAGS)
    yield from _get_neighbors(grid, pos, CROSS)


