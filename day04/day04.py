def parse_line(line: str) -> tuple:
    """ Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53 """
    card, numbers = line.split(':')
    winning_numbers, drawn_numbers = numbers.split('|')
    return {int(n) for n in winning_numbers.split()}, [int(m) for m in drawn_numbers.split()]


def parse_lines(filename):
    return [parse_line(line) for line in open(filename).readlines()]


def count_winners(parsed_lines):
    matches = []
    for winning_numbers, drawn_numbers in parsed_lines:
        matches.append(sum([1 for drawn_number in drawn_numbers if drawn_number in winning_numbers]))
    return matches


def part1_score_calculator(matches):
    return sum([2 ** (m - 1) for m in matches if m != 0])


def part2_score_calculator(matches):
    spares = [0] * len(matches)
    for index, match in enumerate(matches):
        for spare_index in range(match):
            index_to_update = index + spare_index + 1
            if index_to_update <= len(matches):
                spares[index + spare_index + 1] += 1 * (spares[index] + 1)
    return sum(spares) + len(matches)


def test_test_input():
    parsed_lines = parse_lines('day04_test_input.txt')
    matches = count_winners(parsed_lines)
    assert part1_score_calculator(matches) == 13
    assert part2_score_calculator(matches) == 30


def test_real_input():
    parsed_lines = parse_lines('day04_real_input.txt')
    matches = count_winners(parsed_lines)
    assert part1_score_calculator(matches) == 21105
    assert part2_score_calculator(matches) == 0
