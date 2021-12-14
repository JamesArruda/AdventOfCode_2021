from advent2021.solutions import day_solvers
from advent2021.helpers import get_day
from pathlib import Path
# Edit to your liking
INPUT_DIR = Path(__file__).parent / "resources/InputFiles"
SESSION_FILE = Path(__file__).parent / "resources/session_id"


def _str_fmt(ans: str) -> str:
    new = ""
    for i, l in enumerate(ans.split("\n")):
        pre = "\t" if i else ""
        new += pre + l + "\n"
    return new


for day in range(1, 26):
    func = day_solvers.get(day, None)
    if func is None:
        continue
    print(f"Solving Day {day:02d}")
    input = get_day(day, INPUT_DIR, SESSION_FILE)
    ans1, ans2 = func(input)
    if isinstance(ans2, str):
        ans2 = _str_fmt(ans2)
    print(f"\t{ans1}\n\t{ans2}")
    print()