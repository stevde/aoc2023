from dataclasses import dataclass, field
import re
from typing import Iterable

Cubes = dict[str, int]


@dataclass
class Round:
    number: int
    cubes: Cubes = field(default_factory=dict)


@dataclass
class Game:
    number: int
    rounds: list[Round] = field(default_factory=list)


RE_DIGIT = re.compile("\d+")


def parse_game(game: str):
    game_str, round_strs = game.split(":")

    game_number = int(RE_DIGIT.search(game_str).group(0))

    game = Game(number=game_number)

    for i, round_str in enumerate(round_strs.split(";")):
        round = Round(number=i)
        for cube_str in round_str.split(","):
            n, colour = cube_str.strip().split(" ")
            round.cubes[colour] = int(n)

        game.rounds.append(round)

    return game


def is_valid_game(cubes: Cubes, game: Game) -> bool:
    for round in game.rounds:
        for colour, n in round.cubes.items():
            if (colour not in cubes) or (n > cubes[colour]):
                return False

    return True


def part_one(cubes: Cubes, games: list[str]):
    out = 0
    for game_str in games:
        game: Game = parse_game(game_str)
        if is_valid_game(cubes, game):
            out += game.number

    return out


def get_min_cubes(game: Game) -> Cubes:
    out: Cubes = dict()
    for round in game.rounds:
        for colour, n in round.cubes.items():
            if (colour not in out) or (n > out[colour]):
                out[colour] = n

    return out


def get_power_cubes(cubes: Cubes) -> int:
    prod = 1
    for colour in ["red", "green", "blue"]:
        prod *= cubes.get(colour, 0)

    return prod


def part_two(games: list[str]) -> int:
    out = 0
    for game_str in games:
        game: Game = parse_game(game_str)
        cubes: Cubes = get_min_cubes(game)
        power = get_power_cubes(cubes)
        out += power

    return out