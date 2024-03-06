def parse_day9_input(filename):
    return [
        [int(i) for i in line.split()]
        for line in open(filename).readlines()
    ]


def get_next(input, go_forwards=True):
    # 1   3   6  10  15  21
    #   2   3   4   5   6
    #     1   1   1   1
    #       0   0   0
    history = [
        input,
    ]
    while any([x != 0 for x in history[-1]]):
        row_above = history[-1]
        diffs = [j - i for i, j in zip(row_above, row_above[1:])]
        history.append(diffs)

    prediction = 0
    if go_forwards:
        for history_row in history[::-1]:
            prediction +=  history_row[-1]
    else:
        for history_row in history[::-1]:
            prediction = (history_row[0] - prediction)

    return prediction



def test_test_input():
    input = parse_day9_input('day09_test_input.txt')
    assert input == [[0, 3, 6, 9, 12, 15], [1, 3, 6, 10, 15, 21], [10, 13, 16, 21, 30, 45]]
    assert get_next(input[0]) == 18
    assert get_next(input[1]) == 28
    assert get_next(input[2]) == 68
    assert get_next(input[0], go_forwards=False) == -3
    assert get_next(input[1], go_forwards=False) == 0
    assert get_next(input[2], go_forwards=False) == 5


def test_real_input():
    input = parse_day9_input('day09_real_input.txt')
    assert sum([get_next(i) for i in input]) == 1974913025
    assert sum([get_next(i, go_forwards=False) for i in input]) == 884