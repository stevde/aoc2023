from __future__ import annotations
from ast import List
from curses.ascii import isdigit
from dataclasses import dataclass, field
import logging
from typing import Iterable


logger = logging.getLogger()


@dataclass(eq=True, frozen=True)
class Coord:
    x: int
    y: int

    def __add__(self, other: Coord) -> Coord:
        return Coord(self.x + other.x, self.y + other.y)


@dataclass(eq=False)
class PartNumber:
    value: int
    coords: list[Coord] = field(default_factory=list)

    def update(self, char: str, coord: Coord) -> None:
        self.value = int(str(self.value) + str(char))
        self.coords.append(coord)


def is_symbol(char: str) -> bool:
    return not (char.isdigit() or char == ".")


@dataclass
class EngineBlock:
    symbols: dict[Coord, str] = field(default_factory=dict)
    numbers: dict[Coord, PartNumber] = field(default_factory=dict)

    def __init__(self) -> None:
        self.symbols = dict()
        self.numbers = dict()

    def add_symbol(self, symbol: str, coord: Coord):
        self.symbols[coord] = symbol

    def get_symbol(self, coord: Coord):
        return self.symbols.get(coord)

    def add_number(self, number: PartNumber, coord: Coord):
        self.numbers[coord] = number

    def get_number(self, coord: Coord) -> PartNumber:
        return self.numbers.get(coord)

    def load_block(self, input_lines: Iterable[str]) -> None:
        for y, line in enumerate(input_lines):
            for x, char in enumerate(line):
                current_location = Coord(x, y)
                if is_symbol(char):
                    self.add_symbol(char, current_location)

                # if digit, check back one to left -- if that's a number we can update
                elif char.isdigit():
                    previous = self.get_number(Coord(x - 1, y))

                    if previous:
                        previous.update(char, current_location)
                        self.add_number(previous, current_location)

                    # else it's a new number
                    else:
                        number = PartNumber(int(char))
                        number.coords.append(current_location)
                        self.add_number(number, current_location)

                # else it's a dot
                else:
                    pass

    def __getitem__(self, coord: Coord) -> str:
        return self.symbols.get(coord) or self.numbers.get(coord)


def vicinity(coord: Coord) -> list[Coord]:
    return [
        # row above
        Coord(coord.x - 1, coord.y + 1),
        Coord(coord.x, coord.y + 1),
        Coord(coord.x + 1, coord.y + 1),
        # same row
        Coord(coord.x - 1, coord.y),
        Coord(coord.x + 1, coord.y),
        # row below
        Coord(coord.x - 1, coord.y - 1),
        Coord(coord.x, coord.y - 1),
        Coord(coord.x + 1, coord.y - 1),
    ]


def get_numbers_in_vicinity(engine: EngineBlock, anchor: Coord) -> list[PartNumber]:
    numbers = set()
    for coord in vicinity(anchor):
        if (number := engine.get_number(coord)) is not None:
            numbers.add(number)

    return list(numbers)


def part_one(data):
    engine = EngineBlock()
    engine.load_block(data)

    numbers = set()
    for coord in engine.symbols:
        adjacent_numbers = get_numbers_in_vicinity(engine, coord)
        numbers.update(adjacent_numbers)

    return sum([n.value for n in numbers])


def part_two(data):
    engine = EngineBlock()
    engine.load_block(data)

    out = 0

    for coord, symbol in engine.symbols.items():
        if symbol == "*":
            numbers = get_numbers_in_vicinity(engine, coord)
            if len(numbers) == 2:
                a, b = numbers[0].value, numbers[1].value
                out += a * b
                logger.info(f"{symbol} found at {coord}: {a} x {b} = {a*b}")
                logger.info(f"Running total: {out}")

    return out
