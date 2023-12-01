def tokenize(input: str) -> list[int]:
    tokens = []

    for it in range(len(input)):
        c = str(input[it])

        if c.isdigit():
            tokens.append(int(c))

    return tokens


def tokenize2(input: str) -> list[int]:
    numbers = ["one", "two", "three", "four", "five", "six", "seven", "eight", "nine"]

    tokens = []

    for it in range(len(input)):
        c = input[it]

        if c.isdigit():
            tokens.append(int(c))
        elif c.isalpha():
            potential_token = input[it : it + 5]

            for number in numbers:
                if potential_token.startswith(number):
                    tokens.append(numbers.index(number) + 1)
                    it += len(number) - 1
                    break

    return tokens


def main():
    input = """
"""

    lines = input.splitlines()

    digits = [tokenize(line) for line in lines]
    first_last = list(map(lambda x: x[0] * 10 + x[-1], digits))
    print(f"Part 1: {sum(first_last)}")

    digits2 = [tokenize2(line) for line in lines]
    first_last2 = list(map(lambda x: x[0] * 10 + x[-1], digits2))
    print(f"Part 2: {sum(first_last2)}")


if __name__ == "__main__":
    main()
