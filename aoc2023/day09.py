import logging
from typing import Iterable

logger = logging.getLogger()


def parse_input(lines: Iterable[str]) -> Iterable[list[int]]:
    for line in lines:
        yield [int(x) for x in line.split()]


History = list[int]
Ends = list[int]


def diff_history(histories: list[History]) -> History:
    if all([x == 0 for x in histories[-1]]):
        return list(reversed(histories))

    history = histories[-1]
    diff = [history[i] - history[i - 1] for i in range(1, len(history))]
    histories.append(diff)
    return diff_history(histories)


def predict_next(histories: list[History]) -> int:
    deltas = [h[-1] for h in histories]
    out = [0 for _ in deltas]

    for i in range(1, len(out)):
        out[i] = deltas[i] + out[i - 1]
    logger.debug(out)
    return out[-1]


def part_one(lines: Iterable[str]) -> int:
    histories = parse_input(lines)
    out = 0
    for history in histories:
        diffs = diff_history([history])
        result = predict_next(diffs)

        out += result

    return out


def predict_previous(histories: list[History]) -> int:
    deltas = [h[0] for h in histories]
    out = [0 for _ in deltas]

    for i in range(1, len(out)):
        out[i] = deltas[i] - out[i - 1]
    logger.debug(out)
    return out[-1]


def part_two(lines: Iterable[str]) -> int:
    histories = parse_input(lines)
    out = 0
    for history in histories:
        diffs = diff_history([history])
        result = predict_previous(diffs)

        out += result

    return out
