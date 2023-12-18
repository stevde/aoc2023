from __future__ import annotations
from dataclasses import dataclass, field
import logging
import math
from turtle import left, right
from typing import Iterable

FORMAT = "%(levelname) %(message)s"
logging.basicConfig(format=FORMAT)
logger = logging.getLogger()


class Connector:
    def __init__(self, source: int, destination: int, span: int):
        self.source = source
        self.destination = destination
        self.span = span

    def __contains__(self, value: int):
        return (value >= self.source) and (value < self.source + self.span)

    def map(self, value: int):
        if value not in self:
            raise ValueError(f"{value=} not in connector")
        offset = value - self.source
        return self.destination + offset


def parse_seeds(line: str) -> list[int]:
    _, values = line.split(":")
    return [int(x) for x in values.strip().split()]


def parse_connector(line: str) -> tuple[int]:
    values = line.split()
    # note the switch of order
    source, destination, span = int(values[1]), int(values[0]), int(values[2])
    return source, destination, span


@dataclass
class FarmMap:
    name: str = None
    connectors: list[Connector] = field(default_factory=list)


@dataclass
class Almanac:
    seeds: list[int] = field(default_factory=list)
    maps: list[FarmMap] = field(default_factory=list)

    def map(self, seed: int) -> int:
        logger.debug(f"{seed=}")
        for farm_map in self.maps:
            logger.debug(f"{farm_map.name}:")
            for connector in farm_map.connectors:
                if seed in connector:
                    seed = connector.map(seed)
                    break
            logger.debug(f"-> {seed}")
        return seed


def parse_input(lines: Iterable[str]):
    lines = list(lines)
    almanac = Almanac()
    almanac.seeds = parse_seeds(lines[0])
    i = j = 0
    while i < len(lines):
        if lines[i].endswith("map:"):
            farm_map = FarmMap()
            farm_map.name = lines[i].split()[0]
            j = i + 1
            while j < len(lines) and lines[j] != "":
                source, destination, span = parse_connector(lines[j])
                connector = Connector(source, destination, span)
                farm_map.connectors.append(connector)
                j += 1
            almanac.maps.append(farm_map)
        i += 1

    return almanac


def part_one(lines: Iterable[str]) -> int:
    almanac = parse_input(lines)
    out = math.inf
    for seed in almanac.seeds:
        loc = almanac.map(seed)
        if loc < out:
            out = loc

    return out


@dataclass
class Span:
    left: int
    right: int

    def __repr__(self) -> str:
        return f"Span({self.left}, {self.right})"

    def __contains__(self, other: Span) -> bool:
        return (self.left <= other.left) and (self.right >= other.right)

    def overlaps(self, other: Span) -> bool:
        return not (self.right < other.left or self.left > other.right)

    def slice(self, other: Span) -> tuple[Span, list[Span]]:
        leftovers = list()

        # no overlap
        #  self      |      |
        #  other                |      |
        if not self.overlaps(other):
            return None, leftovers

        # other fully covers self -> return self, no leftovers
        #  self      |      |
        #  other   |                   |
        elif other.left <= self.left and other.right >= self.right:
            span = self

        # self fully covers other -> return other + 2 leftovers
        #  self   |                        |
        #  other     |                 |
        elif self.left < other.left and self.right > other.right:
            span = other
            leftovers.append(Span(self.left, other.left - 1))
            leftovers.append(Span(self.right + 1, other.right))

        # self overlaps on the left -> return top of self, + 1 leftover
        #  self   |         |
        #  other     |                 |
        elif self.left < other.left:
            span = Span(other.left, self.right)
            leftovers.append(Span(self.left, other.left - 1))

        # self overlaps on the right -> return bottom of self, + 1 leftover
        #  self              |         |
        #  other     |             |
        else:
            span = Span(self.left, other.right)
            leftovers.append(Span(other.right + 1, self.right))

        return span, leftovers


@dataclass
class SpanConnector:
    source: Span
    destination: Span

    def __contains__(self, span: Span) -> bool:
        return span in self.source

    def map(self, span: Span) -> Span:
        if span not in self.source:
            return ValueError(f"{span} not in {self}")

        offset = self.destination.left - self.source.left
        return Span(span.left + offset, span.right + offset)


@dataclass
class SpanMap:
    name: str = None
    connectors: list[SpanConnector] = field(default_factory=list)

    def __contains__(self, span: Span):
        return any([span in connector for connector in self.connectors])


def parse_span_seeds(seeds: list[int]) -> list[Span]:
    ks = range(0, len(seeds), 2)
    vs = range(1, len(seeds), 2)

    out = list()
    for k, v in zip(ks, vs):
        out.append(Span(seeds[k], seeds[k] + seeds[v] - 1))

    return out


@dataclass
class SpanAlmanac:
    seeds: list[Span] = field(default_factory=list)
    maps: list[SpanMap] = field(default_factory=list)

    # def map(self, seeds: Span) -> Span:
    #     logger.debug(f"{seed=}")
    #     for farm_map in self.maps:
    #         logger.debug(f"{farm_map.name}:")
    #         for connector in farm_map.connectors:
    #             if seed in connector:
    #                 logger.debug(f"! {connector.source}")
    #                 seed = connector.map(seed)
    #                 break
    #             logger.debug(f"? {connector.source}")
    #         logger.debug(f"-> {seed}")
    #     return seed

    def map(self, seeds: list[Span], idx: int = 0) -> Span:
        # if we're out of maps, return seeds unchanged
        if idx >= len(self.maps):
            return seeds

        # pick map we're on
        farm_map = self.maps[idx]
        logger.debug(f"{farm_map.name}: {len(seeds)} seeds")

        # mapped seeds to carry to next map
        next_seeds = list()

        # while seeds in input,
        while seeds:
            seed = seeds.pop()
            logger.debug(f"~ {seed}")
            for connector in farm_map.connectors:
                # if it overlaps with any connector
                if seed.overlaps(connector.source):  # TODO
                    logger.debug(f"! {connector.source}")
                    # map the overlapping part
                    seed, leftovers = seed.slice(connector.source)  # TODO
                    seed = connector.map(seed)
                    next_seeds.append(seed)
                    logger.debug(f"> {seed}")
                    # add leftovers to seeds to process
                    for lo in leftovers:
                        seeds.append(lo)
                        logger.debug(f"lo {lo}")
                    # break out of this iteration of for loop
                    break
                # logger.debug(f"? {connector.source}")
            else:
                # if no overlaps found, maps to self
                next_seeds.append(seed)
                logger.debug(f"-> {seed}")

        # once all seeds are mapped, recurse with next map
        return self.map(next_seeds, idx=idx + 1)


def parse_span_input(lines: Iterable[str]):
    lines = list(lines)
    almanac = SpanAlmanac()
    almanac.seeds = parse_span_seeds(parse_seeds(lines[0]))
    i = j = 0
    while i < len(lines):
        if lines[i].endswith("map:"):
            farm_map = SpanMap()
            farm_map.name = lines[i].split()[0]
            j = i + 1
            while j < len(lines) and lines[j] != "":
                source, destination, width = parse_connector(lines[j])
                connector = SpanConnector(
                    Span(source, source + width), Span(destination, destination + width)
                )
                farm_map.connectors.append(connector)
                j += 1
            almanac.maps.append(farm_map)
        i += 1

    return almanac


def part_two(lines: Iterable[str]) -> int:
    almanac = parse_span_input(lines)
    locations = almanac.map(almanac.seeds)
    logger.debug(f"Final locations: {locations}")
    return min([loc.left for loc in locations])
