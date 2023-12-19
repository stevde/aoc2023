import logging

import pytest
from aoc2023 import read_lines
from aoc2023.day08 import RE_NODE, RE_NODE, parse_input, part_one, part_two

logger = logging.getLogger()


def test_regex():
    line = "NBN = (BKF, NNH)"
    logger.debug(RE_NODE)
    match = RE_NODE.findall(line)
    node, left, right = match[0], match[1], match[2]
    assert node == "NBN"
    assert left == "BKF"
    assert right == "NNH"


@pytest.fixture
def sample_data():
    return [
        "RL",
        "",
        "AAA = (BBB, CCC)",
        "BBB = (DDD, EEE)",
        "CCC = (ZZZ, GGG)",
        "DDD = (DDD, DDD)",
        "EEE = (EEE, EEE)",
        "GGG = (GGG, GGG)",
        "ZZZ = (ZZZ, ZZZ)",
    ]


def test_instructions(sample_data):
    instructions = parse_input(sample_data)
    assert instructions.directions == "RL"
    assert "AAA" in instructions.nodes
    AAA = instructions.nodes["AAA"]
    assert AAA.left == instructions.nodes["BBB"]
    assert AAA.left.left == instructions.nodes["DDD"]
    assert AAA.right.left == instructions.nodes["ZZZ"]


def test_part_one_sample(sample_data):
    assert part_one(sample_data) == 2

    another_example = [
        "LLR",
        "",
        "AAA = (BBB, BBB)",
        "BBB = (AAA, ZZZ)",
        "ZZZ = (ZZZ, ZZZ)",
    ]

    assert part_one(another_example) == 6


@pytest.fixture
def test_data():
    return read_lines("data/day08.txt")


def test_part_one(test_data):
    assert part_one(test_data) == 22199


def test_part_two_sample():
    yet_another_example = [
        "LR",
        "",
        "MMA = (MMB, XXX)",
        "MMB = (XXX, MMZ)",
        "MMZ = (MMB, XXX)",
        "NNA = (NNB, XXX)",
        "NNB = (NNC, NNC)",
        "NNC = (NNZ, NNZ)",
        "NNZ = (NNB, NNB)",
        "XXX = (XXX, XXX)",
    ]
    assert part_two(yet_another_example) == 6


def test_part_two_sample(test_data):
    assert part_two(test_data) == 13334102464297
