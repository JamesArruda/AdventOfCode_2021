from advent2021.solutions import day_solvers
from advent2021.helpers import get_day
from pathlib import Path
# Edit to your liking
INPUT_DIR = Path(__file__).parent / "resources/InputFiles"
SESSION_FILE = Path(__file__).parent / "resources/session_id"


for day in range(1, 26):
    func = day_solvers.get(day, None)
    if func is None:
        continue
    print(f"Solving Day {day:02d}")
    input = get_day(day, INPUT_DIR, SESSION_FILE)
    ans1, ans2 = func(input)
    print(f"\t{ans1}\n\t{ans2}")
    print()