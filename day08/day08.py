import math
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


def walk_the_ghostly_nodes_another_attempt(instructions, network):
    nodes = [(node, node) for node in network.keys() if node.endswith('A')]
    seen_it_before = {
        # (node, instruction_index): start_node
    }
    instruction_index = 0
    while not all([current_node.endswith('Z') for start_node, current_node in nodes]):
        for node_index, (start_node, current_node) in enumerate(nodes):
            position_in_instructions = instruction_index % len(instructions)
            if (current_node, position_in_instructions) in seen_it_before and seen_it_before[(current_node, position_in_instructions)] != start_node:
                print(f"{start_node} has become a duplicate - remove it")
                nodes[node_index] = None
            else:
                seen_it_before[(current_node, position_in_instructions)] = start_node
                left, right = network[current_node]
                instruction = instructions[position_in_instructions]
                nodes[node_index] = (start_node, left) if instruction == 'L' else (start_node, right)

        nodes = [x for x in nodes if x is not None]
        instruction_index += 1
    return instruction_index


# def walk_the_ghostly_nodes(instructions, network):
#     nodes = [node for node in network.keys() if node.endswith('A')]
#     instruction_index = 0
#     while not all([node.endswith('Z') for node in nodes]):
#         instruction = instructions[instruction_index % len(instructions)]
#         for node_index, current_node in enumerate(nodes):
#             left, right = network[current_node]
#             nodes[node_index] = left if instruction == 'L' else right
#         instruction_index += 1
#     return instruction_index

def walk_the_ghostly_nodes(instructions, network):
    """
    AAAAAAAAAAGH!!!
    I assumed that:
    1) the point of entering the cycles could be random
    2) the cycles might not be neat (given the instructions and network you could get a supercycle e.g. 7-9-7-9...
    ** but ** the instructions and input are **MASSIVELY** special so it all 'just works with math.lcm
    So: was really struggling to find a 'general' solution and had to look this one up...

    What I should have done is fizzbuzzed this and the periodic patterns would jump out!

    https://www.reddit.com/r/adventofcode/comments/18dhqti/2023_day_8_part_2_eli5_how_the_much_discussed/

    """
    nodes = [node for node in network.keys() if node.endswith('A')]
    count = []
    for node in nodes:
        current_node = node
        instruction_index = 0
        while not current_node.endswith('Z'):
            instruction = instructions[instruction_index % len(instructions)]
            left, right = network[current_node]
            current_node = left if instruction == 'L' else right
            instruction_index += 1
        count.append(instruction_index)
    return math.lcm(*count)


def test_test_input():
    instructions, network = parse_input('day08_test_input.txt')
    assert instructions == 'LLR'
    assert len(network) == 3
    assert walk_the_nodes(instructions, network) == 6
    # assert walk_the_ghostly_nodes(instructions, network) == 6


def test_test_input_part2():
    instructions, network = parse_input('day08_test_input_part_2.txt')
    assert instructions == 'LR'
    assert len(network) == 8
    # assert walk_the_ghostly_nodes__brute_force_edition(instructions, network) == 6
    assert walk_the_ghostly_nodes(instructions, network) == 6


def test_real_input():
    instructions, network = parse_input('day08_real_input.txt')
    assert walk_the_nodes(instructions, network) == 19199
    assert walk_the_ghostly_nodes(instructions, network) == 13663968099527


def walk_the_nodes(instructions, network, current_node="AAA"):
    instruction_index = 0
    while current_node != 'ZZZ':
        left, right = network[current_node]
        # TODO: find out if there is a nice way to repeatedly / infinitely cycle through a list
        instruction = instructions[instruction_index % len(instructions)]
        current_node = left if instruction == 'L' else right
        instruction_index += 1
    return instruction_index

def test_play_around():
    instructions, network = parse_input('day08_real_input.txt')
    nodes = [node for node in network.keys() if node.endswith('A')]
    loops = [""] * len(nodes)

    # so I'm curious ... all of the experienced AoC'ers online "spotted" the lead-in and cycles for ALL of the nodes
    # being identical (REALLY 'special' puzzle input right there...) and seemed to say that inspecting the sample data
    # would give it away ... so here's a little investigation into how I'd try to review the input data and initially
    # try to look for patterns (spoiler: not obvious). The repetition is so slow for the 'real' example that the special
    # nature of the instruction set did NOT jump out to me. Clearly I'm a rookie ... I hope that this stuff becomes more
    # obvious or predictable with practice...
    instruction_index = 0
    for i in range(20000):
        instruction = instructions[instruction_index % len(instructions)]
        for node_index, current_node in enumerate(nodes):
            left, right = network[current_node]
            nodes[node_index] = left if instruction == 'L' else right
            loops[node_index] += 'Z' if nodes[node_index].endswith('Z') else '.'
        instruction_index += 1
    assert loops == []