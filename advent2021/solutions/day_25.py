Loc = tuple[int, int]
Cuces = tuple[Loc,...]

def _nxt_pos(
    pos:Loc,
    idx:int,
    rows:int,
    cols:int,
) -> Loc:
    new = list(pos)
    new[idx] += 1
    if new[0] >= rows or new[1] >= cols:
        new[idx] = 0
    return tuple(new)


def cycle(
    right:Cuces,
    down:Cuces,
    rows:int,
    cols:int,
) -> tuple[Cuces, Cuces]:
    rt = set()
    dn = set()
    for pos in right:
        p2 = _nxt_pos(pos, 1, rows, cols)
        if p2 in right or p2 in down:
            rt.add(pos)
        else:
            rt.add(p2)
    for pos in down:
        p2 = _nxt_pos(pos, 0, rows, cols)
        if p2 in rt or p2 in down:
            dn.add(pos)
        else:
            dn.add(p2)
    return rt, dn

def solve_day_25(input: str) -> tuple[int, str]:
    # build the board
    right = set()
    down = set()
    for i, row in enumerate(input.split("\n")):
        cols = len(row)
        for j, val in enumerate(row):
            if val == 'v':
                down.add((i,j))
            elif val == '>':
                right.add((i,j))
    rows, cols = i+1, j+1

    # run the cycles
    ct = 0
    while True:
        ct += 1
        rt, dn = cycle(right, down, rows, cols)
        if rt == right and dn == down:
            print("DONE")
            break
        right = rt
        down = dn
    ans_1 = ct
    ans_2 = "Freebie!"
    return ans_1, ans_2
