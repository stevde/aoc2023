from collections import Counter
import logging
import pytest
from aoc2023 import read_lines
from aoc2023.day07 import Card, Hand, HandType, parse_input, part_one, part_two

logger = logging.getLogger()


@pytest.fixture
def sample_data():
    return [
        "32T3K 765",
        "T55J5 684",
        "KK677 28",
        "KTJJT 220",
        "QQQJA 483",
    ]


def test_card():
    assert Card.ACE.rank == 14
    assert Card.ACE > Card.QUEEN
    assert Card.ACE == Card.ACE

    assert Card("A") == Card.ACE


def test_hand_type():
    assert HandType.FIVE_KIND > HandType.FOUR_KIND


def test_hand():
    fives = Hand(cards=[Card.ACE] * 5)
    fours = Hand(cards=[Card.ACE] * 4 + [Card.QUEEN])

    assert fives.hand_type == HandType.FIVE_KIND
    assert fours.hand_type == HandType.FOUR_KIND

    assert fives > fours
    assert fives == fives
    assert fives <= fives


def test_parse_input(sample_data):
    hands = parse_input(sample_data)
    assert len(hands) == 5
    assert [hand.bid for hand in hands] == [765, 684, 28, 220, 483]


def test_sorting(sample_data):
    hands = parse_input(sample_data)

    hands = sorted(hands, reverse=True)

    # QQQJA
    assert hands[0] == Hand(
        cards=[Card.QUEEN, Card.QUEEN, Card.QUEEN, Card.JACK, Card.ACE]
    )
    assert hands[0].hand_type == HandType.THREE_KIND
    # 32T3K
    assert hands[-1] == Hand(cards=[Card.X3, Card.X2, Card.TEN, Card.X3, Card.KING])
    assert hands[-1].hand_type == HandType.ONE_PAIR


@pytest.fixture
def test_data():
    return read_lines("data/day07.txt")


def test_part_one_sample(sample_data):
    assert part_one(sample_data) == 6440


def test_part_one(test_data):
    assert part_one(test_data) == 251121738


def test_jokers(sample_data):
    hands = parse_input(sample_data, jokers=True)

    hands = sorted(hands, reverse=True)

    # QQQJA
    assert hands[0] == Hand(
        cards=[Card.QUEEN, Card.QUEEN, Card.QUEEN, Card.JOKER, Card.ACE]
    )


def test_part_two_sample(sample_data):
    assert part_two(sample_data) == 5905


def test_part_two(test_data):
    assert part_two(test_data) == 251421071
