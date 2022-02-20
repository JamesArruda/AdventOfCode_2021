from copy import deepcopy
from itertools import product
from heapq import heappop, heappush
from typing import Union, Dict, Generator
"""
Amphipod game!
This one is a beast, in terms of lines of code.
It's solvable by hand, maybe even faster than coding it...
Also, the locations go (column, row) when you look at the input.
Starting from the top left first feasible spot as (0,0).
"""
# Types!
Loc = tuple[int, int]
Direct = tuple[int, int]
DBoard = Dict[Loc, str]
TBoard = tuple[tuple[Loc,str],...]

# Game data!
ENERGY = {'A':1, 'B':10, 'C':100, 'D':1000}
COL_RULES = {'A':2, 'B':4, 'C':6, 'D':8}
BLANK_FIRST_GAME = {
    (0, 0):'',  (1, 0):'', (2, 0):'X', (3, 0):'',
    (4, 0):'X', (5, 0):'', (6, 0):'X', (7, 0):'',
    (8, 0):'X', (9, 0):'', (10,0):'',  (2, 1):'',
    (2, 2):'',  (4, 1):'', (4, 2):'',  (6, 1):'',
    (6, 2):'',  (8, 1):'', (8, 2):'',
}
BLANK_SECOND_GAME = BLANK_FIRST_GAME.copy()
BLANK_SECOND_GAME[2,2] = 'D'
BLANK_SECOND_GAME[2,3] = 'D'
BLANK_SECOND_GAME[4,2] = 'C'
BLANK_SECOND_GAME[4,3] = 'B'
BLANK_SECOND_GAME[6,2] = 'B'
BLANK_SECOND_GAME[6,3] = 'A'
BLANK_SECOND_GAME[8,2] = 'A'
BLANK_SECOND_GAME[8,3] = 'C'


def _is_open(
    board:DBoard,
    loc:Loc,
) -> bool:
    """Can a mover go to this space?
    Doesn't check for stopping, just moving.
    """
    val = board[loc]
    return not val or val == 'X'


def move_up(
    board:DBoard,
    pos:Loc,
) -> Union[None, Loc]:
    """Return the position that a mover
    can move up to, if one exists.
    None otherwise.
    """
    while pos[1] != 0:
        pos = (pos[0], pos[1]-1)
        if not _is_open(board, pos):
            return None
    return pos


def move_down(
    board:DBoard,
    pos:Loc,
) -> Loc:
    """Return the result of moving down"""
    last = pos
    while True:
        pos = (pos[0], pos[1] + 1)
        if pos not in board:
            return last
        if not _is_open(board, pos):
            return last
        last = pos

def move_side(
    board:DBoard,
    pos:Loc,
    direc:Direct,
    filt:bool=True,
) -> Generator[Loc, None, None]:
    """Yield the spot a piece can move to
    going left or right. Finishes when
    no more motion is possible.
    The `filt` kwarg decides if we want to
    return positions that can't be stopped at.
    If false, it lets us return positions over
    the drops and then move down.
    """
    pos = (pos[0]+direc, pos[1])
    while pos in board:
        if not _is_open(board, pos):
            return None
        if not filt or board[pos] != 'X':
            yield pos
        pos = (pos[0]+direc, pos[1])

    
def move_up_direc(
    board:DBoard,
    pos:Loc,
    direc:Direct,
) -> Generator[Loc, None, None]:
    """Generate points from moving up from
    a column to the left or right - defined 
    with `direc`. Stops yielding when no 
    motion is possible.
    """
    pos = move_up(board, pos)
    if pos is None:
        return None
    yield from move_side(board, pos, direc, filt=True)


def _ready_col(
    board:DBoard,
    col:int,
    piece:str,
) -> bool:
    """Return whether or not a column is able to receive
    a mover of a particular letter.
    Tests for empty or only other of the same letter.
    Assumes the col/letter matchup is correct. (COL_RULES)
    """
    p = (col, 1)
    while p in board:
        if board[p] not in ['', piece]:
            return False
        p = (col, p[1] + 1)
    return True
        
    
def move_side_down(
    board:DBoard,
    pos:Loc,
    direc:Direct,
) -> Generator[Loc, None, None]:
    """Generate points a piece can stop at
    by going left/right, then down.
    NOTE: Probably doesn't need to be a generator."""
    piece = board[pos]
    allowed = COL_RULES[piece]
    if not _ready_col(board, allowed, piece):
        return
    for new in move_side(board, pos, direc, filt=False):
        if board[new] == 'X' and new[0] == allowed:
            final = move_down(board, new)
            if final != new:
                yield final


def move_up_down(
    board:DBoard,
    pos:Loc,
    direc:Direct,
) -> Generator[Loc, None, None]:
    """Yields values where a piece can go up, over, then
    down into a usable column."""
    piece = board[pos]
    allowed = COL_RULES[piece]
    if not _ready_col(board, allowed, piece):
        return
    pos = move_up(board, pos)
    if pos is None:
        return None
    yield from move_side_down(board, pos, direc)


def all_moves(
    board:DBoard,
) -> Generator[tuple[Loc, Loc], None, None]:
    """Yield all moves available to the board.
    Moves are yielded as (start point, end point)."""
    for pos, val in board.items():
        if not val or val == 'X':
            continue
        if pos[1] != 0:
            movers = [move_up_direc]#, move_up_down]
            for func, direc in product(movers, [1, -1]):
                for m in func(board, pos, direc):
                    yield pos, m
        else:
            movers = [move_side, move_side_down]
            for func, direc in product(movers, [-1, 1]):
                for m in func(board, pos, direc):
                    yield pos, m


def board_move(
    board:DBoard,
    curr:Loc,
    to:Loc,
) -> tuple[TBoard, int]:
    """Move a piece and calculate the energy of the move."""
    board = board.copy()
    piece = board[curr]
    board[curr] = ''
    board[to] = piece
    d = abs(curr[0]-to[0]) + abs(curr[1] - to[1])
    return tuple_board(board), ENERGY[piece] * d


def neighbors(
    board: DBoard,
) -> Generator[tuple[TBoard, int], None, None]:
    """Yield all possible moves on the current board."""
    for curr, to in all_moves(board):
        board2, cost = board_move(board, curr, to)
        yield board2, cost


def complete_check(
    board: DBoard,
) -> bool:
    """Returns whether or not the game is done."""
    for piece, col in COL_RULES.items():
        check = _ready_col(board, col, piece)
        if not check:
            return False
    for i in [0,1,3,5,7,9,10]:
        if board[(i, 0)] != '':
            return False
    return True


def tuple_board(board: DBoard) -> TBoard:
    return tuple([(k,v) for k,v in board.items()])


def dict_board(board: TBoard) -> DBoard:
    return {k:v for k,v in board}


def shortest_path_length(
    start: TBoard,
) -> Union[None, tuple[int, Dict[TBoard, TBoard], TBoard]]:
    """Standard Dijkstra for the board."""
    dist = {start: 0}
    preds = {start: None}
    Q = [(0, start)]
    while Q:
        d, u = heappop(Q)
        u_dict = dict_board(u)
        if complete_check(u_dict):
            return d, preds, u
        for new_board, d_pos in neighbors(u_dict):
            new_dist = d + d_pos
            if new_dist < dist.get(new_board, float('inf')):
                dist[new_board] = new_dist
                preds[new_board] = u
                heappush(Q, (new_dist, new_board))


def make_first_board(input: str) -> DBoard:
    input = input.split("\n")
    the_board = BLANK_FIRST_GAME.copy()
    for col in [2, 4, 6, 8]:
        for row in [1, 2]:
            the_board[col,row] = input[row+1][col+1]
    return the_board


def make_second_board(input: str) -> DBoard:
    input = input.split("\n")
    the_board = BLANK_SECOND_GAME.copy()
    for col in [2, 4, 6, 8]:
        for row in [1, 2]:
            use_row = 1 if row == 1 else 4
            the_board[col,use_row] = input[row+1][col+1]
    return the_board


def solve_day_23(input: str) -> tuple[int, int]:
    board_1 = make_first_board(input)
    t_init = tuple_board(board_1)
    ans_1, preds, final = shortest_path_length(t_init)

    board_2 = make_second_board(input)
    t_init = tuple_board(board_2)
    ans_2, preds, final = shortest_path_length(t_init)
    
    return ans_1, ans_2

# # For visualizing the moves:
# def plot_board(board):
#     if isinstance(board, tuple):
#         board = dict_board(board)
#     s = ""
#     for y in range(0, 5):
#         if (2, y) not in board:
#             continue
#         for i in range(0, 11):
#             if (i,y) in board:
#                 v = board[i, y]
#                 v = '.' if v in ['X', ''] else v
#             else:
#                 v = ' '
#             s += v
#         s += "\n"
#     print(s)
#
# def backtrack(preds, final):
#     res = [final]
#     while preds[res[-1]] is not None:
#         res.append(preds[res[-1]])
#     return res[::-1]
#
# # THEN:
# t_init = tuple_board(some_start_board)
# dist, preds, final = shortest_path_length(t_init)
# for board in backtrack(preds, final):
#     plot_board(board)

