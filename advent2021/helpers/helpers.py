from pathlib import Path
import requests
import advent2021


BASE_PATH = Path(advent2021.__path__[0])
INPUT_FOLDER = BASE_PATH / "resources"/ "InputFiles"
SESSION_FILE = BASE_PATH / "resources"/ "session_id"
URL = "https://adventofcode.com/2021/day/{}/input"
FILE_NAMER = "day{:02d}.txt"


def do_get(day: int, session_id: str) -> str:
    """Using your Advent of Code session id cookie (F12 is your friend),
    grab the input file.
    """
    use_url = URL.format(day)
    res = requests.get(use_url, cookies={'session':session_id})
    return res.text


def make_day(day: int) -> str:
    """Make or read the input file for the day.
    Reading preferred so we don't hammer the
    fine folk's server at Advent of Code.
    """
    session_id = load_session_id()
    txt = do_get(day, session_id)
    if not INPUT_FOLDER.exists():
        INPUT_FOLDER.mkdir()
    fname = FILE_NAMER.format(day)
    with open(INPUT_FOLDER / fname, 'w') as f:
        f.write(txt.strip())


def get_day(day: int) -> str:
    """Read the input file for the day. 
    Make it if it does not exist.
    Returns the input data.
    """
    fname = FILE_NAMER.format(day)
    f = INPUT_FOLDER / fname
    if not f.exists():
        make_day(day)
    
    with open(f, 'r') as f:
        return f.read().strip()    


def load_session_id() -> str:
    with open(SESSION_FILE, "r") as fp:
        return fp.read().strip()