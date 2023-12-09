from __future__ import annotations
from dataclasses import dataclass
import logging
from typing import Iterable

logger = logging.getLogger()


@dataclass
class ScratchCard:
    card_id: int
    winners: set[int]
    numbers: set[int]

    @staticmethod
    def from_line(line: str) -> ScratchCard:
        # Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53
        card, digits = line.split(":")
        _, card_id = card.split()

        win, num = digits.split("|")
        winners = set([int(x) for x in win.split()])
        numbers = set([int(x) for x in num.split()])

        return ScratchCard(card_id=int(card_id), winners=winners, numbers=numbers)

    def calculate_points(self) -> int:
        if (i := self.calculate_matches()) > 0:
            return 2 ** (i - 1)
        else:
            return 0

    def calculate_matches(self) -> int:
        return len(self.winners.intersection(self.numbers))


def part_one(lines: Iterable[str]) -> int:
    out = 0
    for line in lines:
        card = ScratchCard.from_line(line)
        out += card.calculate_points()

    return out


CardDict = dict[int, ScratchCard]


def resolve_card(card: ScratchCard, card_dict: CardDict, running_total=0):
    matches = card.calculate_matches()

    if matches == 0:
        logger.debug(f"Card {card.card_id}: no children")
        return 1

    else:
        children = [card.card_id + i + 1 for i in range(card.calculate_matches())]
        logger.debug(f"Card {card.card_id}: {len(children)} children ({children})")
        return (
            sum([resolve_card(card_dict[child], card_dict) for child in children]) + 1
        )


def part_two(lines: str) -> int:
    cards = (ScratchCard.from_line(line) for line in lines)
    card_dict: CardDict = {card.card_id: card for card in cards}

    out = 0

    for card in card_dict:
        out += resolve_card(card_dict[card], card_dict)

    return out


# TODO: works but it's slow
# * don't recalculate matches and points every time (use a frozen dataclass)
# * save result from previous resolution of a card -- it's the same every time

