from pathlib import Path
import requests

URL = "https://adventofcode.com/2021/day/{}/input"
FILE_NAMER = "day{:02d}.txt"


def do_get(day: int, session_id: str) -> str:
    """Using your Advent of Code session id cookie (F12 is your friend),
    grab the input file.
    """
    use_url = URL.format(day)
    res = requests.get(use_url, cookies={'session':session_id})
    return res.text


def make_day(day: int, input_dir: Path, session_path: Path):
    """Make or read the input file for the day.
    Reading preferred so we don't hammer the
    fine folk's server at Advent of Code.
    """
    session_id = load_session_id(session_path)
    txt = do_get(day, session_id)
    if not input_dir.exists():
        input_dir.mkdir()
    fname = FILE_NAMER.format(day)
    with open(input_dir / fname, 'w') as f:
        f.write(txt.strip())


def get_day(day: int, input_dir: Path, session_path: Path) -> str:
    """Read the input file for the day. 
    Make it if it does not exist.
    Returns the input data.
    """
    fname = FILE_NAMER.format(day)
    f = input_dir / fname
    if not f.exists():
        make_day(day, input_dir, session_path)
    
    with open(f, 'r') as f:
        return f.read().strip()    


def load_session_id(session_path) -> str:
    with open(session_path, "r") as fp:
        return fp.read().strip()