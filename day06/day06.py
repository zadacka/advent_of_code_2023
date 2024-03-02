import math


def parse_input(filename):
    def parse_line(line):
        name, *values = line.split()
        int_values = [int(i) for i in values]
        return int_values

    with open(filename) as f:
        times = parse_line(f.readline())
        distances = parse_line(f.readline())
    return times, distances


def find_ways_of_winning(race_duration, current_record):
    ways_of_winning = 0
    for speed in range(race_duration):
        time_to_race_for = race_duration - speed
        if speed * time_to_race_for > current_record:
            ways_of_winning += 1
    return ways_of_winning


def test_find_ways_of_winning():
    assert 4 == find_ways_of_winning(7, 9)
    assert 8 == find_ways_of_winning(15, 40)
    assert 9 == find_ways_of_winning(30, 200)


def test_test_part1():
    times, distances = parse_input('day06_test_input.txt')
    assert times == [7, 15, 30]
    assert distances == [9, 40, 200]
    ways_of_winning = []
    for time, distance in zip(times, distances):
        ways_of_winning.append(find_ways_of_winning(time, distance))

def test_real_part1():
    times, distances = parse_input('day06_real_input.txt')
    ways_of_winning = [find_ways_of_winning(time, distance) for time, distance in zip(times, distances)]
    assert ways_of_winning == [23, 56, 56, 46]
    assert math.prod(ways_of_winning) == 3317888

    # part 2
    time = int(''.join([str(i) for i in times]))
    distance = int(''.join([str(i) for i in distances]))
    assert find_ways_of_winning(time, distance) == 24655068