import pytest
from aoc2023 import read_lines
from aoc2023.day02 import Cubes, Game, is_valid_game, parse_game, part_one, part_two


def test_parse_game():
    string = "Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green"
    game = parse_game(string)

    assert isinstance(game, Game)

    assert game.number == 1
    assert len(game.rounds) == 3

    assert game.rounds[0].number == 0
    assert game.rounds[0].cubes["blue"] == 3
    assert game.rounds[0].cubes["red"] == 4

    assert game.rounds[1].number == 1
    assert game.rounds[1].cubes["red"] == 1
    assert game.rounds[1].cubes["green"] == 2
    assert game.rounds[1].cubes["blue"] == 6

    assert game.rounds[2].number == 2
    assert game.rounds[2].cubes["green"] == 2


@pytest.fixture
def sample_part_one():
    return [
        "Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green",
        "Game 2: 1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue",
        "Game 3: 8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red",
        "Game 4: 1 green, 3 red, 6 blue; 3 green, 6 red; 3 green, 15 blue, 14 red",
        "Game 5: 6 red, 1 blue, 3 green; 2 blue, 1 red, 2 green",
    ]


def test_is_valid_game(sample_part_one):
    bag: Cubes = {"red": 12, "green": 13, "blue": 14}
    expected_results = [True, True, False, False, True]
    for game_str, as_expected in zip(sample_part_one, expected_results):
        game = parse_game(game_str)
        assert is_valid_game(bag, game) is as_expected


@pytest.fixture
def test_data():
    return read_lines("data/day02.txt")


def test_part_one(test_data):
    bag: Cubes = {"red": 12, "green": 13, "blue": 14}
    assert part_one(bag, test_data) == 2879


def test_part_two(test_data):
    assert part_two(test_data) == 65122