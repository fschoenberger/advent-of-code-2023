import os


def game_to_dict(game: str) -> dict[str, int]:
    ret = {}
    for item in game.split(","):
        amount, color = item.strip().split(" ")
        ret[color] = int(amount)

    return ret


def main():
    with open(os.path.join(os.path.dirname(__file__), "./input.txt")) as f:
        lines = f.readlines()

        all_games = [line.split(":")[1].strip() for line in lines]
        games = []

        for game in all_games:
            draws = game.split(";")
            games.append([game_to_dict(draw) for draw in draws])

        actual_bag = {"red": 12, "green": 13, "blue": 14}

        sum_valid = 0

        for i, game in enumerate(games):
            valid = True
            for draw in game:
                for color, amount in draw.items():
                    if color in actual_bag and actual_bag[color] < amount:
                        print(f"Game {i + 1} is invalid")
                        valid = False
                        break

            if valid:
                print(f"Game {i + 1} is valid")
                sum_valid += i + 1

        print(f"Part 1: Sum of valid games: {sum_valid}")

        games_min_cubes = []
        for game in games:
            current_min_cubes = {}
            
            for draw in game:
                for color, amount in draw.items():
                    current_min_cubes[color] = max(current_min_cubes.get(color, 0), amount)

            games_min_cubes.append(current_min_cubes)

        print(games_min_cubes)

        games_power = []
        for min_cube in games_min_cubes:
            current_power = 1
            
            for color, amount in min_cube.items():
                current_power *= amount

            games_power.append(current_power)
        
        print(f"Part 2: Sum of power: {sum(games_power)}")
                    


if __name__ == "__main__":
    main()
