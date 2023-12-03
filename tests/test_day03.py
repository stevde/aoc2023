import logging
import pytest

from aoc2023 import read_lines
from aoc2023.day03 import Coord, EngineBlock, part_one, part_two

logger = logging.getLogger()


@pytest.fixture
def sample_data():
    return [
        "467..114..",
        "...*......",
        "..35..633.",
        "......#...",
        "617*......",
        ".....+.58.",
        "..592.....",
        "......755.",
        "...$.*....",
        ".664.598..",
    ]


@pytest.fixture
def test_data():
    return read_lines("data/day03.txt")


def test_engine_block(sample_data):
    engine = EngineBlock()
    engine.load_block(sample_data)

    assert engine[Coord(0, 0)].value == 467
    assert engine[Coord(1, 0)].value == 467

    assert engine[Coord(0, 0)] is engine[Coord(1, 0)]

    assert Coord(3, 1) in engine.symbols
    assert engine[Coord(3, 1)] == "*"


def test_part_one_sample(sample_data):
    assert part_one(sample_data) == 4361


def test_part_one_sample(test_data):
    assert part_one(test_data) == 514969


def test_part_two_sample(sample_data):
    assert part_two(sample_data) == 467835


def test_part_two_sample(test_data):
    assert part_two(test_data) == 514969
