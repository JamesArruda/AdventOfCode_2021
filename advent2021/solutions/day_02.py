from typing import List
from functools import reduce


def _proc_input(input: str) -> List[tuple[str, int]]:
    data = []
    for line in input.split("\n"):
        command, n = line.split(" ")
        data.append((command, int(n)))
    return data


func_map = {
    'forward': lambda a, x: [a[0]+x, a[1]],
    'down': lambda a, x: [a[0], a[1]+x],
    'up': lambda a, x: [a[0], a[1]-x],
}

func_map_2 = {
    'forward': lambda pos, aim, x: ([pos[0]+x,pos[1]+x*aim], aim),
    'down': lambda pos, aim, x: (pos, aim+x),
    'up': lambda pos, aim, x: (pos, aim-x),
}


def solve_day_2(input: str) -> tuple[int, int]:
    data = _proc_input(input)
    pos = [0, 0]
    for command, n in data:
        pos = func_map[command](pos, n)
    ans_1 = pos[0] * pos[1]

    aim, pos = 0, [0, 0]
    for command, n in data:
        pos, aim = func_map_2[command](pos, aim, n)
    ans_2 = pos[0] * pos[1]
    return ans_1, ans_2