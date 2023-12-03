import os
import re


def is_point_in_rectangle(x, y, x1, x2, y1, y2):
    return x1 <= x <= x2 and y1 <= y <= y2


def main():
    with open(os.path.join(os.path.dirname(__file__), "./input.txt")) as f:
        file = [line.strip() for line in f.readlines()]

        number_coordinates = []

        for index, line in enumerate(file):
            result = re.finditer(r"(\d+)", line)
            for match in result:
                number_coordinates.append(
                    {
                        "value": int(match.groups()[0]),
                        "x1": max(0, index - 1),
                        "x2": min(index + 1, len(file) - 1),
                        "y1": max(0, match.start() - 1),
                        "y2": min(match.end(), len(line) - 1),
                    }
                )

        part_numbers = []

        for number_coordinate in number_coordinates:
            # print("-----------")
            found = False

            for x in range(number_coordinate["x1"], number_coordinate["x2"] + 1):
                for y in range(number_coordinate["y1"], number_coordinate["y2"] + 1):
                    # print(f"Checking {x}, {y}: {file[x][y]}")
                    if file[x][y] in ["*", "@", "/", "-", "=", "#", "%", "$", "&", "+"]:
                        found = True
                        break

            if found:
                part_numbers.append(number_coordinate["value"])
                
        print(f"Part 1: {sum(part_numbers)}")

        gear_coordinates = []
        for x, line in enumerate(file):
            for y, char in enumerate(line):
                if char == "*":
                    gear_coordinates.append((x, y))

        gear_part_numbers = []
        for x, y in gear_coordinates:
            part_numbers = []

            for number_coordinate in number_coordinates:
                if is_point_in_rectangle(
                    x,
                    y,
                    number_coordinate["x1"],
                    number_coordinate["x2"],
                    number_coordinate["y1"],
                    number_coordinate["y2"],
                ):
                    part_numbers.append(number_coordinate["value"])
            gear_part_numbers.append(part_numbers)

        gear_part_numbers = [
            part_num[0] * part_num[1]
            for part_num in gear_part_numbers
            if len(part_num) == 2
        ]

        print(f"Part 2: {sum(gear_part_numbers)}")


if __name__ == "__main__":
    main()
