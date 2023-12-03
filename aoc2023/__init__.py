

from pathlib import Path


def read_lines(fp: str):
    fp = Path(fp)
    with fp.open() as file:
        for line in file:
            yield str(line).strip()
    