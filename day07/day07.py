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

    number_of_jokers = card_counts['J']
    if jokers and 0 < number_of_jokers < 5:
        del card_counts['J']
        card_counts[card_counts.most_common(1)[0][0]] += number_of_jokers

    value_counts = [count for _, count in card_counts.most_common()]

    if value_counts == [5]:
        # Five of a kind, where all five cards have the same label: AAAAA
        return HandValue.five_of_a_kind
    elif value_counts == [4, 1]:
        # Four of a kind, where four cards have the same label and one card has a different label: AA8AA
        return HandValue.four_of_a_kind
    elif value_counts == [3, 2]:
        # Full house, where three cards have the same label, and the remaining two cards share a different label: 23332
        return HandValue.full_house
    elif value_counts == [3, 1, 1]:
        # Three of a kind, where three cards have the same label, and the remaining two cards are each different from any other card in the hand: TTT98
        return HandValue.three_of_a_kind
    elif value_counts == [2, 2, 1]:
        # Two pair, where two cards share one label, two other cards share a second label, and the remaining card has a third label: 23432
        return HandValue.two_pairs
    elif value_counts == [2, 1, 1, 1]:
        # One pair, where two cards share one label, and the other three cards have a different label from the pair and each other: A23A4
        return HandValue.one_pair
    else:
        # High card, where all cards' labels are distinct: 23456
        return HandValue.high_card


def value_hands(hands, jokers=False):
    """For each hand, return a list:
       [ hand value ] + [value for each of the five cards]
       The list can then be compared to sort, including doing the tie-break """

    value_map = card_to_value2 if jokers else card_to_value

    hand_to_value = {}
    for hand in hands:
        hand_to_value[hand] = [value_hand(hand, jokers=jokers)] + [value_map[card] for card in hand]
    return hand_to_value


def calculate_winning_total(hand_to_bid, hand_to_value):
    winning_order = sorted(hand_to_value.items(), key=operator.itemgetter(1))
    winning_total = 0
    print()
    for rank, (hand, score) in enumerate(winning_order, start=1):
        winning_total += hand_to_bid[hand] * rank
    return winning_total

def test_part1_test_input():
    hands, bids = parse_input('day07_test_input.txt')
    assert hands == ['32T3K', 'T55J5', 'KK677', 'KTJJT', 'QQQJA']
    assert bids == [765, 684, 28, 220, 483]

    hand_to_bid = {hand: bid for hand, bid in zip(hands, bids)}
    hand_to_value = value_hands(hands)
    winning_total = calculate_winning_total(hand_to_bid, hand_to_value)
    assert winning_total == 6440

    # part 2
    hand_to_value = value_hands(hands, jokers=True)
    winning_total = calculate_winning_total(hand_to_bid, hand_to_value)
    assert winning_total == 5905


def test_part1_real_input():
    hands, bids = parse_input('day07_real_input.txt')
    hand_to_bid = {hand: bid for hand, bid in zip(hands, bids)}
    hand_to_value = value_hands(hands)
    winning_total = calculate_winning_total(hand_to_bid, hand_to_value)
    assert winning_total == 253313241

    # part 2
    hand_to_value = value_hands(hands, jokers=True)
    winning_total = calculate_winning_total(hand_to_bid, hand_to_value)
    assert winning_total == 253362743


def test_value_hand():
    assert HandValue.five_of_a_kind == value_hand('KKKKK')
    assert HandValue.five_of_a_kind == value_hand('KKKKJ', jokers=True)
    assert HandValue.five_of_a_kind == value_hand('JKKKJ', jokers=True)
    assert HandValue.full_house == value_hand('JKKKJ', jokers=False)
    assert HandValue.full_house == value_hand('JKKKJ', jokers=False)
