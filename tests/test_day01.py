from random import sample
import pytest
from aoc2023 import read_lines

from aoc2023.day01 import (
    get_calibration_advanced,
    get_calibration_value,
    get_first_and_last,
    part_one,
    part_two,
)


@pytest.fixture
def sample_part_one():
    return [
        "1abc2",
        "pqr3stu8vwx",
        "a1b2c3d4e5f",
        "treb7uchet",
    ]


@pytest.fixture
def expected():
    return [
        12,
        38,
        15,
        77,
    ]


@pytest.fixture
def test_data():
    return read_lines("data/day01.txt")


def test_get_calibration_value(sample_part_one: list[str], expected: list[int]):
    for key, value in zip(sample_part_one, expected):
        assert get_calibration_value(key) == value


def test_part_one_sample(sample_part_one: list[str]):
    assert part_one(sample_part_one) == 142


def test_part_one(test_data: str):
    assert part_one(test_data) == 53080


@pytest.fixture
def sample_part_two():
    return [
        "two1nine",
        "eightwothree",
        "abcone2threexyz",
        "xtwone3four",
        "4nineeightseven2",
        "zoneight234",
        "7pqrstsixteen",
    ]


def test_get_first_and_last():
    assert get_first_and_last("two1nine") == ("2", "9")
    assert get_first_and_last("zoneight234") == ("1", "4")


def test_get_calibration_advanced(sample_part_two: list[str]):
    expected = [29, 83, 13, 24, 42, 14, 76]
    for key, value in zip(sample_part_two, expected):
        assert get_calibration_advanced(key) == value


def test_part_two_sample(sample_part_two: list[str]):
    assert part_two(sample_part_two) == 281


def test_part_two_overlapping():
    assert get_calibration_advanced("nineight") == 98


def test_part_two(test_data: str):
    assert part_two(test_data) == 53268
