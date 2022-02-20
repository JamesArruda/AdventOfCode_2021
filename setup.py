from pathlib import Path
from setuptools import setup

HERE = Path(__file__).parent

def read(fname):
    return open(HERE / fname).read()


setup(
    name = "AdventOfCode_2021",
    version = "0.0.1",
    author = "James Arruda",
    author_email = "",
    description = ("Solutions and helpers to Advent of Code 2021"),
    license = "MIT",
    keywords = "AdventOfCode Python puzzles",
    url = "https://github.com/JamesArruda/AdventOfCode_2021",
    packages=['advent2021'],
    install_requires=read('requirements.txt').splitlines(),
    long_description=read('README.md'),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Topic :: Games/Entertainment :: Puzzle Games",
        "License :: OSI Approved :: MIT License",
    ],
)
