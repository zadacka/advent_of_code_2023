import re


def load_input(file_name):
    with open(file_name) as f:
        return f.readlines()


def parse_line(line: str) -> int:
    filtered = [int(x) for x in line if x.isnumeric()]
    return 10 * filtered[0] + filtered[-1]


def test_parse_line():
    assert 38 == parse_line("pqr3stu8vwx")
    assert 12 == parse_line("1abc2")
    assert 15 == parse_line("a1b2c3d4e5f")
    assert 77 == parse_line("treb7uchet")


words_to_numbers = {
    "one": 1,
    "two": 2,
    "three": 3,
    "four": 4,
    "five": 5,
    "six": 6,
    "seven": 7,
    "eight": 8,
    "nine": 9,
    "1": 1,
    "2": 2,
    "3": 3,
    "4": 4,
    "5": 5,
    "6": 6,
    "7": 7,
    "8": 8,
    "9": 9,
}


def parse_wordy_line(line: str) -> int:
    filtered = []
    for index in range(len(line)):
        for word, number in words_to_numbers.items():
            if line[index:].startswith(word):
                filtered.append(number)
                break
        index += 1
    return filtered[0] * 10 + filtered[-1]


def parse_wordy_line2(line: str) -> int:
    filtered = []
    for index, char in enumerate(line):
        if char.isnumeric():
            filtered.append(int(char))
        else:
            for word in words_to_numbers.keys():
                if line[index:].startswith(word):
                    filtered.append(words_to_numbers[word])
    return filtered


def test_parse_line_with_words():
    assert 29 == parse_wordy_line("two1nine")
    assert 83 == parse_wordy_line("eightwothree")
    assert 13 == parse_wordy_line("abcone2threexyz")
    assert 24 == parse_wordy_line("xtwone3four")
    assert 42 == parse_wordy_line("4nineeightseven2")
    assert 14 == parse_wordy_line("zoneight234")
    assert 76 == parse_wordy_line("7pqrstsixteen")
    assert 31 == parse_wordy_line("'35zrgthreetwonesz")


def test_calculate_calibration():
    assert 142 == calculate_calibration('day01_test_input.txt')


def test_calculate_wordy_calibration():
    assert 281 == calculate_wordy_calibration('day01_more_test_input.txt')


def calculate_calibration(filename: str) -> int:
    total = 0
    with open(filename) as f:
        for line in f.readlines():
            total += parse_line(line)
    return total


def calculate_wordy_calibration(filename: str) -> int:
    total = 0
    with open(filename) as f:
        for line in f.readlines():
            total += parse_wordy_line(line)
    return total


def test_day_01():
    assert calculate_calibration('day01_real_input.txt') == 54632
    assert calculate_wordy_calibration('day01_real_input.txt') == 54019
