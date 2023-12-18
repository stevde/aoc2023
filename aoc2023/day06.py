import logging
from typing import Iterable

logger = logging.getLogger()


def parse_input(lines: Iterable[str]) -> tuple[list[int], list[int]]:
    times = list()
    distances = list()

    for i, line in enumerate(lines):
        record = line.split()

        if i == 0:
            times = [int(x) for x in record[1:]]
        if i == 1:
            distances = [int(x) for x in record[1:]]

    return times, distances


def n_winners(time, record) -> int:
    logger.debug(f"Time: {time}  Record: {record}")
    t = 0

    while t < time and t * (time - t) < record:
        t += 1

    logger.debug(f"{t=}")
    return time + 1 - 2 * t


def part_one(lines: Iterable[str]) -> int:
    times, distances = parse_input(lines)

    out = 1
    for t, d in zip(times, distances):
        out *= n_winners(t, d)

    return out


def parse_input_kerning(lines: Iterable[str]) -> tuple[list[int], list[int]]:
    times = list()
    distances = list()

    for i, line in enumerate(lines):
        record = line.split(":")

        if i == 0:
            times = int(record[1].replace(" ", ""))
        if i == 1:
            distances = int(record[1].replace(" ", ""))

    return times, distances


def part_two(lines: Iterable[str]) -> int:
    time, distance = parse_input_kerning(lines)
    return n_winners(time, distance)
