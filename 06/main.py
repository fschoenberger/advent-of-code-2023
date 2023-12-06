import os
import re

def get_ways_to_win(time_alloted: int, distance_to_beat: int) -> int:
    ways_to_win = 0

    for button_hold_time in range(time_alloted):
        if (time_alloted - button_hold_time) * button_hold_time > distance_to_beat:
            ways_to_win += 1
    return ways_to_win

def main():
    with open(os.path.join(os.path.dirname(__file__), "./input.txt")) as f:
        time_string, distance_string = f.readlines()

        time = list(map(lambda x: int(x), re.findall("\d+", time_string)))
        distance =  list(map(lambda x: int(x), re.findall("\d+", distance_string)))

        races = list(zip(range(len(time)), time, distance))
        
        part1_result = 1

        for index, time_alloted, distance_to_beat in races:
            part1_result *= get_ways_to_win(time_alloted, distance_to_beat)
        
        print(f"Part 1: {part1_result}")

        time = int(time_string.split(":")[1].replace(" ", ""))
        distance = int(distance_string.split(":")[1].replace(" ", ""))

        print(f"Part 2: {get_ways_to_win(time, distance)}")

if __name__ == "__main__":
    main()
