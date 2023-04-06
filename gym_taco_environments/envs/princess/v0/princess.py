import time
from .game import settings
import numpy as np
import math
import gym
from gym import spaces

from .game.Game import Game


class PrincessEnv(gym.Env):
    metadata = {"render_modes": ["human"], "render_fps": 4}

    def __init__(self, **kwargs):
        super().__init__()
        self.render_mode = kwargs.get("render_mode")
        self.game = Game("Princess Puzzle Env", self.render_mode)
        self.game_cols = self.game.world.tile_map.cols
        self.game_rows = self.game.world.tile_map.rows
        self.n = self.game_rows * self.game_cols
        self.observation_space = spaces.Discrete(self.n * self.n * self.n)
        self.action_space = spaces.Discrete(4)
        self.current_state = self.game.get_state()
        self.current_action = 0
        self.current_reward = 0.0
        self.delay = 1
        self.goal = None
        self.P = {}
        self.__build_P()

    def __compute_state_result(self, mc, s1, s2):
        return mc * self.n**2 + s1 * self.n + s2
    
    def get_game_state(self, row: int, col: int):
        return self.game_cols * row + col
    
    def get_game_position(self, state: int):
        row = math.floor(state / self.game_cols)
        col = state - (self.game_cols * row)

        return row, col

    def compute_step(self, action: int, mc: int, s1: int, s2: int):
        self.map = self.game.world.tile_map.map
        
        #Helper tuple to apply action movements
        move = (0, 0)
        if (action == 0):
            move = (0, -1)
        elif (action == 1):
            move = (1, 0)
        elif (action == 2):
            move = (0, 1)
        else:
            move = (-1, 0)

        #Convert the current loop position to the game position
        current_mc_pos = self.get_game_position(mc)
        current_s1_pos = self.get_game_position(s1)
        current_s2_pos = self.get_game_position(s2)

        #Action on the main character
        next_row = current_mc_pos[0]+move[0]
        next_col = current_mc_pos[1]+move[1]
        
        mc_can_move = (0 <= next_row < self.game_rows and 0 <= next_col < self.game_cols
            and (next_row, next_col) != current_s1_pos and (next_row, next_col) != current_s2_pos
            and self.map[next_row][next_col] != 0)

        if (mc_can_move):
            next_mc_pos = (next_row, next_col)
        else:
            next_mc_pos = current_mc_pos 
        
        #Action on s1, same direction as mc
        next_row = current_s1_pos[0]+(-1)*move[0]
        next_col = current_s1_pos[1]+(-1)*move[1]

        s1_can_move = (0 <= next_row < self.game_rows and 0 <= next_col < self.game_cols
            and (next_row, next_col) != current_s2_pos and self.map[next_row][next_col] != 0)
        
        if (s1_can_move):
            next_s1_pos = (next_row, next_col)
        else:
            next_s1_pos = current_s1_pos

        #Action on s1, opposite direction than mc
        next_row = current_s2_pos[0]+move[0]
        next_col = current_s2_pos[1]+move[1]
        
        s2_can_move = (0 <= next_row < self.game_rows and 0 <= next_col < self.game_cols
            and (next_row, next_col) != next_s1_pos and self.map[next_row][next_col] != 0)

        if (s2_can_move):
            next_s2_pos = (next_row, next_col)
        else:
            next_s2_pos = current_s2_pos

        #If the statues position is the same, undo it
        if next_s1_pos == next_s2_pos:
            next_s1_pos = current_s1_pos
            next_s2_pos = current_s2_pos

        reward = 0.0
        terminated = False
        current_state = self.__compute_state_result(mc, s1, s2)
        next_state = self.__compute_state_result(self.get_game_state(*next_mc_pos), 
            self.get_game_state(*next_s1_pos), self.get_game_state(*next_s2_pos))
        
        #Mc lost?
        if (next_mc_pos == next_s1_pos or next_mc_pos == next_s2_pos):
            reward = -100.0
            terminated = True
        #S1 won?
        elif (next_s1_pos == self.game.world.target_1 and next_s2_pos == self.game.world.target_2):
            reward = 1000.0
            terminated = True
            self.goal = next_state
        #S2 won?
        elif (next_s2_pos == self.game.world.target_1 and next_s1_pos == self.game.world.target_2):
            reward = 1000.0
            terminated = True
            self.goal = next_state
        #State didn't change?
        elif (current_state == next_state):
            reward = -10.0
        #State changed but didn't win or lose
        else:
            reward = -1.0

        return (next_state, reward, terminated)
    
    def __build_P(self):
        size = self.n
        all_states = self.observation_space.n
        actions = self.action_space.n
        probability = 1.0
        #Init P
        self.P = {state: {action: [] for action in range(actions)} for state in range(all_states)}

        for mc_state in range(size):
            for s1_state in range(size):
                for s2_state in range(size):
                    for action in range(actions):
                        state = self.__compute_state_result(mc_state, s1_state, s2_state)

                        if (state == self.goal):
                            self.P[state][action] = [(probability, state, 0.0, True)]
                        else:
                            next_state, reward, terminated = self.compute_step(action, mc_state, s1_state, s2_state)
                            
                            self.P[state][action] = [(probability, next_state, reward, terminated)]

    def reset(self, seed=None, options=None):
        super().reset(seed=seed)

        if options is not None:
            if not isinstance(options, dict):
                raise RuntimeError("Variable options is not a dictionary")
            self.delay = options.get("delay", 0.5)

        np.random.seed(seed)

        self.current_state = self.game.reset()
        self.current_action = 0
        self.current_reward = 0

        return self.__compute_state_result(*self.current_state), {}

    def step(self, action):
        self.current_action = action
        former_state = self.current_state
        self.current_state = self.game.update(self.current_action)

        if self.render_mode is not None:
            self.render()
            time.sleep(self.delay)

        _, target_state, reward, terminated = self.P[self.__compute_state_result(*former_state)][action][0]

        return (
            target_state,
            reward,
            terminated,
            False,
            {},
        )

    def render(self):
        self.game.render()

    def close(self):
        self.game.close()
