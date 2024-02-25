def get_schematic(filename):
    schematic = []
    with open(filename) as f:
        for line in f.readlines():
            schematic.append([character for character in line.strip()])
    return schematic


def get_symbol_map(schematic: list) -> dict:
    symbol_map = dict()
    for row, line in enumerate(schematic):
        for column, character in enumerate(line):
            if character.isnumeric() or character == '.':
                pass  # a number or a placeholder
            else:
                symbol_map[(row, column)] = character
    return symbol_map


def get_number_map(schematic: list) -> dict:
    numbers = dict()

    for row, line in enumerate(schematic):
        number_starting_position = None
        current_number = ""
        for column, character in enumerate(line):
            if character.isnumeric():
                if number_starting_position is None:
                    number_starting_position = (row, column)
                current_number += character

            if not character.isnumeric() or column == len(line)-1:
                if current_number:
                    numbers[number_starting_position] = int(current_number)
                    number_starting_position = None
                    current_number = ""
    return numbers


def get_surrounding_locations(loc, number):
    start_row, start_column = loc
    number_length = len(str(number))
    locations_above = [(start_row -1, col) for col in range(start_column -1, start_column + number_length + 1)]
    locations_around = [(start_row, start_column -1), (start_row, start_column + number_length)]
    locations_below = [(start_row +1, col) for col in range(start_column -1, start_column + number_length + 1)]
    return locations_above + locations_around + locations_below

def get_parts(number_map, symbol_map):
    parts = dict()
    for number_loc, number in number_map.items():
        surrounding_locations = get_surrounding_locations(number_loc, number)
        if any([loc in symbol_map for loc in surrounding_locations]):
            parts[number_loc] = number
    return parts


def get_gears(number_map, symbol_map):
    asterisk_map = {loc: symbol for loc, symbol in symbol_map.items() if symbol == "*"}
    gear_count_map = {loc: [] for loc in asterisk_map.keys()}

    for number_loc, number in number_map.items():
        for surrounding_loc in get_surrounding_locations(number_loc, number):
            if surrounding_loc in gear_count_map:
                gear_count_map[surrounding_loc].append(number)
    return [part_numbers[0] * part_numbers[1] for gear_loc, part_numbers in gear_count_map.items() if len(part_numbers) == 2]


def test_part1_test_input():
    schematic = get_schematic('day03_test_input.txt')
    symbol_map = get_symbol_map(schematic)
    assert symbol_map == {(1, 3): '*', (3, 6): '#', (4, 3): '*', (5, 5): '+', (8, 3): '$', (8, 5): '*'}

    number_map = get_number_map(schematic)
    assert number_map == {(0, 0): 467, (0, 5): 114, (2, 2): 35, (2, 6): 633, (4, 0): 617, (5, 7): 58, (6, 2): 592,
                          (7, 6): 755, (9, 1): 664, (9, 5): 598}

    parts = get_parts(number_map, symbol_map)
    assert sum([value for value in parts.values()]) == 4361

    gears = get_gears(number_map, symbol_map)
    assert gears == [16345, 451490]
    assert sum(gears) == 467835

def test_part1_real_input():
    schematic = get_schematic('day03_real_input.txt')
    symbol_map = get_symbol_map(schematic)
    number_map = get_number_map(schematic)
    parts = get_parts(number_map, symbol_map)
    assert sum([value for value in parts.values()]) == 543867

    gears = get_gears(number_map, symbol_map)
    assert sum(gears) == 79613331


