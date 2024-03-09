PIPE_MAP = {
    "|": {'N': 'N', 'S': 'S'},  # | is a vertical pipe connecting north and south.
    "-": {"W": "W", "E": "E"},  # - is a horizontal pipe connecting east and west.
    "L": {"S": "E", "W": "N"},  # L is a 90-degree bend connecting north and east.
    "J": {"S": "W", "E": "N"},  # J is a 90-degree bend connecting north and west.
    "7": {"E": "S", "N": "W"},  # 7 is a 90-degree bend connecting south and west.
    "F": {"N": "E", "W": "S"},  # F is a 90-degree bend connecting south and east.
    # ".": ".",  # . is ground; there is no pipe in this tile.
    "S": {"N": None, "E": None, "S": None, "W": None},
}


def parse_day_10_input(filename):
    maze = {}
    with open(filename) as f:
        for row, line in enumerate(f.readlines()):
            for col, char in enumerate(line):
                maze[(row, col)] = char
    return maze


def get_start(pipe_map):
    return [k for k, v in pipe_map.items() if v == 'S'][0]


class TheAnimal:
    def __init__(self, position, direction):
        self.position = position
        self.direction = direction


def get_start_direction(starting_position, pipe_map):
    row, col = starting_position

    up = pipe_map.get((row - 1, col), None)
    down = pipe_map.get((row + 1, col), None)
    left = pipe_map.get((row, col - 1), None)
    right = pipe_map.get((row, col + 1), None)

    if up in {"|", "7", "F"}:
        return "N"
    elif down in {"|", "L", "J"}:
        return "S"
    elif left in {"-", "L", "F"}:
        return "W"
    elif right in {"-", "7", "J"}:
        return "E"
    else:
        raise RuntimeError(f"Could not work out which direction to go. Neighbours {up}, {down}, {left}, {right}")


def move_one(position, direction, area_map):
    row, column = position
    if direction == "N":
        next_position = (row - 1, column)
    elif direction == "S":
        next_position = (row + 1, column)
    elif direction == "W":
        next_position = (row, column - 1)
    elif direction == "E":
        next_position = (row, column + 1)
    else:
        raise RuntimeError(f"Direction {direction} not handled")

    next_position_type = area_map[next_position]
    next_direction = PIPE_MAP[next_position_type][direction]
    return next_position, next_direction


def test_test_input():
    area_map = parse_day_10_input("day10_test_input.txt")
    starting_position = get_start(area_map)
    assert starting_position == (2, 0)
    starting_direction = get_start_direction(starting_position, area_map)
    assert starting_direction == "S"

    route = get_route(area_map, starting_direction, starting_position)

    assert len(route) - 1 == 16
    assert route[0] == (2, 0)
    midpoint = (len(route) - 1) // 2
    assert midpoint == 8


def test_real_data():
    area_map = parse_day_10_input("day10_real_input.txt")
    starting_position = get_start(area_map)
    starting_direction = get_start_direction(starting_position, area_map)
    route = get_route(area_map, starting_direction, starting_position)
    midpoint = (len(route) - 1) // 2
    assert midpoint == 6613


def test_test_data_part2():
    area_map = parse_day_10_input("day10_test_input2.txt")
    starting_position = get_start(area_map)
    starting_direction = get_start_direction(starting_position, area_map)
    route = get_route(area_map, starting_direction, starting_position)

    enclosed = 0

    rows = max(key[0] for key in area_map)
    columns = max(key[1] for key in area_map)
    for row in range(rows):
        in_loop = False
        for column in range(columns):
            if (row, column) in route and area_map[(row, column)] in "JL|":
                in_loop = not in_loop
            if in_loop and not (row, column) in route:
                enclosed += 1
    assert enclosed == 4


def get_start_type(route):
    first_position = route[1]
    last_position = route[-2]
    connection_row_diff = last_position[0] - first_position[0]
    connection_col_diff = last_position[1] - first_position[1]
    if connection_row_diff == 2 and connection_col_diff == 0:
        return "|"
    elif connection_row_diff == 0 and connection_col_diff == 2:
        return "-"
    elif connection_row_diff == 1 and connection_col_diff == 1:
        return "L"
    elif connection_row_diff == 1 and connection_col_diff == -1:
        return "J"
    elif connection_row_diff == -1 and connection_col_diff == 1:
        return "F"
    elif connection_row_diff == -1 and connection_col_diff == -1:
        return "7"
    else:
        raise RuntimeError(f"Don't know how to handle {route[1]} to {route[0]} to  {route[-2]}")



def test_real_data_part2():
    area_map = parse_day_10_input("day10_real_input.txt")
    starting_position = get_start(area_map)
    starting_direction = get_start_direction(starting_position, area_map)
    route = get_route(area_map, starting_direction, starting_position)

    start_type = get_start_type(route)
    area_map[starting_position] = start_type

    internal_count = 0
    rows = max(key[0] for key in area_map)
    columns = max(key[1] for key in area_map)
    for row in range(rows):
        in_loop = False
        for column in range(columns):
            if (row, column) in route and area_map[(row, column)] in "JL|":
                in_loop = not in_loop
            if in_loop and not (row, column) in route:
                area_map[(row, column)] = "O"
                internal_count += 1

    assert internal_count == 511
    # for row in range(rows):
    #     for column in range(columns):
    #         character = area_map[(row, column)]
    #         if (row, column) in route or character == "O":
    #             print(character, end='')
    #         else:
    #             print(".", end='')
    #     print()



def calculate_distance(first_point, second_point):
    distance = abs(first_point[0] - second_point[0]) + abs(first_point[1] - second_point[1])
    return distance


def get_route(area_map, starting_direction, starting_position):
    position = starting_position
    direction = starting_direction
    # move us off the starting position so the "while true" works
    position, direction = move_one(position, direction, area_map)
    route = [starting_position, position]
    while position != starting_position:
        position, direction = move_one(position, direction, area_map)
        route.append(position)
    return route
