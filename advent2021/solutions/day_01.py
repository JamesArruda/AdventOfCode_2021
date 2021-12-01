from advent2021.helpers import *

raw_data = get_day(1)
data = list(map(int, raw_data.split("\n")))

# Part 1
ans_1 = (np.diff(data) > 0).sum()

# Part 2
window = np.convolve(
    data,
    np.ones(3),
    'valid',
)
ans_2 = (np.diff(window) > 0).sum()

print(f"Day 1\nPart 1: {ans_1}\nPart 2: {ans_2}")
