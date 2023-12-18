import logging
import pytest
from aoc2023 import read_lines
from aoc2023.day05 import (
    Connector,
    Span,
    SpanAlmanac,
    parse_input,
    parse_span_input,
    parse_span_seeds,
    part_one,
    part_two,
)

logger = logging.getLogger()


def test_range_connector():
    connector = Connector(98, 50, 2)

    assert 10 not in connector
    assert 98 in connector
    assert 99 in connector

    with pytest.raises(ValueError):
        assert connector.map(10) == 10
    assert connector.map(98) == 50
    assert connector.map(99) == 51

    connector = Connector(50, 52, 48)
    for value, expected in zip(range(50, 98), range(52, 100)):
        assert connector.map(value) == expected


@pytest.fixture
def sample_data():
    return [
        "seeds: 79 14 55 13",
        "",
        "seed-to-soil map:",
        "50 98 2",
        "52 50 48",
        "",
        "soil-to-fertilizer map:",
        "0 15 37",
        "37 52 2",
        "39 0 15",
        "",
        "fertilizer-to-water map:",
        "49 53 8",
        "0 11 42",
        "42 0 7",
        "57 7 4",
        "",
        "water-to-light map:",
        "88 18 7",
        "18 25 70",
        "",
        "light-to-temperature map:",
        "45 77 23",
        "81 45 19",
        "68 64 13",
        "",
        "temperature-to-humidity map:",
        "0 69 1",
        "1 0 69",
        "",
        "humidity-to-location map:",
        "60 56 37",
        "56 93 4",
    ]


def test_parse_input(sample_data):
    almanac = parse_input(sample_data)
    assert almanac.seeds == [79, 14, 55, 13]
    assert len(almanac.maps) == 7


def test_almanac(sample_data):
    almanac = parse_input(sample_data)
    assert almanac.map(79) == 82
    assert almanac.map(14) == 43
    assert almanac.map(55) == 86
    assert almanac.map(13) == 35


def test_part_one_sample(sample_data):
    assert part_one(sample_data) == 35


@pytest.fixture
def test_data():
    return read_lines("data/day05.txt")


def test_part(test_data):
    assert part_one(test_data) == 51580674


def test_span():
    assert Span(3, 5) == Span(3, 5)
    assert Span(3, 5) in Span(3, 5)
    assert Span(3, 5) in Span(2, 6)
    assert Span(3, 5) not in Span(4, 6)


def test_parse_span_seeds():
    seeds = [79, 14, 55, 13]
    assert parse_span_seeds(seeds) == [Span(79, 92), Span(55, 67)]


def test_parse_span_input(sample_data):
    almanac = parse_span_input(sample_data)
    assert isinstance(almanac, SpanAlmanac)

    assert almanac.seeds == [Span(79, 92), Span(55, 67)]
    assert len(almanac.maps) == 7


def test_part_two_sample(sample_data):
    assert part_two(sample_data) == 46


def test_part_two(test_data):
    # This is the correct answer, but my current implementation is off by one
    assert part_two(test_data) == 99751240
