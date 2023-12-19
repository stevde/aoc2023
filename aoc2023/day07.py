from __future__ import annotations
from collections import Counter
from dataclasses import dataclass, field
from enum import Enum
import logging
from typing import Iterable

logger = logging.getLogger()


class Card(Enum):
    ACE = ("A", 14)
    KING = ("K", 13)
    QUEEN = ("Q", 12)
    JACK = ("J", 11)
    TEN = ("T", 10)
    X9 = ("9", 9)
    X8 = ("8", 8)
    X7 = ("7", 7)
    X6 = ("6", 6)
    X5 = ("5", 5)
    X4 = ("4", 4)
    X3 = ("3", 3)
    X2 = ("2", 2)
    JOKER = ("j", 1)

    def __new__(cls, char, rank):
        entry = object.__new__(cls)
        entry.char = entry._value_ = char
        entry.rank = rank
        return entry

    def __eq__(self, other: Card):
        return self.rank == other.rank

    def __hash__(self):
        return self.rank

    def __lt__(self, other: Card):
        return self.rank < other.rank

    def __le__(self, other: Card):
        return self.rank <= other.rank

    def __repr__(self):
        return self.char


class HandType(Enum):
    FIVE_KIND = 7
    FOUR_KIND = 6
    FULL_HOUSE = 5
    THREE_KIND = 4
    TWO_PAIR = 3
    ONE_PAIR = 2
    HIGH_CARD = 1

    def __eq__(self, other: Card):
        return self._value_ == other._value_

    def __lt__(self, other: Card):
        return self._value_ < other._value_

    def __le__(self, other: Card):
        return self._value_ <= other._value_


@dataclass
class Hand:
    cards: list[Card] = field(default_factory=list)
    hand_type: HandType = None
    bid: int = 0
    jokers: bool = False

    def __init__(self, cards: list[Card], jokers: bool = False) -> None:
        self.cards = cards
        self.jokers = jokers
        self.hand_type = self.infer_hand_type()

    def infer_hand_type(self) -> HandType:
        counts = Counter(self.cards)

        first_card, first_count = counts.most_common(1)[0]
        second_card, second_count = None, 0
        third_card, third_count = None, 0

        if len(counts.keys()) > 1:
            second_card, second_count = counts.most_common(2)[1]

        if self.jokers and Card.JOKER in counts:
            joker_count = counts[Card.JOKER]

            if Card.JOKER not in [first_card, second_card]:
                first_count += joker_count

            else:
                # bring third card in
                if len(counts.keys()) > 2:
                    third_card, third_count = counts.most_common(3)[2]

                if first_card == Card.JOKER:
                    # add joker count to second card, and bring third card in
                    second_count += joker_count
                    first_count = third_count
                elif second_card == Card.JOKER:
                    # add joker count to first card, and bring third card in
                    first_count += joker_count
                    second_count = third_count
                # finally, reorder first and second counts if necessary
                if second_count > first_count:
                    first_count, second_count = second_count, first_count

        if first_count == 5:
            return HandType.FIVE_KIND
        elif first_count == 4:
            return HandType.FOUR_KIND
        elif first_count == 3 and second_count == 2:
            return HandType.FULL_HOUSE
        elif first_count == 3:
            return HandType.THREE_KIND
        elif first_count == 2 and second_count == 2:
            return HandType.TWO_PAIR
        elif first_count == 2:
            return HandType.ONE_PAIR
        else:
            return HandType.HIGH_CARD

    def __eq__(self, other: Hand):
        return self.hand_type == other.hand_type and self.cards == other.cards

    def __lt__(self, other: Card):
        if self.hand_type != other.hand_type:
            return self.hand_type < other.hand_type

        for self_card, other_card in zip(self.cards, other.cards):
            if self_card != other_card:
                return self_card < other_card

        return False

    def __le__(self, other: Card):
        if self.hand_type != other.hand_type:
            return self.hand_type <= other.hand_type

        for self_card, other_card in zip(self.cards, other.cards):
            if self_card != other_card:
                return self_card <= other_card

        return True

    def __repr__(self):
        return "".join([str(card) for card in self.cards])


def parse_input(lines: Iterable[str], jokers: bool = False) -> list[Hand]:
    hands = list()

    for line in lines:
        card_str, bid = line.split()

        cards = list()
        for card in card_str:
            if jokers is True and card == "J":
                cards.append(Card.JOKER)
            else:
                cards.append(Card(card))

        hand = Hand(cards, jokers=jokers)
        hand.bid = int(bid)
        hands.append(hand)

    return hands


def part_one(lines: Iterable[str]) -> int:
    hands = parse_input(lines)

    out = 0
    for rank, hand in enumerate(sorted(hands), start=1):
        out += rank * hand.bid

    return out


def part_two(lines: Iterable[str]) -> int:
    hands = parse_input(lines, jokers=True)

    out = 0
    for rank, hand in enumerate(sorted(hands), start=1):
        out += rank * hand.bid

    return out
