from collections import Counter
from typing import Union, List
Span = tuple[int, int]
Cube = tuple[Span, Span, Span]
Command = tuple[Cube, str]
"""
Solution process is to find cubes that overlap, and record
their overlapping sections as new off/on commands.
If an 'off' command overlaps with existing cubes, then we
create an 'off' command just for the existing cubes that 
are already on. Turning off an off is ignored.
"""

def proc_line(line:str) -> tuple[str, Cube]:
    comm, rest = line.split(" ")
    cube = [x[2:] for x in rest.split(",")]
    cube = [tuple([int(x) for x in y.split("..")]) for y in cube]
    return comm, tuple(cube)


def intersection(
    a_cube:Cube,
    b_cube:Cube,
) -> Union[None, Cube]:
    # Find the intersecting sub-cube, if it exists
    ax, ay, az = a_cube
    bx, by, bz = b_cube
    # lower left of intersection is 
    # the most lower left of both
    x0 = max(ax[0], bx[0])
    y0 = max(ay[0], by[0])
    z0 = max(az[0], bz[0])
    # upper right is least upper right
    x1 = min(ax[1], bx[1])
    y1 = min(ay[1], by[1])
    z1 = min(az[1], bz[1])
    # lower left needs to be lower and lefter-er
    if x0 <= x1 and y0 <= y1 and z0 <= z1:
        return (x0, x1), (y0, y1), (z0, z1)
    return None


def volume(a_cube:Cube) -> int:
    spans = [a[1] - a[0] + 1 for a in a_cube]
    return spans[0] * spans[1] * spans[2]


def solve_overlap(
    commands:List[Command],
) -> int:
    cube_value_ct = Counter()
    for i, (cube, command) in enumerate(commands):
        cube_value = 1 if command == 'on' else -1
        # Find all intersections with existing cubes, and 
        # create a negating cube
        intersecting = Counter()
        for b_cube, b_value in cube_value_ct.items():
            inter = intersection(cube, b_cube)
            if inter is None:
                continue
            intersecting[inter] -= b_value
        # only add on cuboid to the new. Off only affects past cubes
        if cube_value == 1:
            cube_value_ct[cube] += cube_value
        cube_value_ct.update(intersecting)
    answer = sum(volume(cube) * value for cube, value in cube_value_ct.items())
    return answer


def filter(cube:Cube, limit:int=50) -> bool:
    for part in cube:
        if any(abs(x) > limit for x in part):
            return False
    return True


def solve_day_22(input: str) -> tuple[int, int]:
    all_cubes = []
    for l in input.split("\n"):
        comm, cube = proc_line(l)
        all_cubes.append((cube, comm))
    part_1_commands = [x for x in all_cubes if filter(x[0])]
    ans_1 = solve_overlap(part_1_commands)
    ans_2 = solve_overlap(all_cubes)
    return ans_1, ans_2