def parse_line(line: str) -> tuple:
    """ Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53 """
    card, numbers = line.split(':')
    winning_numbers, drawn_numbers = numbers.split('|')
    return {int(n) for n in winning_numbers.split()}, [int(m) for m in drawn_numbers.split()]


def parse_lines(filename):
    return [parse_line(line) for line in open(filename).readlines()]


def count_winners(parsed_lines):
    result = 0
    for winning_numbers, drawn_numbers in parsed_lines:
        winners = [1 for drawn_number in drawn_numbers if drawn_number in winning_numbers]
        if winners:
            result += 2 ** (sum(winners) - 1)
    return result


def test_test_input():
    parsed_lines = parse_lines('day04_test_input.txt')
    winners = count_winners(parsed_lines)
    assert winners == 13

def test_real_input():
    parsed_lines = parse_lines('day04_real_input.txt')
    winners = count_winners(parsed_lines)
    assert winners == 13
