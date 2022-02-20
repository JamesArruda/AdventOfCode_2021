from itertools import cycle, product
from collections import Counter
from functools import lru_cache


def pos(loc:int) -> int:
    return 10 if loc % 10 == 0 else loc % 10


def solve_part_1(player_1:int, player_2:int) -> int:
    # Simple to solve the short deterministic game
    # with brute force
    determin = cycle(range(1, 101))
    locs = [player_1, player_2]
    scores = [0, 0]

    idx = 0
    nr = 0
    while True:
        rolls = sum(next(determin) for _ in range(3))
        nr += 3
        loc = pos(locs[idx] + rolls)
        locs[idx] = loc
        scores[idx] += loc
        if scores[idx] >= 1000:
            break
        idx = not idx
    return nr * scores[not idx]


def solve_part_2(player_1:int, player_2:int) -> int:
    # dirac game means all orderings of 1,2,3, but independent of player!
    # Simplify down to the number of moves we can achieve each turn
    rolls = Counter(sum(p) for p in product([1,2,3], repeat=3))

    # Given the locations of both players, and their scores,
    # create possible futures.
    # Recurse on those futures, and when a score gets to 21
    # send it back up the line to sum up.
    @lru_cache(maxsize=None)
    def play(locs:tuple[int, int], score:tuple[int, int]):
        local_wins = {0:0, 1:0}
        for amt, n in rolls.items():
            new_loc = pos(locs[0] + amt)
            sc = score[0] + new_loc
            if sc >= 21:
                local_wins[0] += n
                continue
            for amt2, n2 in rolls.items():
                new_loc2 = pos(locs[1] + amt2)
                sc2 = score[1] + new_loc2
                if sc2 >= 21:
                    local_wins[1] += n*n2
                else:
                    res = play((new_loc, new_loc2), (sc, sc2))
                    local_wins[0] += n*n2*res[0]
                    local_wins[1] += n*n2*res[1]
        return local_wins

    locs = (player_1, player_2)
    ans = play(locs, (0, 0))
    return max(ans.values())
    

def solve_day_21(input: str) -> tuple[int, int]:
    one, two = input.split("\n")[:2]
    player_1 = int(one.split(" ")[-1])
    player_2 = int(two.split(" ")[-1])

    ans_1 = solve_part_1(player_1, player_2)
    ans_2 = solve_part_2(player_1, player_2)
    return ans_1, ans_2