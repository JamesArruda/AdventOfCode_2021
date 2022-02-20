import re
from typing import List
Vector = tuple[int, int]


def targ_area(inputs: str) -> tuple[Vector, Vector]:
    res = re.findall(r"(x|y)=([-\d]+)..([-\d]+)", inputs)
    xs = [(int(a), int(b)) for v, a, b in res if v == 'x'][0]
    ys = [(int(a), int(b)) for v, a, b in res if v == 'y'][0]
    return xs, ys


def can_hit(vel: Vector, xt: Vector, yt:Vector) -> bool:
    x, y, t = 0, 0, 0
    xv, yv = vel
    while x <= xt[1] and y >= yt[0]:
        x = x + xv
        y = y + yv
        if (xt[0] <= x <= xt[1] and yt[0] <= y <= yt[1]):
            return True
        yv -= 1
        xv = max(0, xv - 1)
    return False


def solve_day_17(input: str) -> tuple[int, int]:
    xt, yt = targ_area(input)
    # After y_vel * 2 + 1 time steps, the shot is back at the 
    # zero line, with velocity = -(y_vel + 1)
    # Fastest y_vel = max height (t = y_vel)
    # Fastest y_vel is the one that touches the bottom of the zone
    # first after hitting 0. 
    y_vel = abs(yt[0]) - 1
    # Remember: sum 1 to n = n * (n+1) / 2
    # Sum of distance lost due to accel = -1
    # And decrease the velocity lost time step by 1 since it
    # ticks at the end.. algebra:
    t_height = y_vel
    height_lost = (t_height - 1) * (t_height - 1 + 1) / 2
    ans_1 = int(y_vel * t_height - height_lost)

    ct = 0
    mny, mxy = yt[0], abs(yt[0]) - 1
    for x_vel in range(0, xt[1]+1):
        for y_vel in range(mny, mxy+1):
            ct += can_hit((x_vel, y_vel), xt, yt)
    ans_2 = ct
    return ans_1, ans_2