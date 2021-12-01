from pathlib import Path
import requests
from itertools import *
from collections import *
import numpy as np


BASE_PATH = Path("./InputFiles")
URL = "https://adventofcode.com/2021/day/{}/input"


def do_get(day: int, session_id: str) -> str:
    """Using your Advent of Code session id cookie (F12 is your friend),
    grab the input file.
    """
    use_url = URL.format(day)
    res = requests.get(use_url, cookies={'session':session_id})
    return res.text


def make_day(day: int, session_id: str) -> str:
    """Make or read the input file for the day.
    Reading preferred so we don't hammer the
    fine folk's server at Advent of Code.
    """
    fname = f"day{day:02d}.txt"
    f = BASE_PATH / fname
    if f.exists():
        print("Data already exists")
        with open(BASE_PATH / fname, 'r') as f:
            return f.read().strip()
    print("Getting the data and writing it")
    txt = do_get(day, session_id)
    with open(BASE_PATH / fname, 'w') as f:
        f.write(txt.strip())
    return txt


def load_session_id() -> str:
    with open("session_id", "r") as fp:
        return fp.read().strip()