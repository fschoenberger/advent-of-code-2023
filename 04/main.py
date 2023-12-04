import os
import re


def main():
    with open(os.path.join(os.path.dirname(__file__), "./input.txt")) as f:
        cards = [(index, *line.split(":")[1].strip().split("|")) for index, line in enumerate(f.readlines())]

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

        tally = 0

        for index, winning_numbers, actual_numbers in cards_queue:
            winning_numbers_set = set([int(n.strip()) for n in winning_numbers.split()])
            actual_numbers_set = set([int(n.strip()) for n in actual_numbers.split()])

            matching_numbers = len(winning_numbers_set.intersection(actual_numbers_set))

            tally += 1
            if matching_numbers > 0:
                # if matching_numbers == 1:
                #     print(f"Card {index + 1}: Adding {matching_numbers} card to the queue (card {index + 2}). Remaining: {len(cards_queue)}")
                # else:
                #     print(f"Card {index + 1}: Adding {matching_numbers} cards to the queue (card {index + 2} to {index + matching_numbers + 1}). Remaining: {len(cards_queue)}")

                cards_queue.extend(cards[index + 1: index + matching_numbers + 1])

            if tally % 100000 == 0:
                print(f"Remaining: {len(cards_queue) - tally}")

        print(f"Part 2: {len(cards_queue)}")


if __name__ == "__main__":
    main()
