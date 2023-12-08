from collections import Counter
import os
import re
import enum


class HAND_TYPE(enum.IntEnum):
    FIVE_OF_A_KIND = 0
    FOUR_OF_A_KIND = 1
    FULL_HOUSE = 2
    THREE_OF_A_KIND = 3
    TWO_PAIRS = 4
    ONE_PAIR = 5
    HIGH_CARD = 6


def get_card_type(card: str) -> int:
    return {
        "A": 0,
        "K": 1,
        "Q": 2,
        "J": 3,
        "T": 4,
        "9": 5,
        "8": 6,
        "7": 7,
        "8": 9,
        "7": 10,
        "6": 11,
        "5": 12,
        "4": 13,
        "3": 14,
        "2": 15,
    }[card]


def get_card_type_part2(card: str) -> int:
    return {
        "A": 0,
        "K": 1,
        "Q": 2,
        "J": 20,  # Doesn't matter as it is just used for sorting purposes
        "T": 4,
        "9": 5,
        "8": 6,
        "7": 7,
        "8": 9,
        "7": 10,
        "6": 11,
        "5": 12,
        "4": 13,
        "3": 14,
        "2": 15,
    }[card]


def get_hand_type(hand: str):
    cards_dict = Counter(hand)
    cards = list(cards_dict.values())

    if len(cards) == 1:
        return HAND_TYPE.FIVE_OF_A_KIND

    if len(cards) == 2:
        if cards[0] == 4 or cards[1] == 4:
            return HAND_TYPE.FOUR_OF_A_KIND
        return HAND_TYPE.FULL_HOUSE

    if len(cards) == 3:
        # print(cards)
        if cards[0] == 3 or cards[1] == 3 or cards[2] == 3:
            return HAND_TYPE.THREE_OF_A_KIND
        return HAND_TYPE.TWO_PAIRS

    if len(cards) == 4:
        return HAND_TYPE.ONE_PAIR

    return HAND_TYPE.HIGH_CARD


def get_hand_type_part2(hand: str):
    return min(
        [
            # Its okay to replace all jokers with the same card because we don't check for flushes
            get_hand_type(hand.replace("J", replacement))
            for replacement in [
                "A",
                "K",
                "Q",
                "T",
                "9",
                "8",
                "7",
                "6",
                "5",
                "4",
                "3",
                "2",
            ]
        ]
    )


def main():
    with open(os.path.join(os.path.dirname(__file__), "./input.txt")) as f:
        hands = [line.split(" ") for line in f.readlines()]

        hands_with_type = [
            (
                get_hand_type(card.strip()),
                list(map(get_card_type, card.strip())),
                card.strip(),
                int(bet.strip()),
            )
            for card, bet in hands
        ]
        hands_with_type = reversed(sorted(hands_with_type))

        total_winnings = 0
        for i, (type, card_list, hand, bet) in enumerate(hands_with_type):
            # print(f"Rank {i + 1}: Hand {hand} ({type})")
            total_winnings += (i + 1) * bet

        print(f"Part 1: {total_winnings}")

        hands_with_type = [
            (
                get_hand_type_part2(card.strip()),
                list(map(get_card_type_part2, card.strip())),
                card.strip(),
                int(bet.strip()),
            )
            for card, bet in hands
        ]
        hands_with_type = reversed(sorted(hands_with_type))

        total_winnings = 0
        for i, (type, card_list, hand, bet) in enumerate(hands_with_type):
            # print(f"Rank {i + 1}: Hand {hand} ({type})")
            total_winnings += (i + 1) * bet

        print(f"Part 2: {total_winnings}")


if __name__ == "__main__":
    main()
