from typing import List, Tuple, Dict
from .maze_generator import prim_maze
import numpy
import math


class SpaceGenerator:
    def __init__(self, seed: int) -> None:
        self.random = numpy.random.RandomState(seed=seed)
        self.maze_generator = prim_maze.PrimMazeGenerator(self.random)

    def generate_frozen_lake_maze_tuples(
        self, action: int, state: int, options: int, height: int, width: int, maze, entrance_cell, exit_cell
    ) -> List[Tuple]:
        if maze[math.floor(state/width)-1][state % width] == 'w':
            return [(1, state, 0.0, False)]

        size = height*width
        if state == (exit_cell[0]*width+exit_cell[1]):
            return [(1 / options, state, 1.0, True) for _ in range(options)]

        tuples = []
        greater_than_zero_above = (state - width) >= 0
        greater_than_zero_left = (state > 0) and ((state % width) != 0)
        smaller_than_max_bellow = (state + width) <= (size - 1)
        smaller_than_max_right = (state < size) and ((state + 1) % width != 0)
        not_wall_up = maze[math.floor(
            state/width)-1][state % width] != 'w' if greater_than_zero_above else False
        not_wall_left = maze[math.floor(
            state/width)][(state % width)-1] != 'w' if greater_than_zero_left else False
        not_wall_right = maze[math.floor(
            state/width)][(state % width)+1] != 'w' if smaller_than_max_right else False
        not_wall_down = maze[math.floor(
            state/width)+1][state % width] != 'w' if smaller_than_max_bellow else False

        possible_actions = [
            state - width if greater_than_zero_above and not_wall_up else state,
            state - 1 if greater_than_zero_left and not_wall_left else state,
            state + width if smaller_than_max_bellow and not_wall_down else state,
            state + 1 if smaller_than_max_right and not_wall_right else state,
        ]

        good_above_goal = (state + width) == (exit_cell[0]*width+exit_cell[1])
        good_next_to_goal = (state + 1) == (exit_cell[0]*width+exit_cell[1])

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

            random_above_goal = possible_actions[random_index] == (
                exit_cell[0]*width+exit_cell[1])
            random_next_to_goal = possible_actions[random_index] == (
                exit_cell[0]*width+exit_cell[1])
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

    def generate_frozen_lake_maze_pmatrix(
        self, height: int, width: int
    ) -> Dict[int, Dict[int, List[Tuple]]]:
        maze, entrance_cell, exit_cell = self.maze_generator.generate_prim_maze(
            height, width)
        self.maze_generator.print_prim_maze(maze, height, width)
        result = {}
        i = 0
        for state in range(height*width):
            states = {}
            for action in range(4):
                options = self.random.randint(1, 4)
                states[action] = self.generate_frozen_lake_maze_tuples(
                    action, state, options, height, width, maze, entrance_cell, exit_cell
                )
            result[i] = states
            i += 1

        return result

    def generate_pmatrix(
        self, problem: str, height: int, width: int
    ) -> Dict[int, Dict[int, List[Tuple]]]:
        if problem == "frozen_lake_maze":
            return self.generate_frozen_lake_maze_pmatrix(height, width)

        return {0: {0: [()]}}
