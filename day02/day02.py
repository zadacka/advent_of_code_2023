from collections import defaultdict


def extract_games(filename: str) -> defaultdict:
    games = defaultdict(list)
    # Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green
    with open(filename) as f:
        for line in f.readlines():
            game, records = line.split(':')
            for draw in records.split(';'):
                colour_count = {'red': 0, 'green': 0, 'blue': 0}
                for count_colour in draw.split(','):
                    count, colour = count_colour.split()
                    colour_count[colour] = int(count)
                games[game].append(colour_count)
    return games


def get_possible_games(games, bag_state):
    invalid_games = set()
    for game, draws in games.items():
        for draw in draws:
            for colour in ['red', 'green', 'blue']:
                if draw[colour] > bag_state[colour]:
                    invalid_games.add(game)
    return [game for game in games.keys() if game not in invalid_games]


def get_sum_of_games(games):
    total = 0
    for game in games:
        _, number = game.split()
        total += int(number)
    return total


def get_fewest_cubes(games):
    fewest_cubes = {}
    for game, draws in games.items():
        fewest_cubes[game] = {
            'red': max([draw['red'] for draw in draws]),
            'green': max([draw['green'] for draw in draws]),
            'blue': max([draw['blue'] for draw in draws])
        }
    return fewest_cubes


def get_powerset(fewest_cubes):
    result = [draw['red'] * draw['green'] * draw['blue'] for draw in fewest_cubes.values()]
    return sum(result)


def test_test_input():
    games = extract_games('day02_test_input.txt')
    bag_state = {'red': 12, 'green': 13, 'blue': 14}
    possible_games = get_possible_games(games, bag_state)
    game_sum = get_sum_of_games(possible_games)
    assert game_sum == 8

    fewest_cubes = get_fewest_cubes(games)
    assert fewest_cubes == {
        "Game 1": {'red': 4, 'green': 2, 'blue': 6},
        "Game 2": {'red': 1, 'green': 3, 'blue': 4},
        "Game 3": {'red': 20, 'green': 13, 'blue': 6},
        "Game 4": {'red': 14, 'green': 3, 'blue': 15},
        "Game 5": {'red': 6, 'green': 3, 'blue': 2},
    }
    powerset = get_powerset(fewest_cubes)
    assert powerset == 2286


def test_real_input():
    games = extract_games('day02_real_input.txt')
    bag_state = {'red': 12, 'green': 13, 'blue': 14}
    possible_games = get_possible_games(games, bag_state)
    game_sum = get_sum_of_games(possible_games)
    assert game_sum == 2449
    fewest_cubes = get_fewest_cubes(games)
    powerset = get_powerset(fewest_cubes)
    assert powerset == 63981
