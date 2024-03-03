import operator
from collections import Counter


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


def value_hand(hand):
    card_counts = Counter(hand)
    value_counts = Counter(card_counts.values())
    if 5 in value_counts:
        # Five of a kind, where all five cards have the same label: AAAAA
        return 7
    elif 4 in value_counts:
        # Four of a kind, where four cards have the same label and one card has a different label: AA8AA
        return 6
    elif 3 in value_counts and 2 in value_counts:
        # Full house, where three cards have the same label, and the remaining two cards share a different label: 23332
        return 5
    elif 3 in value_counts:
        # Three of a kind, where three cards have the same label, and the remaining two cards are each different from any other card in the hand: TTT98
        return 4
    elif 2 in value_counts and 2 in value_counts.values():
        # Two pair, where two cards share one label, two other cards share a second label, and the remaining card has a third label: 23432
        return 3
    elif 2 in value_counts:
        # One pair, where two cards share one label, and the other three cards have a different label from the pair and each other: A23A4
        return 2
    else:
        # High card, where all cards' labels are distinct: 23456
        return 1


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

    assert winning_total == 6440
