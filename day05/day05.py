from itertools import chain


def unmap(seed, maps):
    result = [seed]
    for map_name in [
        "seed-to-soil",
        "soil-to-fertilizer",
        "fertilizer-to-water",
        "water-to-light",
        "light-to-temperature",
        "temperature-to-humidity",
        "humidity-to-location",
    ]:
        source = result[-1]
        matching_range = [k for k in maps[map_name] if source in k]
        offset = maps[map_name][matching_range[0]] if matching_range else 0
        result.append(source + offset)
    # Seed 79, soil 81, fertilizer 81, water 81, light 74, temperature 78, humidity 78, location 82.
    return result


def parse_file(filename):
    maps = {
        "seed-to-soil": {},
        "soil-to-fertilizer": {},
        "fertilizer-to-water": {},
        "water-to-light": {},
        "light-to-temperature": {},
        "temperature-to-humidity": {},
        "humidity-to-location": {},
    }

    with open(filename) as f:
        map_sections = f.read().split('\n\n')

    assert map_sections[0].startswith('seeds')
    seeds = [int(seed) for seed in map_sections[0].split()[1:]]

    for map_section in map_sections[1:]:
        name, *translations = map_section.split('\n')
        name = name.split()[0]
        assert name in maps
        for translation in translations:
            destination, source, length = (int(i) for i in translation.split())
            offset = destination - source
            maps[name][range(source, source + length)] = offset
    return seeds, maps


def test_test_input():
    seeds, maps = parse_file('day05_test_input.txt')
    locations = [unmap(seed, maps) for seed in seeds]
    assert locations == [
        [79, 81, 81, 81, 74, 78, 78, 82],
        [14, 14, 53, 49, 42, 42, 43, 43],
        [55, 57, 57, 53, 46, 82, 82, 86],
        [13, 13, 52, 41, 34, 34, 35, 35],
    ]
    minimum = min(locations, key=lambda x: x[-1])
    assert minimum[-1] == 35

    # part 2
    ranges = (range(start, start + length) for start, length in zip(seeds[::2], seeds[1::2]))
    part2_locations = [unmap(seed, maps) for seed in (chain(*ranges))]
    assert len(part2_locations) == 27
    part2_minimum = min(part2_locations, key=lambda x: x[-1])
    assert part2_minimum[-1] == 46

    # part 2 efficient
    seed_ranges = [range(start, start + length) for start, length in zip(seeds[::2], seeds[1::2])]
    input_range = [s for s in seed_ranges]
    for map_name, map in maps.items():
        print(map_name)
        input_range = remap(input_range, map)

    assert min([min(r.start, r.stop) for r in input_range]) == 46


def remap(input_range, map):
    new_input = []
    while input_range:
        range_to_remap = input_range.pop()
        source_min = min(range_to_remap.start, range_to_remap.stop)
        source_max = max(range_to_remap.start, range_to_remap.stop) - 1

        for map_range, offset in map.items():
            map_min = min(map_range.start, map_range.stop)
            map_max = max(map_range.start, map_range.stop) - 1
            if source_min in map_range and source_max in map_range:
                new_input.append(range(source_min + offset, source_max + offset + 1))
                break
            elif source_min in map_range:
                new_input.append(range(source_min + offset, map_max + offset + 1))
                input_range.append(range(map_max + 1, source_max + 1))
                break
            elif source_max in map_range:
                new_input.append(range(map_min + offset, source_max + offset + 1))
                input_range.append(range(source_min, map_min))
                break
        else:
            new_input.append(range(source_min, source_max + 1))

    return new_input


def test_real_input():
    seeds, maps = parse_file('day05_real_input.txt')
    locations = [unmap(seed, maps) for seed in seeds]
    minimum = min(locations, key=lambda x: x[-1])
    assert minimum[-1] == 265018614

    # part 2
    seed_ranges = [range(start, start + length) for start, length in zip(seeds[::2], seeds[1::2])]

    input_range = [s for s in seed_ranges]
    for map_name, map in maps.items():
        input_range = remap(input_range, map)

    assert min([min(r.start, r.stop) for r in input_range]) == 63179500


def test_remap():
    assert remap([range(0, 3)], {range(0, 3): 1}) == [range(1, 4)]
    assert remap([range(0, 3)], {range(0, 3): 1, range(3, 6): 2}) == [range(1, 4)]
    assert remap([range(0, 6)], {range(0, 3): 1, range(3, 6): 2}) == [range(1, 4), range(5, 8)]
