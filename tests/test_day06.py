import pytest
from aoc2023 import read_lines
from aoc2023.day06 import (
    n_winners,
    parse_input,
    parse_input_kerning,
    part_one,
    part_two,
)


def test_parse_input():
    lines = [
        "Time:      7  15   30",
        "Distance:  9  40  200",
    ]

    times, distances = parse_input(lines)
    assert times == [7, 15, 30]
    assert distances == [9, 40, 200]


def test_n_winners():
    assert n_winners(7, 9) == 4


@pytest.fixture
def test_data():
    return read_lines("data/day06.txt")


def test_part_one(test_data):
    assert part_one(test_data) == 608902


def test_parse_input_kerning():
    lines = [
        "Time:      7  15   30",
        "Distance:  9  40  200",
    ]

    time, distance = parse_input_kerning(lines)
    assert time == 71530
    assert distance == 940200


def test_part_two(test_data):
    assert part_two(test_data) == 46173809
