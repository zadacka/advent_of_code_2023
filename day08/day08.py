import re


def parse_input(file_name):
    nodes = {}
    with open(file_name) as f:
        instructions = f.readline().strip()
        _ = f.readline()
        for line in f.readlines():
            # SMX = (KCF, KJR)
            match = re.match(r'(\w+) = \((\w+), (\w+)\)', line)
            nodes[match[1]] = (match[2], match[3])
    return instructions, nodes


def walk_the_ghostly_nodes(instructions, network):
    nodes = [node for node in network.keys() if node.endswith('A')]
    instruction_index = 0
    while not all([node.endswith('Z') for node in nodes]):

        for node_index, current_node in enumerate(nodes):
            left, right = network[current_node]
            instruction = instructions[instruction_index % len(instructions)]
            nodes[node_index] = left if instruction == 'L' else right

        instruction_index += 1
    return instruction_index

def test_test_input():
    instructions, network = parse_input('day08_test_input.txt')
    assert instructions == 'LLR'
    assert len(network) == 3
    assert walk_the_nodes(instructions, network) == 6
    assert walk_the_ghostly_nodes(instructions, network) == 6


def test_real_input():
    instructions, network = parse_input('day08_real_input.txt')
    assert walk_the_nodes(instructions, network) == 19199
    # TODO: find out if there is a nice way to repeatedly / infinitely cycle through a list
    assert walk_the_ghostly_nodes(instructions, network) == 0


def walk_the_nodes(instructions, network):
    current_node = "AAA"
    instruction_index = 0
    while current_node != 'ZZZ':
        left, right = network[current_node]
        instruction = instructions[instruction_index % len(instructions)]
        current_node = left if instruction == 'L' else right
        instruction_index += 1
    return instruction_index
