import importlib
import re
from pathlib import Path
HERE = Path(__file__).parent

fmatch = re.compile("day_(\d+).py")
day_solvers = {}
files = [f for f in HERE.iterdir() if fmatch.match(f.name)]
for f in files:
    day = int(fmatch.match(f.name).groups()[0])
    mod = importlib.import_module(f"advent2021.solutions.{f.stem}")
    func_name = [x for x in dir(mod) if "solve_day_" in x][0]
    day_solvers[day] = getattr(mod, func_name)