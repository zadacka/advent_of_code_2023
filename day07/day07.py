import operator
from collections import Counter
from enum import Enum, IntEnum


def parse_input(file_name):
    hands, bids = [], []
    with open(file_name) as f:
        for line in f.readlines():
            hand, bid = line.split()
            hands.append(hand)
            bids.append(int(bid))

    return hands, bids


card_to_value = {'A': 14, 'K': 13, 'Q': 12, 'J': 11, 'T': 10, '9': 9, '8': 8, '7': 7, '6': 6, '5': 5, '4': 4, '3': 3,
                 '2': 2, }
card_to_value2 = {'A': 14, 'K': 13, 'Q': 12, 'T': 10, '9': 9, '8': 8, '7': 7, '6': 6, '5': 5, '4': 4, '3': 3, '2': 2,
                  'J': 1}


class HandValue(IntEnum):
    five_of_a_kind = 7
    four_of_a_kind = 6
    full_house = 5
    three_of_a_kind = 4
    two_pairs = 3
    one_pair = 2
    high_card = 1


def value_hand(hand, jokers=False):
    card_counts = Counter(hand)

    joker_modifier = hand.count('J') if jokers else 0

    value_counts = Counter(card_counts.values())

    if 5 in value_counts:
        # Five of a kind, where all five cards have the same label: AAAAA
        return HandValue.five_of_a_kind
    elif 4 in value_counts:
        # Four of a kind, where four cards have the same label and one card has a different label: AA8AA
        if joker_modifier in (4, 1):
            return HandValue.five_of_a_kind
        return HandValue.four_of_a_kind
    elif 3 in value_counts and 2 in value_counts:
        # Full house, where three cards have the same label, and the remaining two cards share a different label: 23332
        if joker_modifier in (3, 2):
            return HandValue.five_of_a_kind
        if joker_modifier == 1:
            return HandValue.four_of_a_kind
        return HandValue.full_house
    elif 3 in value_counts:
        # Three of a kind, where three cards have the same label, and the remaining two cards are each different from any other card in the hand: TTT98
        if joker_modifier in (3, 1):
            return HandValue.four_of_a_kind
        return HandValue.three_of_a_kind
    elif 2 in value_counts and 2 in value_counts.values():
        # Two pair, where two cards share one label, two other cards share a second label, and the remaining card has a third label: 23432
        if joker_modifier == 2:
            return HandValue.four_of_a_kind
        if joker_modifier == 1:
            return HandValue.full_house
        return HandValue.two_pairs
    elif 2 in value_counts:
        # One pair, where two cards share one label, and the other three cards have a different label from the pair and each other: A23A4
        if joker_modifier == 2:
            return HandValue.three_of_a_kind
        if joker_modifier == 1:
            return HandValue.three_of_a_kind
        return HandValue.one_pair
    else:
        if joker_modifier == 1:
            return HandValue.one_pair
        # High card, where all cards' labels are distinct: 23456
        return HandValue.high_card


def test_part1_test_input():
    hands, bids = parse_input('day07_test_input.txt')
    assert hands == ['32T3K', 'T55J5', 'KK677', 'KTJJT', 'QQQJA']
    assert bids == [765, 684, 28, 220, 483]

    hand_to_bid = {hand: bid for hand, bid in zip(hands, bids)}
    hand_to_value = {}
    for hand in hands:
        # first the hand value, then the card values for a tie-break
        hand_to_value[hand] = [value_hand(hand)] + [card_to_value[card] for card in hand]

    winning_order = sorted(hand_to_value.items(), key=operator.itemgetter(1))
    winning_total = 0
    print()
    for rank, (hand, score) in enumerate(winning_order, start=1):
        bid = hand_to_bid[hand]
        print(rank, hand, hand_to_bid[hand], score)
        winning_total += hand_to_bid[hand] * rank
    # 765 * 1 + 220 * 2 + 28 * 3 + 684 * 4 + 483 * 5
    assert winning_total == 6440

    # part 2
    hand_to_value2 = {}
    for hand in hands:
        # first the hand value, then the card values for a tie-break
        hand_to_value2[hand] = [value_hand(hand, jokers=True)] + [card_to_value2[card] for card in hand]
    winning_order2 = sorted(hand_to_value2.items(), key=operator.itemgetter(1))
    winning_total = 0
    print()
    for rank, (hand, score) in enumerate(winning_order2, start=1):
        bid = hand_to_bid[hand]
        print(rank, hand, hand_to_bid[hand], bid, score)
        winning_total += hand_to_bid[hand] * rank
    # 765 * 1 + 220 * 2 + 28 * 3 + 684 * 4 + 483 * 5
    assert winning_total == 5905


def test_part1_real_input():
    hands, bids = parse_input('day07_real_input.txt')
    hand_to_bid = {hand: bid for hand, bid in zip(hands, bids)}
    hand_to_value = {}
    for hand in hands:
        # first the hand value, then the card values for a tie-break
        hand_to_value[hand] = [value_hand(hand)] + [card_to_value[card] for card in hand]

    winning_order = sorted(hand_to_value.items(), key=operator.itemgetter(1))
    winning_total = 0
    for rank, (hand, score) in enumerate(winning_order, start=1):
        winning_total += hand_to_bid[hand] * rank

    assert winning_total == 253313241

    # part 2
    hand_to_value2 = {}
    for hand in hands:
        # first the hand value, then the card values for a tie-break
        hand_to_value2[hand] = [value_hand(hand, jokers=True)] + [card_to_value2[card] for card in hand]
    winning_order2 = sorted(hand_to_value2.items(), key=operator.itemgetter(1))
    winning_total = 0
    for rank, (hand, score) in enumerate(winning_order2, start=1):
        bid = hand_to_bid[hand]
        winning_total += hand_to_bid[hand] * rank

    assert winning_total == 253362743

def test_value_hand():
    assert HandValue.five_of_a_kind == value_hand('KKKKK')
    assert HandValue.five_of_a_kind == value_hand('KKKKJ', jokers=True)
    assert HandValue.five_of_a_kind == value_hand('JKKKJ', jokers=True)
    assert HandValue.full_house == value_hand('JKKKJ', jokers=False)
    assert HandValue.full_house == value_hand('JKKKJ', jokers=False)