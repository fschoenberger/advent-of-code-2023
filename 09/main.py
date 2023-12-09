import math
import os
import re
import tqdm
import numpy as np

def get_extrapolated_value_next(sequence) -> int:
    if(all([item == 0 for item in sequence])):
        return 0
    
    next_sequence = np.diff(sequence)
    return sequence[-1] + get_extrapolated_value_next(next_sequence)

def get_extrapolated_value_previous(sequence) -> int:
    if(all([item == 0 for item in sequence])):
        return 0
    
    next_sequence = np.diff(sequence)
    return sequence[0] - get_extrapolated_value_previous(next_sequence)

def main():
    with open(os.path.join(os.path.dirname(__file__), "./input.txt")) as f:
        sequences_list = [
            list(map(lambda x: int(x), line.strip().split(" ")))
            for line in f.readlines()
        ]

        sequences = np.array(sequences_list)

        total = 0
        for index, sequence in enumerate(sequences):
            num = get_extrapolated_value_next(sequence)
            print(f"Sequence {index}: {num}")
            total += num

        print(f"Part 1: {total}")

        total = 0
        for index, sequence in enumerate(sequences):
            num = get_extrapolated_value_previous(sequence)
            print(f"Sequence {index}: {num}")
            total += num

        print(f"Part 2: {total}")


if __name__ == "__main__":
    main()
