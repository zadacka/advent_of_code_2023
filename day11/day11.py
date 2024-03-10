from itertools import combinations


def parse_day11_input(filename):
    return [list(line.strip()) for line in open(filename).readlines()]


def expand_star_map(star_map):
    def add_rows(rows):
        expanded = []
        for row in rows:
            expanded.append(row)
            if set(row) == set('.'):
                expanded.append(row)
        return expanded

    expanded = add_rows(star_map)
    transposed = [list(i) for i in zip(*expanded)]
    expanded_again = add_rows(transposed)
    transposed_again = [list(i) for i in zip(*expanded_again)]
    return transposed_again


def all_paths(galaxies):
    pairs = combinations(galaxies, 2)
    manhatten_distances = [
        abs(a[0] - b[0]) + abs(a[1] - b[1])
        for a, b in pairs
    ]
    return sum(manhatten_distances)


def get_galaxies(star_map):
    galaxies = []
    for row_idx, row in enumerate(star_map):
        for col_idx, cell in enumerate(row):
            if cell == '#':
                galaxies.append((row_idx, col_idx))
    return galaxies


def get_blank_rows_and_columns(star_map):
    blank_rows = [
        False if '#' in row else True
        for row in star_map
    ]
    transposed = [list(i) for i in zip(*star_map)]
    blank_columns = [
        False if '#' in column else True
        for column in transposed
    ]
    return blank_rows, blank_columns


def adjust_galaxies(galaxies, blank_rows, blank_columns, expansion_factor):
    adjusted_galaxies = []
    for galaxy in galaxies:
        galaxy_row, galaxy_column = galaxy[0], galaxy[1]
        blank_rows_to_expand = sum(blank_rows[:galaxy_row])
        blank_columns_to_expand = sum(blank_columns[:galaxy_column])
        new_row = galaxy_row + blank_rows_to_expand * (expansion_factor - 1)
        new_column = galaxy_column + blank_columns_to_expand * (expansion_factor - 1)
        adjusted_galaxies.append((new_row, new_column))
    return adjusted_galaxies


def test_test_input():
    star_map = parse_day11_input('day11_test_input.txt')
    expanded_star_map = expand_star_map(star_map)
    assert len(expanded_star_map) == 12
    assert len(expanded_star_map[0]) == 13

    galaxies = get_galaxies(expanded_star_map)

    count = all_paths(galaxies)
    assert count == 374

    galaxies = get_galaxies(star_map)
    blank_rows, blank_columns = get_blank_rows_and_columns(star_map)
    adjusted_galaxies = adjust_galaxies(galaxies, blank_rows, blank_columns, expansion_factor=10)
    assert all_paths(adjusted_galaxies) == 1030
    adjusted_galaxies = adjust_galaxies(galaxies, blank_rows, blank_columns, expansion_factor=100)
    assert all_paths(adjusted_galaxies) == 8410


def test_real_input():
    star_map = parse_day11_input('day11_real_input.txt')
    expanded_star_map = expand_star_map(star_map)

    galaxies = get_galaxies(expanded_star_map)

    count = all_paths(galaxies)
    assert count == 702770569197

    # part 2
    blank_rows, blank_columns = get_blank_rows_and_columns(star_map)
    galaxies = get_galaxies(star_map)
    adjusted_galaxies = adjust_galaxies(galaxies, blank_rows, blank_columns, expansion_factor=1000000)
    assert all_paths(adjusted_galaxies) == 0
