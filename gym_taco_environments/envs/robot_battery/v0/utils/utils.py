from typing import List, Tuple, Dict
import numpy


class SpaceGenerator:
    def __init__(self, seed: int) -> None:
        self.random = numpy.random.RandomState(seed=seed)

    def generate_robot_battery_tuples(
        self, action: int, state: int, options: int, size: int
    ) -> List[Tuple]:
        if state == size**2 - 1:
            return [(1 / options, state, 1.0, True) for _ in range(options)]

        tuples = []
        greater_than_zero_above = state - size >= 0
        greater_than_zero_left = (state > 0) and ((state % size) != 0)
        smaller_than_max_bellow = (state + size) <= (size**2 - 1)
        smaller_than_max_right = (state < size**2 - 1) and ((state + 1) % size != 0)

        possible_actions = [
            state - size if greater_than_zero_above else state,
            state - 1 if greater_than_zero_left else state,
            state + size if smaller_than_max_bellow else state,
            state + 1 if smaller_than_max_right else state,
        ]

        good_above_goal = (state + size) == (size**2 - 1)
        good_next_to_goal = (state + 1) == (size**2 - 1)

        used_index = []
        for option in range(options):

            if option == 0:
                going_to_goal = (good_next_to_goal and action == 3) or (
                    good_above_goal and action == 2
                )
                tuples.append(
                    (
                        1 / options,
                        possible_actions[action],
                        1.0 if going_to_goal else 0.0,
                        True if going_to_goal else False,
                    )
                )
                used_index.append(action)
                continue

            random_index = self.random.randint(4)
            while random_index in used_index:
                random_index = self.random.randint(4)

            random_above_goal = possible_actions[random_index] == (size**2 - 1)
            random_next_to_goal = possible_actions[random_index] == (size**2 - 1)
            tuples.append(
                (
                    1 / options,
                    possible_actions[random_index],
                    1.0 if random_next_to_goal or random_above_goal else 0.0,
                    True if random_next_to_goal or random_above_goal else False,
                )
            )
            used_index.append(random_index)

        return tuples

    def generate_robot_battery_pmatrix(
        self, size: int
    ) -> Dict[int, Dict[int, List[Tuple]]]:
        result = {}
        i = 0
        for state in range(size**2):
            states = {}
            j = 0
            for action in range(4):

                options = self.random.randint(1, 4)

                states[j] = self.generate_robot_battery_tuples(
                    action, state, options, size
                )
                j += 1
            result[i] = states
            i += 1

        return result

    def generate_pmatrix(
        self, problem: str, size: int
    ) -> Dict[int, Dict[int, List[Tuple]]]:
        if problem == "robot_battery":
            return self.generate_robot_battery_pmatrix(size)

        return {0: {0: [()]}}
