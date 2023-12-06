import os
import time
import re
import gc
from typing import Iterable
from itertools import chain, zip_longest
from functools import partial, reduce, lru_cache
from multiprocessing import Pool
from sortedcontainers import SortedDict
import tqdm
import bisect
import cProfile


def parse_map(description: list[str]) -> list[tuple[int, int, int]]:
    ret = []  # SortedDict()
    for line in description:
        (destination_index, source_index, extent) = line.split(" ")
        ret.append((int(source_index), int(destination_index), int(extent)))

    ret.sort(key=lambda x: x[0])

    return ret


# Returns the index and the index one can skip to
def find_next_index(map: list[tuple[int, int, int]], needle: int) -> tuple[int, int]:
    index = bisect.bisect(map, needle, key=lambda x: x[0]) - 1

    if index < 0:
        return needle, needle + 1  # TODO: Make skip value better

    source, destination, extent = map[index]

    if needle < source:
        print(
            f"needle = {needle}, source = {source}, list = {map[index -2 : index +2]}"
        )
        raise Exception("This should never happen")

    # 622612797
    # 226172555
    if source < needle < source + extent:
        return destination + (needle - source), source + 1 #extent - 1

    return needle, needle + 1  # TODO: Make skip value better


def grouper(iterable, n, *, incomplete="fill", fillvalue=None):
    "Collect data into non-overlapping fixed-length chunks or blocks"
    # grouper('ABCDEFG', 3, fillvalue='x') --> ABC DEF Gxx
    # grouper('ABCDEFG', 3, incomplete='strict') --> ABC DEF ValueError
    # grouper('ABCDEFG', 3, incomplete='ignore') --> ABC DEF
    args = [iter(iterable)] * n
    if incomplete == "fill":
        return zip_longest(*args, fillvalue=fillvalue)
    if incomplete == "strict":
        return zip(*args, strict=True)
    if incomplete == "ignore":
        return zip(*args)
    else:
        raise ValueError("Expected fill, strict, or ignore")


def main():
    with open(os.path.join(os.path.dirname(__file__), "./input.txt")) as f:
        content = f.read()

        (
            seeds_string,
            seed_to_soil,
            soil_to_fertilizer,
            fertilizer_to_water,
            water_to_light,
            light_to_temp,
            temp_to_humidity,
            humidity_to_location,
        ) = content.split("\n\n")

        seeds = [int(seed) for seed in re.findall("\d+", seeds_string)]

        seed_to_soil_map = parse_map(seed_to_soil.splitlines()[1:])
        soil_to_fertilizer_map = parse_map(soil_to_fertilizer.splitlines()[1:])
        fertilizer_to_water_map = parse_map(fertilizer_to_water.splitlines()[1:])
        water_to_light_map = parse_map(water_to_light.splitlines()[1:])
        light_to_temp_map = parse_map(light_to_temp.splitlines()[1:])
        temp_to_humidity_map = parse_map(temp_to_humidity.splitlines()[1:])
        humidity_to_location_map = parse_map(humidity_to_location.splitlines()[1:])

        def get_lowest_index_candidates(map, indices_raw):
            ret = []

            indices = sorted(indices_raw)

            cursor = 0
            for index in indices:
                if index < cursor:
                    continue

                candidate, skip_to = find_next_index(map, index)
                ret.append(candidate)
                cursor = skip_to
            return ret

        find_soil_candidates = partial(get_lowest_index_candidates, seed_to_soil_map)
        find_fertilizer_candidates = partial(
            get_lowest_index_candidates, soil_to_fertilizer_map
        )
        find_water_candidates = partial(
            get_lowest_index_candidates, fertilizer_to_water_map
        )
        find_light_candidates = partial(get_lowest_index_candidates, water_to_light_map)
        find_temp_candidates = partial(get_lowest_index_candidates, light_to_temp_map)
        find_humidity_candidates = partial(
            get_lowest_index_candidates, temp_to_humidity_map
        )
        find_location_candidates = partial(
            get_lowest_index_candidates, humidity_to_location_map
        )

        def get_lowest_value_for_seeds(seeds: Iterable) -> int:
            return min(
                reduce(
                    lambda r, f: f(r),
                    (
                        find_soil_candidates,
                        find_fertilizer_candidates,
                        find_water_candidates,
                        find_light_candidates,
                        find_temp_candidates,
                        find_humidity_candidates,
                        find_location_candidates,
                    ),
                    seeds,
                )
            )

        print(f"Part 1: Lowest location is {get_lowest_value_for_seeds(seeds)}")

        print("\n==================\n")

        seeds_part_2 = []
        batch_size = 10_000_00
        for start, extent in zip(seeds[::2], seeds[1::2]):
            num_batches = extent // batch_size
            print(f"[Doing {num_batches} batches]")

            index = 1
            for batch in tqdm.tqdm(
                grouper(range(start, start + extent + 1), batch_size, fillvalue=None),
                total=num_batches,
            ):
                # print(f"\nBatch {index} of {num_batches}:")
                index += 1
                seeds_part_2.append(get_lowest_value_for_seeds(batch))

        print(len(seeds_part_2))

        print(f"Part 2: Lowest location is {min(seeds_part_2)}")


if __name__ == "__main__":
    # cProfile.run("main()")
    main()
