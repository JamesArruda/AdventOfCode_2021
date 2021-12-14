from itertools import takewhile
from typing import List
Point = tuple[int, int]
Dots = List[Point]
Instr = tuple[str, int]


def x_fold(dots: Dots, x_loc: int) -> Dots:
    # Note: A fold at 5 with a dot at (5, y)
    # means dot becomes (4, y)
    new_dots = []
    for x, y in dots:
        new_x = x if x < x_loc else 2 * x_loc - x
        if (new_x,y) not in new_dots:
            new_dots.append((new_x,y))
    return new_dots


def y_fold(dots: Dots, y_loc: int) -> Dots:
    dots = [(y,x) for x,y in dots]
    new = x_fold(dots, y_loc)
    return [(y,x) for x,y in new]


folder = {'x': x_fold, 'y': y_fold}


def _proc_input(input: str) -> tuple[Dots, List[Instr]]:
    data_sp = input.split("\n")
    dots = [tuple(map(int, x.split(","))) for x in takewhile(lambda x: x, data_sp)]
    folds = [d for d in takewhile(lambda x: x, data_sp[::-1])][::-1]
    folds = [f.split("=") for f in folds]
    folds = [(f[0].split(" ")[-1], int(f[1])) for f in folds]
    return dots, folds


def solve_day_13(input: str) -> tuple[int, str]:
    dots, folds = _proc_input(input)
    kind, amt = folds[0]
    dots2 = folder[kind](dots, amt)
    ans_1 = len(dots2)

    for kind, loc in folds:
        dots = folder[kind](dots, loc)
    ans_2 = ""
    for y in range(6):
        for x in range(40):
            ans_2 += "#" if (x,y) in dots else " "
        ans_2 += "\n"
    return ans_1, ans_2[:-1]