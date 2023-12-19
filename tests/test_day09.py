import logging

import pytest
from aoc2023 import read_lines
from aoc2023.day09 import diff_history, parse_input, part_one, part_two, predict_next


logger = logging.getLogger()


def test_parse_input():
    data = [
        "0 3 6 9 12 15",
        "1 3 6 10 15 21",
        "10 13 16 21 30 45",
    ]
    histories = parse_input(data)
    for history in histories:
        assert len(history) == 6


def test_diff_history():
    data = [
        "0 3 6 9 12 15",
    ]
    history = next(parse_input(data))
    diffs = diff_history([history])
    assert len(diffs) == 3
    for diff in diffs:
        logger.debug(diff)


def test_predict_next():
    data = [
        "0 3 6 9 12 15",
        "1 3 6 10 15 21",
        "10 13 16 21 30 45",
    ]
    expected_values = [18, 28, 68]
    histories = parse_input(data)

    for history, expected in zip(histories, expected_values):
        diffs = diff_history([history])
        result = predict_next(diffs)

        assert result == expected


@pytest.fixture
def test_data():
    return read_lines("data/day09.txt")


def test_part_one(test_data):
    assert part_one(test_data) == 2101499000


def test_part_two(test_data):
    assert part_two(test_data) == 2101499000
