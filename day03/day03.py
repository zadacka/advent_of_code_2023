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


def test_part1_test_input():
    schematic = get_schematic('day03_test_input.txt')
    symbol_map = get_symbol_map(schematic)
    assert symbol_map == {(1, 3): '*', (3, 6): '#', (4, 3): '*', (5, 5): '+', (8, 3): '$', (8, 5): '*'}

    number_map = get_number_map(schematic)
    assert number_map == {(0, 0): 467, (0, 5): 114, (2, 2): 35, (2, 6): 633, (4, 0): 617, (5, 7): 58, (6, 2): 592,
                          (7, 6): 755, (9, 1): 664, (9, 5): 598}

    parts = get_parts(number_map, symbol_map)
    assert sum([value for value in parts.values()]) == 4361


def test_part1_real_input():
    schematic = get_schematic('day03_real_input.txt')
    symbol_map = get_symbol_map(schematic)
    number_map = get_number_map(schematic)
    parts = get_parts(number_map, symbol_map)
    assert sum([value for value in parts.values()]) == 543867



if __name__ == '__main__':
    schematic = get_schematic('day03_real_input.txt')
    symbol_map = get_symbol_map(schematic)
    number_map = get_number_map(schematic)
    parts = get_parts(number_map, symbol_map)
    # assert sum(parts.values()) == 4361

    updated_schematic = get_schematic('day03_real_input.txt')
    # for number_loc, number in number_map.items():
    #     for surrounding_loc in get_surrounding_locations(number_loc, number):
    #         row, col = surrounding_loc
    #         if 0 <= row < len(schematic) and 0 <= col < len(schematic[0]) and surrounding_loc not in symbol_map:
    #             updated_schematic[row][col] = '#'

    from colorama import init as colorama_init
    from colorama import Fore
    from colorama import Style
    colorama_init()
    for row, line in enumerate(updated_schematic):
        this_row = ""
        for col, character in enumerate(line):
            if (row, col) in number_map:
                if (row, col) in parts:
                    this_row += f"{Fore.GREEN}{character}{Style.RESET_ALL}"
                else:
                    this_row += f"{Fore.YELLOW}{character}{Style.RESET_ALL}"
            elif (row, col) in symbol_map:
                this_row += f"{Fore.RED}{character}{Style.RESET_ALL}"
            else:
                this_row += character
        print(''.join(this_row))
