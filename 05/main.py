import os
import re
import bisect
from functools import reduce

def parse_map(description: list[str]) -> list[tuple[int, int, int]]:
    ret = []
    for line in description:
        (destination_index, source_index, extent) = line.split(" ")
        ret.append((int(source_index), int(extent), int(destination_index)))

    ret.sort(key=lambda x: x[0])

    return ret


def make_intervals_explicit(
    mapping: list[tuple[int, int, int]]
) -> list[tuple[int, int]]:
    ret = []

    for i, (start, length, destination) in enumerate(mapping):
        ret.append((start, destination))

        # If the next interval is not directly adjacent, we have to insert a new one
        # Do this for the last interval in any case
        if (i != len(mapping) - 1 and mapping[i + 1][0] != start + length) or (
            i == len(mapping) - 1
        ):
            ret.append((start + length, start + length))

    # Add a starting interval if mapping didn't start with 0
    if ret[0][0] != 0:
        ret.insert(0, (0, 0))

    return merge_intervals(ret)


def merge_intervals(l: list[tuple[int, int]]) -> list[tuple[int, int]]:
    ret = l

    i = 1
    # Merge intervals if possible
    while i < len(ret) - 2:
        start, start_value = ret[i]
        end, end_value = ret[i + 1]

        if start_value + (end - start) == end_value:
            del ret[i + 1]
        i += 1
    return ret


def get_intersected_intervals(
    start: int, end: int | None, mapping: list[tuple[int, int]]
) -> list[tuple[int, int]]:
    ret = [
        value
        for value in mapping
        if start <= value[0] and (end is None or end >= value[0])
    ]

    if len(ret) == 0 or ret[0][0] > start:
        # No fucking idea why
        start_index = bisect.bisect_left(mapping, (start,)) - 1
        assert start_index >= 0

        x, f_x = mapping[start_index]

        ret.insert(0, (start, f_x + (start - x)))

    assert len(ret) > 0

    # print(ret)
    return ret


def compose(
    f: list[tuple[int, int]], g: list[tuple[int, int]]
) -> list[tuple[int, int]]:
    ret = []

    # print(f"f: {f}")
    # print(f"g: {g}")
    for (x_start, f_start), (x_end, _) in zip(f, f[1:]):
        length = x_end - x_start

        ret.extend(
            [
                (start - (f_start - x_start), projection)
                for start, projection in get_intersected_intervals(
                    f_start, f_start + length, g
                )
            ]
        )

    f_start = f[-1][1]
    ret.extend(
        [
            (start, projection)
            for start, projection in get_intersected_intervals(f_start, None, g)
        ]
    )

    # print(f"Ret: {ret}")
    return ret


def lookup(start: int, end: int, f):
    values = [mapping for _, mapping in get_intersected_intervals(start, end, f)]

    return min(values)


def main():
    with open(os.path.join(os.path.dirname(__file__), "./input.txt")) as f:
        content = f.read()

        (
            seeds_string,
            _seed_to_soil,
            _soil_to_fertilizer,
            _fertilizer_to_water,
            _water_to_light,
            _light_to_temp,
            _temp_to_humidity,
            _humidity_to_location,
        ) = content.split("\n\n")

        seeds = [int(seed) for seed in re.findall("\d+", seeds_string)]

        seed_to_soil_map = make_intervals_explicit(
            parse_map(_seed_to_soil.splitlines()[1:])
        )
        soil_to_fertilizer_map = make_intervals_explicit(
            parse_map(_soil_to_fertilizer.splitlines()[1:])
        )
        fertilizer_to_water_map = make_intervals_explicit(
            parse_map(_fertilizer_to_water.splitlines()[1:])
        )
        water_to_light_map = make_intervals_explicit(
            parse_map(_water_to_light.splitlines()[1:])
        )
        light_to_temp_map = make_intervals_explicit(
            parse_map(_light_to_temp.splitlines()[1:])
        )
        temp_to_humidity_map = make_intervals_explicit(
            parse_map(_temp_to_humidity.splitlines()[1:])
        )
        humidity_to_location_map = make_intervals_explicit(
            parse_map(_humidity_to_location.splitlines()[1:])
        )

        maps = [
            seed_to_soil_map,
            soil_to_fertilizer_map,
            fertilizer_to_water_map,
            water_to_light_map,
            light_to_temp_map,
            temp_to_humidity_map,
            humidity_to_location_map,
        ]

        total_map = reduce(compose, maps)

        values = [lookup(seed, seed, total_map) for seed in seeds]
        print(f"Part 1: {min(values)}")

        values_part2 = [
            lookup(start, start + length, total_map)
            for start, length in zip(seeds[::2], seeds[1::2])
        ]
        print(f"Part 1: {min(values_part2)}")


if __name__ == "__main__":
    # cProfile.run("main()")
    main()
