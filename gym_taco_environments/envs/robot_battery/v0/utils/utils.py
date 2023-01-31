#!/usr/bin/python

import sys
import argparse
from typing import List, Tuple
import numpy as np
import json


def define_parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("-n", "--size", help="Matrix size", type=int)
    parser.add_argument("-p", "--problem", help="Problem ID", type=str)
    parser.add_argument("-f", "--file", help="Filepath", type=str)

    return parser.parse_args()


def generate_robot_battery_tuples(action: int, state: int, options: int, size: int) -> List[Tuple]:
    if state == size**2 - 1:
        return [(1/options, state, 1.0, True) for _ in range(options)]

    tuples = []
    greater_than_zero_above = state-size >= 0
    greater_than_zero_left = (state > 0) and ((state % size) != 0)
    smaller_than_max_bellow = (state+size) <= (size**2-1)
    smaller_than_max_right = (state < size**2-1) and ((state+1) % size != 0)

    possible_actions = [
        state-size if greater_than_zero_above else state,
        state-1 if greater_than_zero_left else state,
        state+size if smaller_than_max_bellow else state,
        state+1 if smaller_than_max_right else state
    ]

    good_above_goal = (state+size) == (size**2-1)
    good_next_to_goal = (state+1) == (size**2-1)

    used_index = []
    for option in range(options):

        if option == 0:
            going_to_goal = (good_next_to_goal and action == 3) or (
                good_above_goal and action == 2)
            tuples.append((
                1/options,
                possible_actions[action],
                1.0 if going_to_goal else 0.0,
                True if going_to_goal else False,
            ))
            used_index.append(action)
            continue

        random_index = np.random.randint(4)
        while random_index in used_index:
            random_index = np.random.randint(4)

        random_above_goal = possible_actions[random_index] == (size**2-1)
        random_next_to_goal = possible_actions[random_index] == (size**2-1)
        tuples.append((
            1/options,
            possible_actions[random_index],
            1.0 if random_next_to_goal or random_above_goal else 0.0,
            True if random_next_to_goal or random_above_goal else False,
        ))

    return tuples


def generate_robot_battery_pmatrix(size: int) -> List[List[List[Tuple]]]:
    result = []
    for state in range(size**2):
        states = []
        for action in range(4):
            actions = []
            options = np.random.randint(1, 4)
            actions.append(generate_robot_battery_tuples(
                action, state, options, size))
            states.append(actions)
        result.append(states)

    return result


def generate_pmatrix(problem: str, size: int) -> List[List[List[Tuple]]]:
    if problem == 'robot_battery':
        return generate_robot_battery_pmatrix(size)

    return [[[()]]]


if __name__ == "__main__":
    arguments = define_parse_arguments()

    f = open(arguments.file, 'w+')
    with f:
        json.dump(generate_pmatrix(arguments.problem, arguments.size), f)
