import os
import time


def main():
    with open(os.path.join(os.path.dirname(__file__), "./input.txt")) as f:
        cards = [
            (index, *line.split(":")[1].strip().split("|"))
            for index, line in enumerate(f.readlines())
        ]

        total_wins = 0

        cards_queue = [card for card in cards]

        print(cards_queue)

        for index, winning_numbers, actual_numbers in cards_queue:
            winning_numbers_set = set([int(n.strip()) for n in winning_numbers.split()])
            actual_numbers_set = set([int(n.strip()) for n in actual_numbers.split()])

            matching_numbers = len(winning_numbers_set.intersection(actual_numbers_set))

            if matching_numbers > 0:
                print(
                    f"Card {index + 1}: {matching_numbers} number(s) matched (= {2 ** (matching_numbers - 1)} points)"
                )
                total_wins += 2 ** (matching_numbers - 1)
            else:
                print(f"Card {index + 1}: No numbers matched")

        print(f"Part 1: {total_wins} points")

        print("\n\n\n=======================")

        cache = {}

        def get_num_winning_cards(index: int) -> int:
            if index in cache:
                return cache[index]

            winning_numbers, actual_numbers = cards[index][1:]
            winning_numbers_set = set([int(n.strip()) for n in winning_numbers.split()])
            actual_numbers_set = set([int(n.strip()) for n in actual_numbers.split()])

            matching_numbers = len(winning_numbers_set.intersection(actual_numbers_set))

            if matching_numbers == 0:
                cache[index] = 0
                return 0

            ret = matching_numbers
            for i in range(index + 1, index + matching_numbers + 1):
                print(f"Checking card {i}")
                ret += get_num_winning_cards(i)

            cache[index] = ret
            return ret

        start_time_block1 = time.perf_counter()
        sum = len(cards)
        for i in range(len(cards)):
            sum += get_num_winning_cards(i)

        end_time_block1 = time.perf_counter()
        print(f"Part 2 (with memoization): {sum} ({end_time_block1 - start_time_block1} seconds)")

        start_time_block2 = time.perf_counter()
        tally = 0
        for index, winning_numbers, actual_numbers in cards_queue:
            winning_numbers_set = set([int(n.strip()) for n in winning_numbers.split()])
            actual_numbers_set = set([int(n.strip()) for n in actual_numbers.split()])

            matching_numbers = len(winning_numbers_set.intersection(actual_numbers_set))

            tally += 1
            if matching_numbers > 0:
                cards_queue.extend(cards[index + 1 : index + matching_numbers + 1])

            if False and tally % 100000 == 0:
                print(f"Remaining: {len(cards_queue) - tally}")
        end_time_block2 = time.perf_counter()

        print(f"Part 2 (naive implementation): {len(cards_queue)}  ({end_time_block2 - start_time_block2} seconds)")


if __name__ == "__main__":
    main()
