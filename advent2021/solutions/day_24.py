"""
I solved this one manually first.

Since this is an assembly-like language, many of the operations 'merge' down
into simpler operations/if statements. 
    `mul x 0`
    `add x z`
Is just setting x = z, for example.

The trick is figuring out that there are two kinds of computational blocks.
The input is a number, which is really a string of 14 1-9 integers.
Each of those 14 1-9 numbers goes to a computation block.

There is a running number that is returned at the end that starts at 0.
The running number is `z`, which is updated after each block.

The blocks either:
    1. Increase the running number according to the input and a constant.
        z = z * 26 + (input + constant)
    2. Based on conditions, reduces z by integer division with 26
        If z < 26, that means 0, which is what we want
        The block sets: x = z % 26 + testing constant
        The block also sets: z = z // 26
        Now z is some smaller number, possible 0.
        Then, if x != input:
            z is increased like Block 1
The second block forces us to pick a number that doesn't equal x, so 
z never gets bigger.

The second block type, due to the integer division, has the effect of
ignoring an increase block earlier in the chain.

The input should have 7 of each kind, with the running total of each type
always having the first type as more or equal (so they can be cancelled).

Get each block by finding the `inp w` starting points.
Blocks of type 1 have: `div z 1`
    The constant is found at:
        `div z 1`
        `add x 15` <- the constant


Blocks of type 2 have: `div z 26`
    The testing constant is found at:
        `div z 26`
        `add x -14` <- the testing constant

I called Type 1 blocks 'increase' (constant).
         Type 2 blocks 'test' (test constant, increase constant if fail).
We can ignore the increase constants in the test blocks.

My input was:
blocks = [
          (increase, 15),
          (increase, 5),
          (increase, 6),
          (test, -14, 7),
          (increase, 9),
          (test, -7, 6),
          (increase, 14),
          (increase, 3),
          (increase, 1),
          (test, -7, 3),
          (test, -8, 4),
          (test, -7, 6),
          (test, -5, 7),
          (test, -10, 1),
]

Note these three blocks:
          (increase, 6),
          (test, -14, 7),
That's the first testing block, which negates the previous
increase block.
Since the increase constant is 6, we know that within test:
    x = z % 26 - 14
    AND
    z = prev_z * 26 + (prev_input + 6)
    THEREFORE:
    x = (prev_z * 26 + (prev_input + 6)) % 26 - 14
    x = (prev_input + 6) % 26 - 14

Note that the mod strips the previous multiplication off. We only care
about the previous input value and the constant.

Our current input, w, must equal x.
Since ([1-9] + 6) % 26 = [1-9] + 6,
    x = [1-9] + 6 - 14
    x = [1-9] - 8
That has to be at least 1, so prev_input is either 9 or 8.
That makes x = 0 or 1
For picking the max, we want the previous number to be the largest.
That means we pick the previous input to be 9.

Following the path of all the pairs of test-increase blocks that need 
to cancel each other, the min and max input numbers can be found.

This is simple to set up as a series of equations in the Z3 solver.
Thanks to the hakank page for some helpful hints on building good
z3 code: https://github.com/hakank/hakank/blob/master/z3/z3_utils_hakank.py
"""
from typing import List, Union
from z3 import Solver, Int, Or, Model


def make_int(sol: Solver, name: str) -> Int:
    v = Int(name)
    sol.add(v >= 1, v <= 9)
    return v


def force_different(
    sol:Solver,
    mod:Model,
    *params:List[Int],
) -> None:
    for t in params:
        sol.add(Or([t[i] != mod.eval(t[i]) for i in range(len(t))]))
        

def eval_array(mod:Model, a:List[Int]):
    return [mod.eval(a[i]) for i in range(len(a))]


def get_all(sol:Solver, variables:List[Int], lim:Union[int, None]=None):
    answers = []
    while sol.check().r == 1:
        mod = sol.model()
        xs = eval_array(mod, variables)
        answers.append(xs)
        force_different(sol, mod, variables)
        if lim is not None and len(answers) == lim:
            return answers
    return answers


def block_maker(input:str) -> tuple[str, int]:
    blocks = []
    split_inp = input.split("\n")
    for i, l in enumerate(split_inp):
        if l == "div z 1":
            blocks.append(["increase"])
        elif l == "div z 26":
            l2 = split_inp[i+1]
            const = int(l2.split(" ")[-1])
            blocks.append(["test", const])
        elif l == "add y w":
            const = int(split_inp[i+1].split(" ")[-1])
            if blocks[-1][0] == 'increase':
                blocks[-1].append(const)
    return tuple(blocks)


def solve_day_24(input:str) -> tuple[int, int]:
    blocks = block_maker(input)
    # build the limiting equations
    pairs = []
    increasers = []
    for i, block in enumerate(blocks):
        if block[0] == 'increase':
            increasers.append((block[1], i))
        elif block[0] == 'test':
            c1, i1 = increasers.pop(-1)
            p = (c1, i1, block[1], i)
            pairs.append(p)

    # set it up in z3
    sol = Solver()
    the_nums = [make_int(sol, f"{i}") for i in range(14)]
    for p in pairs:
        c1, i1, c2, i2 = p
        sol.add(
            (the_nums[i1] + c1) % 26 + c2 == the_nums[i2]
        )
    # TODO: Use the built-in z3 min and max features to do this automatically
    res = get_all(sol, the_nums, lim=None)
    nums = [int(''.join([a.as_string() for a in r])) for r in res]

    ans_1 = max(nums)
    ans_2 = min(nums)
    return ans_1, ans_2