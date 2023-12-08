import math
import os
import re
import tqdm


def main():
    with open(os.path.join(os.path.dirname(__file__), "./input.txt")) as f:
        lines = f.readlines()

        path = lines[0].strip()
        nodes_list = [
            re.match("(.*) = \((.*), (.*)\)", node_declaration).groups()
            for node_declaration in lines[2:]
        ]
        nodes = {key: (left, right) for key, left, right in nodes_list}

        # print(nodes)

        def calculate_path(starting_node: str, is_end_node: callable) -> int:
            current_node = starting_node
            step_count = 0
            while not is_end_node(current_node):
                # print(f"Currently at {current_node} and going {path[step_count % len(path)]}")
                if path[step_count % len(path)] == "L":
                    current_node = nodes[current_node][0]
                else:
                    current_node = nodes[current_node][1]
                step_count += 1

            return step_count

        print(f"Part 1: {calculate_path('AAA', lambda x: x == 'ZZZ')}")

        result_nodes = [
            calculate_path(node, lambda x: x.endswith("Z"))
            for node in tqdm.tqdm(nodes.keys())
            if node.endswith("A")
        ]
        print(f"Part 2: {math.lcm(*result_nodes)}")


if __name__ == "__main__":
    main()
